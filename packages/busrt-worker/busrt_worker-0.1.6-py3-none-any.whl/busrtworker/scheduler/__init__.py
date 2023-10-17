import asyncio
import time
from collections.abc import AsyncIterator
from typing import Any, Awaitable, Callable, Coroutine, Optional, Set, Union

AsyncFuncType = Callable[[Any, Any], Awaitable[Any]]
class ClockTicker(AsyncIterator):
    """
    T - A clock tick
    F - Something that happens inside an iteration ("x" = running "-" = waiting)
    I - A clock iteration

    E.g:

    async for tick in Clock(seconds=2):
        await asyncio.sleep(3)


    T: 15------17------19------21------23------25------27------29------
    F: xxxxxxxxxxxxx---xxxxxxxxxxxxx---xxxxxxxxxxxxx---xxxxxxxxxxxxx---
    I: x---------------x---------------x---------------x---------------

    """

    def __init__(self, seconds: Union[float, int]) -> None:
        """
        :param seconds: Tick interval in seconds
        """
        self.seconds = seconds
        self.current_iteration = 0
        self._tick_event = asyncio.Event()
        self._running: Optional[bool] = None
        self._main_task: Optional[asyncio.Future] = None

    def __aiter__(self) -> AsyncIterator:
        if self._running is not None:
            raise RuntimeError("Cannot reuse a clock instance.")

        self._running = True
        self._main_task = asyncio.ensure_future(self._run())
        return self

    async def __anext__(self) -> int:
        if not self._running:
            raise StopAsyncIteration

        self._tick_event.clear()
        await self._tick_event.wait()

        i = self.current_iteration
        self.current_iteration += 1
        return i

    async def _run(self) -> None:
        while self._running:
            self._tick_event.set()
            await asyncio.sleep(self.seconds)
            self._tick_event.clear()

    async def stop(self) -> None:
        self._running = False
        if self._main_task:
            await self._main_task


def perf_counter_ms() -> float:
    """
    Return the value (in fractional milliseconds) of a performance counter,
    i.e. a clock with the highest available resolution to measure a short
    duration. It does include time elapsed during sleep and is system-wide.
    The reference point of the returned value is undefined, so that only the
    difference between the results of consecutive calls is valid.
    """
    return time.perf_counter() * 1000


class ScheduledTaskRunner:
    def __init__(
            self,
            seconds: int,
            task: Callable[[], Coroutine],
            max_concurrency: int,
    ) -> None:
        self.seconds = seconds
        self.max_concurrency = max_concurrency
        self.task = task
        self.running_tasks: Set[asyncio.Future] = set()
        self.task_is_done_event = asyncio.Event()
        self._started = False
        self.clock = ClockTicker(seconds=self.seconds)

    async def can_dispatch_task(self) -> bool:
        if len(self.running_tasks) < self.max_concurrency:
            return True

        if await self.task_is_done_event.wait():
            return True
        return False

    async def _wrapped_task(self) -> None:
        """
        Wraps the future task on a coroutine that's responsible for unregistering
        itself from the "running tasks" and emitting an "task is done" event
        """
        try:
            await self.task()
        finally:
            self.task_is_done_event.set()
            self.running_tasks.remove(asyncio.current_task())  # type: ignore

    async def start(self,*args,**kwargs) -> asyncio.Future:
        self._started = True
        return asyncio.ensure_future(self._run())

    async def stop(self,*args,**kwargs) -> None:
        await self.clock.stop()
        await asyncio.gather(*self.running_tasks)

    async def _run(self) -> None:
        async for _ in self.clock:
            if await self.can_dispatch_task():
                task = asyncio.ensure_future(self._wrapped_task())
                self.running_tasks.add(task)
                self.task_is_done_event.clear()
