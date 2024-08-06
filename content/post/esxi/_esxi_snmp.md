---
title: esxi snmp 配置
description: esxi snmp 配置
slug: yujunshu-2
date: 2022-10-29 00:00:00+0000
categories:
    - OS
tags:
    - esxi
    - snmp
---



# esxi snmp 配置

esxi 详细文档设置[VMware vSphere 文档](https://docs.vmware.com/cn/VMware-vSphere/index.html)

## 开启 snmp

```she
esxcli system snmp set --communities public,private
esxcli system snmp set --enable true
```



## 配置轮询的 SNMP 代理

```shell
esxcli system snmp set --port 1600
```



