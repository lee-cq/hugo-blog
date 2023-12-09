---
title: "Async 协程入门"
author: "Li, Caleb Chaoqun"
date: 2023-02-13 00:00:00+0000
description: "初步了解异步编程"
typora-copy-images-to: ""
tags:
  - "Python"
  - "asyncio"
---
## Async 库和Python相关关键字

1. `async` - 关键字 - 定义一个 Async函数或方法

   ```python
   async def func():
       pass
   ```
2. `await` - 关键字 - 挂起 coroutine 的执行以等待一个 awaitable 对象。 只能在 coroutine function 内部使用。
> `await` 会创建一个task，将Task放入事件循环，释放操作句柄交给调度器，阻塞上下文知道await的Task返回结果

   ```python
   import asyncio

   async def func():
       await asyncio.sleep(1)

   ```
3. coroutine - 定义 - 协程
4. coroutine function - 定义 - 由 `async def ` 定义的函数；
5. conoutine object - 定义 - coroutine function的一个实例。

> 值得注意的是，当我们直接调用了一个 coroutine function 的时候，并不会调用该函数的具体内容，而是会生成一个 coroutine object，这个obj只有在asyncio 的 event_loop 中被调度。这个过程类似于我们生成器和生成器函数。

5. awaitable对象 - 定义 - 可以被await语句中使用的对象，可以是coroutine function, 或实现了 `__await__` 魔术方法的对象。
6. asyncio.run() - 函数 - 协程事件循环的入口。
7. asyncio.create_task() - 函数创建一个conoutine object包装为Task并加入到事件循环。
8. asyncio.gather(*coros_or_futures, return_exceptions=False) - 函数 - 返回给定协程futures 的未来聚合结果。  
协程将被包装在 future 中并在事件循环中进行调度。它们不一定按照传入的顺序进行安排。  
所有 future 必须共享相同的事件循环。如果所有任务都成功完成，则返回的 future 的结果是结果列表（按照原始序列的顺序，不一定是结果到达的顺序）。如果return_exceptions为True，则任务中的异常将被视为与成功结果相同，并收集在结果列表中；否则，第一个引发的异常将立即传播到返回的 future。  


## 相关视频：

{{< bilibili BV1oa411b7c9 >}}
