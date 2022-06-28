+++
title= "Docker 安装"
date= "2021-06-15T17:23:47+08:00"
description = "Docker系列文章"
draft=false
tags= ["Docker", "安装"] 
categories = ["技术"]
series= ["Container"]
type="new"

+++





## Windows：

1. 下载并安装： [DockerInister.msi](http://mirrors.aliyun.com/docker-toolbox/windows/docker-for-windows/beta/InstallDocker.msi)



### Linux下使用官方Docker安装脚本: 

 `curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun`



### Debian/Ubuntu 用户

以下内容根据 [官方文档](https://docs.docker.com/engine/installation/linux/docker-ce/debian/) 修改而来。

如果你过去安装过 docker，先删掉:

```
sudo apt-get remove docker docker-engine docker.io
```

首先安装依赖:

```
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

根据你的发行版，下面的内容有所不同。你使用的发行版： Debian Ubuntu

信任 Docker 的 GPG 公钥:



```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
```

对于 amd64 架构的计算机，添加软件仓库:

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian \
   $(lsb_release -cs) \
   stable"
```

如果你是树莓派或其它ARM架构计算机，请运行:

```
echo "deb [arch=armhf] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian \
     $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list
```

最后安装

```
sudo apt-get update
sudo apt-get install docker-ce
```



### Fedora/CentOS/RHEL

以下内容根据 [官方文档](https://docs.docker.com/engine/installation/linux/docker-ce/centos/) 修改而来。

如果你之前安装过 docker，请先删掉

```
sudo yum remove docker docker-common docker-selinux docker-engine
```

安装一些依赖

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

根据你的发行版下载repo文件: CentOS/RHEL Fedora

```
wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
```

把软件仓库地址替换为 TUNA:

```
sudo sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```

最后安装:

```
sudo yum makecache fast
sudo yum install docker-ce
```





## 验证

输入`docker version`返回如下结果：

```tex
Client: Docker Engine - Community
 Version:           20.10.5
 API version:       1.41
 Go version:        go1.13.15
 Git commit:        55c4c88
 Built:             Tue Mar  2 20:18:20 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.5
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.13.15
  Git commit:       363e9a8
  Built:            Tue Mar  2 20:16:15 2021
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.4.4
  GitCommit:        05f951a3781f4f2c1911b05e61c160e9c30eaa8e
 runc:
  Version:          1.0.0-rc93
  GitCommit:        12644e614e25b05da6fd08a38ffa0cfe1903fdec
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```





## 启动

`systemctl enable docker`

> 根据您的Docker系统配置，您可能需要在每个Docker命令前使用sudo。
>
> 为了避免在使用docker命令时使用sudo，系统管理员可以创建一个名为docker的Unix组，并向其添加用户。

```bash
groupadd docker
usermod -G <UserName>
```





