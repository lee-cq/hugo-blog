+++
title= "Docker网络详解"
date= "2023-02-26"
description = "Docker系列文章"
draft=false
tags= ["Docker", "常用命令", "CLI命令"]
categories = ["技术"]
series= ["Container", "Docker"]
type="new"

+++

# docker 网络

```shell
root@debian:~# docker network --help

Usage:  docker network COMMAND

Manage networks

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

Run 'docker network COMMAND --help' for more information on a command.

```

## docker 网络类型

### 1. bridge -- 网桥

是一个SNET, 将会创建一个子网

1. 在此网络中的容器将会分配一个子网地址；
2. 并通过NET端口映射访问服务；
3. 主机网络中的其他机器无法直接访问容器中的IP地址

### 2. host -- 主机网络

使用主机的IP地址。此网络类型智能被创建一个，特征如下：

1. 没有自己的IP地址，
2. 所有的网络信息复用主机（使用主机的命名空间）
3. 可以轻松与主机网络中的其他服务通信；
4. 由于没有独立的命名空间，容器和主机之间很容易产生端口冲突。

### 4. container -- 容器附加网络

相似于 **host** 网络，区别在于Host网络附加的是主机的IP地址，而 **container** 附加的是制定容器所拥有的IP地址；

### 3. none -- 空网络

不向容器分配网络，使用此模式的network容器无法联网，也无法使用网络通信（可以使用socket文件管道通信）

1. 容器中没有IP地址，无法与其他容器和主机直接通信；

### 4. macvlan -- 桥接网络

macvlan是另一种网桥，相当于交换网络中的交换机功能，容器会被分配一个和主机在同一个网断中的IP地址，拥有自己的IP，同样的主机网络中的其他机器也能直接轻松的直接访问到容器内部。

1. 拥有一个和主机IP在同一个网段的IP地址
2. 主机网络中的其他机器能够轻松的链接到容器

## 容器连接到网络

```bash
lcq@iMac ~ % docker network connect --help

Usage:  docker network connect [OPTIONS] NETWORK CONTAINER

Connect a container to a network

Options:
      --alias strings           Add network-scoped alias for the container
      --driver-opt strings      driver options for the network
      --ip string               IPv4 address (e.g., 172.30.100.104)
      --ip6 string              IPv6 address (e.g., 2001:db8::33)
      --link list               Add link to another container
      --link-local-ip strings   Add a link-local address for the container

```

## 将一个容器从指定网络中断开 disconnect

## 创建一个网络

```bash
lcq@LCQ-MacdeiMac ~ % docker network create --help

Usage:  docker network create [OPTIONS] NETWORK

Create a network

Options:
      --attachable           Enable manual container attachment. 
                             启用手动容器附件
      --aux-address map      Auxiliary IPv4 or IPv6 addresses used by Network driver (default map[]). 
                             网络驱动程序使用的辅助IPv4或IPv6地址(默认map[])
      --config-from string   The network from which to copy the configuration. 
                             要从中复制配置的网络
      --config-only          Create a configuration only network. 
                             创建一个只配置的网络
  -d, --driver string        Driver to manage the Network (default "bridge"). 
                             驱动程序来管理网络(默认的“桥”)
      --gateway strings      IPv4 or IPv6 Gateway for the master subnet. 
                             IPv4或IPv6主子网的网关
      --ingress              Create swarm routing-mesh network. 
                             创建群集路由网状网络
      --internal             Restrict external access to the network. 
                             限制外部对网络的访问
      --ip-range strings     Allocate container ip from a sub-range. 
                             从子范围分配容器ip
      --ipam-driver string   IP Address Management Driver (default "default"). 
                             IP地址管理驱动程序(默认为default)
      --ipam-opt map         Set IPAM driver specific options (default map[]). 
                             设置IPAM驱动程序特定选项(默认map[])
      --ipv6                 Enable IPv6 networking. 
                             启用IPv6组网
      --label list           Set metadata on a network. 
                             设置网络元数据
  -o, --opt map              Set driver specific options (default map[]). 
                             设置驱动程序特定的选项(默认map[])
      --scope string         Control the network's scope. 
                             控制网络范围
      --subnet strings       Subnet in CIDR format that represents a network segment. 
                             CIDR格式的子网，表示一个网段
```

1. 创建一个简单docker网络
   `docker network create <name>`
2. 创建一个macvlan网络
   `docker network create -d macvlan --subnet=192.168.0.0/24 --gateway=172.16.10.1 -o parent=en1 mac1`

## 查看指定网络的详细信息 inspect

## 列出当前Docker服务的全部网路 list

## 删除为使用的网络 prune

## 删除置顶网络 rm
