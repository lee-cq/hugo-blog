---
title: "Linux 小技巧"
author: "Li, Caleb Chaoqun"
date: "2022-11-17"
description: "Linxu实用的一下小命令"
typora-copy-images-to: ""
tags:
  - "Linux"
  - "Tips"
---
## Linux 修改指定进程的打开文件数限制

`prlimit --pid {pid} --nofile=65535:65535`

## 查询指定PID打开的句文件柄数

`lsof -n | awk '{print $2}' |sort |uniq -c |sort -nr |grep PID`

## 查询指定PID的limit信息

`cat /proc/$PID/limits`

## Telnet 自动超时退出

`timeout --signal=9 {timout_sec} telnet {ip} {port}`

## MySQL导出前100条数据

`mysqldump -uroot -p'password'  {db} --where "1=1 limit 100" > test.sql`

## 使用Python快速开启一个简单的文件服务器

`python3 -m http.server` 或 `python -m SimpleHTTPServer`
