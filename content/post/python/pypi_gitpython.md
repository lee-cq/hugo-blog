+++
title= "GitPython入门"
date= "{{ .Date }}"
description = "Python操作Git的库"
draft=true
tags= ["Python", "pypi", "GitPython"] 
categories = ["Python"]
+++

## 本地存储库相关操作

```python
from git import Repo

# 初始化一个存储库并返回一个Repo对象
repo =Repo.init('/path/to/repo')

# 创建一个Repo对象连接到本地存储库
repo = Repo('/path/to/repo')

repo.git  # Repo Git API操作

repo.git.add(file_name) # 将文件添加到暂存区

repo.index.commit(message)  # 将暂存区的文件提交到库

repo.untracked_files  # 返回未跟踪文件列表

repo.create_remote()  # 创建一个远程库对象并绑定到
```



## 远程存储库相关操作

```python
remote = Remote()  # 实例化一个远程仓库

repo.create_remote(name, url)  # 添加一个远程库

# 推送到远程仓库
repo.remote(name).push("master:master")  
# 从远程仓库拉取
repo.remote(name).pull()
# 从Repo中移除一个remote
repo.remote(name).remove()  

```



## 其他操作

1. HTTP存储库可以在URL中指定用户名和密码： `https://USER:PASSWD@HOST/URI`
