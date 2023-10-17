import abc
import asyncio
import dataclasses
import functools
import os
import signal
from collections import UserList
from enum import Enum, auto
from typing import Callable, Coroutine, Dict, List, Optional

from loguru import logger

from busrtworker.boostrap import RpcBoot
from busrtworker.busrt import OP_PUBLISH, Client, Frame, Rpc, serialize
from busrtworker.kink import di
from busrtworker.scheduler import ScheduledTaskRunner
from busrtworker.tree import RadixTree


@dataclasses.dataclass
class ConnectionInfo:
    name: str = dataclasses.field()
    uri: str = dataclasses.field()
    client_prefix: str = dataclasses.field()
    static: bool = dataclasses.field()
    topic: str | None = dataclasses.field(default=None)
    init_rpc: bool = dataclasses.field(default=True)
    bus: Client = dataclasses.field(default=None, init=False)
    rpc: Rpc = dataclasses.field(default=None, init=False)
    _final_name: str = dataclasses.field(default=None, init=False)

    @property
    def final_name(self):
        if self._final_name:
            return self._final_name
        else:
            self._final_name = f'{self.client_prefix}.{self.name}' if self.static else f'{self.client_prefix}.{os.urandom(4).hex()}'
        return self._final_name

    def __getattr__(self, item):
        if not self.init_rpc:
            raise ValueError('must be init rpc client could call')
        return getattr(self.rpc, item)

    async def send(self, topic, data=None, decode=True):
        bus: Client = self.bus
        await bus.send(topic, Frame(serialize(data) if decode else data, tp=OP_PUBLISH))

    def client_name(self):
        if not self.bus:
            raise ValueError('must be init busrt client could call')
        return self.bus.name


class Router:
    table: dict = {}
    tree: RadixTree = RadixTree()

    def insert(self, path, handler, dynamic=False):
        if not dynamic:
            if path in self.table:
                raise ValueError(f'conflict route {path}')
            self.table[path] = handler
        else:
            self.tree.insert(path, handler, ['RPC'])

    def get(self, path):
        if path in self.table:
            return True, self.table[path], {}
        return self.tree.get(path, 'RPC')


class ServiceEntrypoint:
    def __init__(self, connection: ConnectionInfo, app: 'App'):
        self.name = connection.name
        self.app = app
        if self.name not in self.app.callers:
            self.app.callers[self.name] = {}
        if self.name not in self.app.subscribes:
            self.app.subscribes[self.name] = Router()

    def on_call(self, method=None, auto_decode: bool = True, raw: bool = False):
        def _warp(f):
            target = method or (f.func.__name__ if isinstance(f, functools.partial) else f.__name__)
            self.app.callers[self.name][target] = (f, auto_decode, asyncio.iscoroutinefunction(f), raw)
            return f

        return _warp

    def subscribe(self, topic: str, auto_decode: bool = True, raw: bool = False):
        assert isinstance(topic, str), 'topic must be str'

        def _warp(f):
            self.app.subscribes[self.name].insert(topic, (f, auto_decode, asyncio.iscoroutinefunction(f), raw),
                                                  '/:' in topic)
            return f

        return _warp


class Freezable(metaclass=abc.ABCMeta):
    def __init__(self):
        self._frozen = False

    @property
    def frozen(self) -> bool:
        return self._frozen

    async def freeze(self):
        self._frozen = True


class Signal(UserList, asyncio.Event):
    """
    Coroutine-based signal implementation tha behaves as an `asyncio.Event`.

    To connect a callback to a signal, use any list method.

    Signals are fired using the send() coroutine, which takes named
    arguments.
    """

    def __init__(self, owner: Freezable) -> None:
        UserList.__init__(self)
        asyncio.Event.__init__(self)
        self._owner = owner
        self.frozen = False

    def __repr__(self):
        return "<Signal owner={}, frozen={}, {!r}>".format(
            self._owner, self.frozen, list(self)
        )

    async def send(self, *args, **kwargs):
        """
        Sends data to all registered receivers.
        """
        if self.frozen:
            raise RuntimeError("Cannot send on frozen signal.")

        for receiver in self:
            await receiver(*args, **kwargs)

        self.frozen = True
        await self._owner.freeze()
        self.set()


async def on_frame_default(app, frame):
    logger.opt(lazy=True).debug('{x}',
                                x=lambda: f"default print 'Frame:', {hex(frame.type)}, frame.sender, frame.topic, frame.payload")


async def on_call_default(app, event):
    logger.opt(lazy=True).debug('{x}',
                                x=lambda: f"default print 'Rpc:', {event.frame.sender}, {event.method}, {event.get_payload()}")


def entrypoint(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))
        except KeyboardInterrupt:
            pass

    return _


class AutoNameEnum(str, Enum):
    def _generate_next_value_(  # type: ignore
            name: str, start: int, count: int, last_values: List[str]
    ) -> str:
        return name.lower()


class Options(AutoNameEnum):
    MAX_CONCURRENCY = auto()


class DefaultValues:
    RUN_EVERY_MAX_CONCURRENCY = 1


class App(Freezable):
    callers: dict[str, callable] = {}
    subscribes: dict[str, Router] = {}
    connections: Dict[str, ConnectionInfo] = {}
    closeable = []
    on_frame_default: callable = on_frame_default
    on_call_default: callable = on_call_default
    task_runners = []

    def __init__(self):
        Freezable.__init__(self)
        self.boot = RpcBoot()
        self._on_startup: Signal = Signal(self)
        self._on_shutdown: Signal = Signal(self)
        self._on_startup.append(self.boot.startup)
        self._on_shutdown.append(self.boot.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def registry(self, connection: ConnectionInfo):
        if self.frozen:
            raise RuntimeError(
                "You shouldn't change the state of a started application"
            )
        self.connections[connection.name] = connection
        return ServiceEntrypoint(connection, self)

    def set_on_frame_default(self, on_frame: callable):
        self.on_frame_default = on_frame

    def set_on_call_default(self, on_call: callable):
        self.on_call_default = on_call

    @entrypoint
    async def run(self):
        if self.frozen:
            raise RuntimeError(
                "You shouldn't change the state of a started application"
            )
        logger.debug({"event": "Booting App..."})
        await self.startup()

        await self._on_shutdown.wait()

    async def startup(self):
        """
        Causes on_startup signal

        Should be called in the event loop along with the request handler.
        """
        await self._on_startup.send(self)

    def shutdown(self, *args) -> asyncio.Future:
        """
        Schedules an on_startup signal

        Is called automatically when the application receives
        a SIGINT or SIGTERM
        """
        logger.debug('do shutdown')
        return asyncio.ensure_future(self._on_shutdown.send(self))

    def run_on_startup(self, coro: Callable[["App"], Coroutine]) -> None:
        """
        Registers a coroutine to be awaited for during app startup
        """
        self._on_startup.append(coro)

    def run_on_shutdown(self, coro: Callable[["App"], Coroutine]) -> None:
        """
        Registers a coroutine to be awaited for during app shutdown
        """
        self._on_shutdown.append(coro)

    def __getattr__(self, name):
        return self.connections[name]

    def __getitem__(self, name):
        return self.connections[name]

    def __setitem__(self, key, value):
        di[key] = value

    def run_every(self, seconds: int, options: Optional[Dict] = None):
        """
        Registers a coroutine to be called with a given interval
        """
        if options is None:
            options = {}

        max_concurrency = options.get(
            Options.MAX_CONCURRENCY, DefaultValues.RUN_EVERY_MAX_CONCURRENCY
        )

        def wrapper(task: Callable[..., Coroutine]):
            runner = ScheduledTaskRunner(
                seconds=seconds,
                task=task,
                max_concurrency=max_concurrency,
            )
            self._on_startup.append(runner.start)
            self._on_shutdown.append(runner.stop)
            self.task_runners.append(runner)

            return task

        return wrapper

    def rpc_running(self, name):
        if connection := self.connections.get(name, None):
            if rpc := connection.rpc:
                return rpc.is_connected()
        return False
