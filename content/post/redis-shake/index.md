---
author: "Lee, Caleb Chaoqun"
title: "Redis Shake 错误总结"
date: "2021-07-30"
description: "在使用redis Shake 中遇到的一些奇奇怪怪的问题。"
typora-copy-images-to: ../../static/img
tags:
  - "Redis"
  - "Redis Shake"
  - "Question"
  - "Fix"
---
Redis-Shake 2.+ 版本

# 同步过程中终止

### 报错：

### 问题原因：

在同步过程中会出现一些集群（副本）管理相关的操作指令，这些指令不应该跨集群同步。

这些错误目前发现主要出现在源集群有slave的情况下。

### 解决方案：

在配置文件中加入或修改 项： `filter.command.blacklist` 中追加 `replconf` ，用于过滤replconf 指令的同步。



# 重连后全量同步过成中的RDB Save Error

### 报错：

```log
[PANIC] restore command error key:gmv2022-09-18 00:00:00690047125391hyper1092HYPERCPC err:MISCONF Redis is configured to save RDB snapshot
```

### 问题原因  

redis save rdb 失败，具体根因未知。  

### 解决方案

删除全部集群节点中的 rdb 和 aof 文件 并重启集群。

