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


## 3. iptables配置仅内网可以访问脚本

```bash
iptables -F  # 删除全部的规则
iptables -X  # 删除全部自定义的链

iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT  # 允许已经建立的连接

# 添加允许的IP地址段示例
iptables -A INPUT -i lo -j ACCEPT  # 允许lo接口的全部流量
iptables -A INPUT -s 192.168.0.0/16 -j ACCEPT  # 允许192.168.0.0/16网段的入栈流量
iptables -A INPUT -s 10.0.0.0/8 -j ACCEPT  # 允许10.0.0.0/8网段的入栈流量
iptables -A INPUT -s 172.16.0.0/12 -j ACCEPT  # 允许172.16.0.0/12网段的入栈流量
iptables -A INPUT -s 100.64.0.0/12 -j ACCEPT  # 允许100.64.0.0/12网段的入栈流量

# 添加允许端口示例
iptables -A INPUT -p tcp --dport 8000 -j ACCEPT  # 允许全部的IP地址访问8000端口
iptables -A INPUT -p tcp -s 10.0.0.0/8 --dport 8000 -j ACCEPT  # 仅允许10.0.0/8网段访问8000端口

iptables -P INPUT DROP  # 默认拒绝INPUT链
iptables -P OUTPUT ACCEPT  # 默认允许OUTPUT链
iptables -P FORWARD DROP  # 默认拒绝FORWARD链
```