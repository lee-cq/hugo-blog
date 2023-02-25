---
title: "Async 协程入门"
author: "Li, Caleb Chaoqun"
date: "2023-2-13"
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
6. asyncio.run() - 函数 - 协程事件循环的入口

## 相关视频：

{{< bilibili BV1oa411b7c9 >}}
