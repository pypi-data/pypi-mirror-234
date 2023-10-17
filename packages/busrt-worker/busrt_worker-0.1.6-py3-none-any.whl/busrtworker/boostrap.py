import asyncio
import functools
import traceback
from typing import TYPE_CHECKING

from .busrt import Client, Rpc, RpcException, deserialize, on_frame_default, serialize

if TYPE_CHECKING:  # pragma: no cover
    from .app import App  # noqa: F401


class RpcBoot:
    async def startup(self, app: 'App'):
        for i, (name, connection) in enumerate(app.connections.items()):
            uri = connection.uri
            init_rpc = connection.init_rpc
            topic = connection.topic
            # connection.final_name = f'{prefix}.{name}' if static else f'{prefix}.{os.urandom(4).hex()}'
            bus = Client(uri, connection.final_name)
            connection.bus = bus

            app.closeable.append(bus.disconnect)

            async def callback(app_, _bus, topic):
                print('connect busrt')
                await _bus.connect()
                if topic:
                    await bus.subscribe(topic)
            app.run_on_startup(functools.partial(callback,_bus=bus,topic=topic))
            # await bus.connect()
            if topic:
                # await bus.subscribe(topic)

                async def on_frame(frame, router):
                    success, route, params = router.get(frame.topic)
                    if not success:
                        return await app.on_frame_default(frame)
                    else:
                        func, auto_decode, is_async, raw = route
                        if auto_decode:
                            payload = deserialize(frame.payload)
                            if raw:
                                payload['frame'] = frame
                            if is_async:
                                return await func(**payload, **params)
                            return func(**payload, **params)
                        else:
                            if is_async:
                                return await func(frame, **params)
                            return func(frame, **params)

                on_frame_func = functools.partial(on_frame, router=app.subscribes.get(name, None))
            else:
                on_frame_func = on_frame_default
            if init_rpc:

                async def on_call(event, caller):
                    try:
                        method = event.method.decode('utf-8')
                        caller_tuple = caller.get(method, None)
                        if not caller_tuple:
                            return serialize(await app.on_call_default(event))
                        call, auto_decode, is_async, raw = caller_tuple
                        if auto_decode:
                            payload = deserialize(event.get_payload())
                            if raw:
                                payload['event'] = event
                            if is_async:
                                return serialize(await call(**payload))
                            return serialize(call(**payload))
                        else:
                            if is_async:
                                return serialize(await call(event))
                            return serialize(call(event))
                    except Exception as e:
                        traceback.print_exc()
                        raise RpcException(str(e), 11)

                rpc_client = Rpc(bus)
                connection.rpc = rpc_client
                if topic:
                    rpc_client.on_frame = functools.partial(on_frame_func, router=app.subscribes.get(name, None))
                rpc_client.on_call = functools.partial(on_call, caller=app.callers.get(name, None))
            elif topic:
                bus.on_frame = functools.partial(on_frame_func, router=app.subscribes.get(name, None))

    async def shutdown(self, app: 'App'):
        gathers = []

        for func in app.closeable:
            if asyncio.iscoroutinefunction(func):
                gathers.append(func())
            else:
                try:
                    func()
                except:
                    traceback.print_exc()
        if gathers:
            await asyncio.gather(*gathers, return_exceptions=True)
