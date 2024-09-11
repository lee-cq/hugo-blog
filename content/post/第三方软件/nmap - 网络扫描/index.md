---
title: "nmap - 网络扫描器"
author: "Li, Caleb Chaoqun"
date: "2024-09-09"
description: "开源的网络探测和安全审核工具，可以用来扫描网络中的主机和服务，发现它们的端口开放情况、使用的协议、操作系统类型等信息。"
typora-copy-images-to: ""
image: 
math: 
license: 
tags:
  - "安全"
  - "网络"
  - "扫描"
  - "nmap"
---

nmap（Network Mapper）是一个开源的网络探测和安全审核工具，可以用来扫描网络中的主机和服务，发现它们的端口开放情况、使用的协议、操作系统类型等信息。

## 安装

Ubuntu & Debian :`sudo apt update && sudo apt install nmap`
CentOS & RHEL   : `sudo yum install nmap`

## 常用参数

```
-p 指定端口，","分割，"2-100"指定一个范围，"-"指定全部端口
-v 输出详细信息

-sP：执行Ping扫描，用于快速发现网络中的活动主机。
-sT：执行TCP连接扫描，默认的扫描方式。
-sS：执行TCP SYN扫描（半开扫描），发送SYN包而不建立完整的三次握手。
-sU：执行UDP扫描，探测开放的UDP端口。
-sA：执行ACK扫描，用于确定防火墙规则集。
-sW：执行Window扫描，用于探测防火墙规则集。
-sM：执行IP协议扫描，用于探测IP协议

-A：执行详细的扫描，包括操作系统检测、版本检测、脚本扫描和服务识别。
-T：设置扫描速度，取值范围从T0（最慢）到T5（最快）。
-O：执行操作系统检测。
-sV：执行服务版本检测。

-oN：将扫描结果输出到普通文本文件。
-oX：将扫描结果输出到XML文件。
-oG：将扫描结果输出到Grep格式文件。

--script：执行指定的脚本。
--script-help：显示脚本的帮助信息。

-D：指定欺骗源地址（IP欺骗）
-e：指定扫描时使用的接口。
-n：不执行DNS反向解析。
-R：强制执行DNS反向解析。
-Pn：假设目标主机是在线的，即使没有回应。

--max-retries：设置最大重试次数。
--host-timeout：设置主机超时时间。

```


## 使用

1. 扫描指定机器的全部端口: `nmap -p- -v -A <host>`
2. 扫描一个IP地址段: `nmap 192.168.1.1-255`
3. 