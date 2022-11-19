---
title: "iptables 实现端口转发"
author: "Li, Caleb Chaoqun"
date: "2022-11-17"
description: "在Linux上通过iptables实现端口转发，实现DNAT功能。"
typora-copy-images-to: ""
tags:
  - "Linux"
  - "iptables"
  - "NAT"
---


# iptables 实现端口转发

## 1. 确保IPv4内核流量转发功能开启

```bash
echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf
sysctl -p
```

## 2. 配置iptables抓发规则


流量状态：
Inter --> 10.0.4.14:13389 -->  10.1.1.10:3389

```bash
# 将外网访问192.168.75.5的80端口转发到192.168.75.3:8000端口。
iptables -t nat -A PREROUTING -d 10.0.4.14 -p tcp --dport 13389 -j DNAT --to-destination 10.1.1.10:3389
 
# 将192.168.75.3 8000端口将数据返回给客户端时，将源ip改为192.168.75.5
iptables -t nat -A POSTROUTING -d 10.1.1.10 -p tcp --dport 3389 -j SNAT --to 10.0.4.14
```
