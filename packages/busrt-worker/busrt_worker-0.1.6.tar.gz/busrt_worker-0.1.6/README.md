# Busrt Worker
> `BUS/RT`是一个快速、灵活且非常易于使用的框架，它使用Rust/Tokio编写，受到NATS、ZeroMQ和Nanomsg的启发。

Busrt Worker是一个基于busrt消息中间件的异步框架，它对Python库进行了封装，使其更易于使用。


## 特点

- 异步：Busrt Worker基于python asyncio异步引擎，可以轻松处理高并发请求。
- 易用性：Busrt Worker对原生的busrt python客户端进行了封装，使用装饰器即可轻松创建rpc服务。
- 高性能：BUS/RT 使用Rust/Tokio编写，具有出色的性能和可靠性。

## 用法

要使用Busrt Worker，请按照以下步骤操作：

1. 安装Busrt Worker：`pip install busrt-worker`
2. 导入Busrt Worker：在您的Python项目中导入Busrt Worker。
3. 创建Busrt Worker App：创建一个App对象，并注册连接信息。
4. 处理消息：使用装饰器指明消息处理方式。

以下是一个示例代码片段，演示如何使用Busrt Worker：

```python
import asyncio

from loguru import logger

from busrtworker import App, ConnectionInfo
# 创建 App对象
app = App()

# 连接信息
api_ci = ConnectionInfo('api', 'localhost:9800', 'busrt.worker.test', static=True, topic='test/#')
caller_ci = ConnectionInfo('caller', 'localhost:9800', 'busrt.worker.test', static=True)

# 注册连接
api = app.registry(api_ci)
app.registry(caller_ci)

# rpc调用
@api.on_call()
def add(a, b):
    return a + b

# 主题订阅
@api.subscribe('test/:name')
def print_name(name: str):
    logger.info(f'{name} pub message')

# 钩子函数注册
@app.run_on_startup
async def test(server):
    async def call():
        await asyncio.sleep(1)
        logger.info(f'call remote add result {(await app.caller.add(api_ci.final_name,a=1, b=2))}')
        await app.caller.send('test/i_am_caller')
    asyncio.create_task(call())

# 启动程序
app.run()
```

## License
The MIT License.