+++
title= "Docker配置镜像加速"
date= "2021-06-22"
description = "Docker系列文章"
draft=false
tags= ["Docker", "国内源", "阿里源"] 
categories = ["技术"]
series= ["Container"]
type="new"

+++



## 阿里云镜像加速

1. 打开地址： [容器镜像服务 (aliyun.com)](https://cr.console.aliyun.com/cn-shanghai/instances/mirrors)
2. 开通容器镜像服务；
3. 点击镜像加速器；
4. 根据指引添加相应的配置文件。

Linux 执行以下命令：

```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://eyu4btqs.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```





## 腾讯云镜像加速

无



