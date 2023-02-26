+++
title= "pip 更换国内源"
date= "2023-02-25"
description = "Docker系列文章"
draft=false
tags= ["Docker", "常用命令", "CLI命令"]
categories = ["技术"]
series= ["Container", "Docker"]
type="new"
+++



## 配置方法

a. 找到下列文件

`~/.pip/pip.conf`
b. 在上述文件中添加或修改:
  
```conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```


## 新版pip配置方法

直接使用 `pip config`命令；

```bash

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
```
