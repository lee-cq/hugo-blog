+++
title= "Docker常用命令详解"
date= "2021-06-23"
description = "Docker系列文章"
draft=false
tags= ["Docker", "常用命令", "CLI命令"]
categories = ["技术"]
series= ["Container"]
type="new"

+++

## 帮助命令

```bash
docker version  # 查看docker版本；
docker info     # 显示Docker的系统信息，详细；
docker [command] help  # 万能帮助命令，不会就查
```

> 想要更深入的了解Docker-CLI命令，参见官方文档：
>
> [Use the Docker command line | Docker Documentation](https://docs.docker.com/engine/reference/commandline/cli/)

## 镜像命令

> 镜像相关命令都是  `docker image ` 的子命令；

### `docker image ` 镜像管理

> 下面介绍的命令全部是这些子命令的别名；

```bash

Usage:  docker image COMMAND

Manage images

Commands:
  build       从Dockerfile构建一个映像
  history     显示镜像的历史
  import      从tar包中导入内容以创建文件系统映像
  inspect     在一个或多个镜像的显示详细信息
  load        从tar归档文件或STDIN加载映像
  ls          列出镜像 (docker images)
  prune       移除不再使用的镜像
  pull        从一个注册表中拉取一个镜像或仓库
  push        向一个注册表中推送一个镜像或仓库
  rm          移除一个或多个镜像 (docker rmi)
  save        将一个或多个映像保存到tar归档文件中 (默认输出到STDOUT)
  tag         创建一个指向SOURCE_IMAGE的标记TARGET_IMAGE

Run 'docker image COMMAND --help' for more information on a command.
```

### `docker images` Docker 镜像查询

```bash
$ docker images [OPTIONS] [REPOSITORY[:TAG]]

Options:
  -a, --all             展示全部的镜像（默认忽略中间镜像）
      --digests         展示摘要信息
  -f, --filter filter   根据所提供的条件过滤输出
      --format string   使用Go模板打印漂亮的镜像
      --no-trunc        不截断输出
  -q, --quiet           只显示图像ID


REPOSITORY        TAG              IMAGE ID       CREATED         SIZE
postgres          latest           26c8bcd8b719   2 months ago    314MB

# REPOSITORY  
# 仓库源    
# TAG 标签            
# IMAGE ID 镜像ID      
# CREATED  创建时间    
# SIZE 大小

```

### `docker search ` 搜索Docker镜像

```bash
用法:  docker search [OPTIONS] TERM

在Docker Hub中搜索图像

Options:
  -f, --filter filter   根据所提供的条件过滤输出
      --format string   使用Go模板美化打印搜索
      --limit int       最大搜索结果数目(默认25个)
      --no-trunc        不截断输出

# 示例1： 搜索stars>300 的Tomcat镜像: 
$ docker search -f=STARS=300 tomcat
```

### `docker pull` 下载镜像

```bash

Usage:  docker pull [OPTIONS] NAME[:TAG|@DIGEST]

Pull an image or a repository from a registry

Options:
  -a, --all-tags                下载存储库中所有Tag的镜像
      --disable-content-trust   跳过镜像验证 (default true)
      --platform string         如果服务器具有多平台功能，则设置平台（Windows|Linux|Mac）
  -q, --quiet                   抑制详细输出，静默下载
  

# 示例： 下载MySQL
$ docker pull mysql

Using default tag: latest  # 使用默认的latest版本
latest: Pulling from library/mysql
69692152171a: Pull complete   # 分层下载镜像
1651b0be3df3: Pull complete 
951da7386bc8: Pull complete 
0f86c95aa242: Pull complete 
37ba2d8bd4fe: Pull complete 
6d278bb05e94: Pull complete 
497efbd93a3e: Pull complete 
f7fddf10c2c2: Pull complete 
16415d159dfb: Pull complete 
0e530ffc6b73: Pull complete 
b0a4a1a77178: Pull complete 
cd90f92aa9ef: Pull complete 
Digest: sha256:d50098d7fcb25b1fcb24e2d3247cae3fc55815d64fec640dc395840f8fa80969 # 签名
Status: Downloaded newer image for mysql:latest
docker.io/library/mysql:latest  # 真实地址


# 示例2： 指定5.7版本的MySQL镜像
$ docker pull mysql:5.7

5.7: Pulling from library/mysql
69692152171a: Already exists # 不再下载已经存在的层
1651b0be3df3: Already exists 
951da7386bc8: Already exists 
0f86c95aa242: Already exists 
37ba2d8bd4fe: Already exists 
6d278bb05e94: Already exists 
497efbd93a3e: Already exists 
a023ae82eef5: Pull complete 
e76c35f20ee7: Pull complete 
e887524d2ef9: Pull complete 
ccb65627e1c3: Pull complete 
Digest: sha256:a682e3c78fc5bd941e9db080b4796c75f69a28a8cad65677c23f7a9f18ba21fa
Status: Downloaded newer image for mysql:5.7
docker.io/library/mysql:5.7


```

### 删除镜像 `docker rmi` && `docker image rm `

```bash
# 实际上 rmi 是 docker image rm 的一个别名

Usage:  docker image rm [OPTIONS] IMAGE [IMAGE...]

Remove one or more images

Aliases:
  rm, rmi, remove

Options:
  -f, --force      Force removal of the image
      --no-prune   Do not delete untagged parents


```

## 容器命令

> 有镜像才能创建容器

### `docker run` 运行一个容器

```bash
Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Run a command in a new container

Options:  ## 由于太多选择些常用的

  --name   创建的容器的名字
  -it      以交互式启动容器
  -d       后台启动容器
  -p       指定容器的端口
       -p 主机端口:容器端口
       -p 容器端口
       -p ip:主机端口:容器端口
  -P       随机指定端口
  -v       挂载数据卷
  -h       指定容器的主机名
  -e username="ritchie": 设置环境变量；
  --env-file=[]: 从指定文件读入环境变量；
  --rm     容器退出是自动移除容器
  
 
# 示例1： 交互式启动CentOS
docker run -it centos

# 示例2： 后台启动Nginx并绑定实际端口
docker run -P -d  nginx

# 示例3：使用镜像 nginx:，以后台模式启动一个容器,将容器的 80 端口映射到主机的 80 端口,主机的目录 /data 映射到容器的 /data。
docker run -p 80:80 -v /data:/data -d nginx

```

### 退出容器

1. 执行 `exit`
2. 按 `Ctrl-P-Q`

### `docker rm ` 删除容器

```bash
Usage:  docker rm [OPTIONS] CONTAINER [CONTAINER...]

Remove one or more containers

Options:
  -f, --force     强制删除正在运行中的容器 (使用SIGKILL信号)
  -l, --link      删除指定的链接
  -v, --volumes   删除与容器关联的匿名卷
  

docker rm 容器ID
docker rm -f 
docker rm -f $(docker ps -aq)  # 删除全部的容器
docker ps -aq |xargs docker rm 

```

### 启动和停止容器

```BASH
docker start 容器ID
docker restart 
docker stop   # 停止当前正在运行的容器
docker kill   # 强制停止正在运行的容器

```

## 常用的其他命名

### 进入一个正在运行的容器 `exec|attach  `

> exec: 创建一个新的终端并进入。

```bash
Usage:  docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

Run a command in a running container
在正在运行的容器中运行命令

Options:
  -d, --detach               分离模式:在后台执行命令
      --detach-keys string   覆盖分离容器的键序列
  -e, --env list             设置环境变量
      --env-file list        读入一个环境变量文件
  -i, --interactive          Keep STDIN open even if not attached
      --privileged           Give extended privileges to the command
  -t, --tty                  Allocate a pseudo-TTY
  -u, --user string          Username or UID (format: <name|uid>[:<group|gid>])
  -w, --workdir string       Working directory inside the container

```

> attach： 进入一个现有的终端！容器当前正在运行的终端；相当于附加了一块屏幕

```bash
Usage:  docker attach [OPTIONS] CONTAINER

Attach local standard input, output, and error streams to a running container
将本地标准输入、输出和错误流附加到正在运行的容器

Options:
      --detach-keys string   覆盖分离容器的键序列
      --no-stdin             不附加标准din
      --sig-proxy            代理进程接收到的所有信号 (default true)

```

### 查看日志命令  `docker logs`

> 实际上输出的是容器的标准输出和标准错误、

```bash
Usage:  docker logs [OPTIONS] CONTAINER

Fetch the logs of a container

Options:
      --details        显示提供给日志的额外详细信息
  -f, --follow         跟踪日志输出
      --since string   显示时间戳后的日志 (e.g. 2013-01-02T13:23:37Z) or
                       relative (e.g. 42m for 42 minutes)
  -n, --tail string    从日志末尾开始显示的行数 (default "all")
  -t, --timestamps     显示时间戳
      --until string   显示时间戳之前的日志 (e.g. 2013-01-02T13:23:37Z)
                       or relative (e.g. 42m for 42 minutes)

# 示例1： 显示ID的10条日志并持续输出，显示时间戳
docker logs -tf --tail 10 ID
```

### 查看容器中的进程

`Usage:  docker top CONTAINER [ps OPTIONS]`

显示容器的运行进程; 相当于在容器中运行ps 命令；

### 查看镜像的元数据 `docker instect`

```bash

Usage:  docker inspect [OPTIONS] NAME|ID [NAME|ID...]

Return low-level information on Docker objects
返回Docker对象的底层信息

Options:
  -f, --format string   使用给定的Go格式化输出template
  -s, --size            如果类型是容器，则显示总文件大小
      --type string     返回指定类型的JSON

```

### 从容器内拷贝文件到主机上

```bash

Usage:  docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
	docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH

Copy files/folders between a container and the local filesystem
在容器和本地文件系统之间复制文件/文件夹

Use '-' as the source to read a tar archive from stdin
and extract it to a directory destination in a container.
使用'-'作为源，从stdin读取tar归档文件，并将其解压缩到容器中的目录目标。
Use '-' as the destination to stream a tar archive of a
container source to stdout.
使用'-'作为目标，将容器源的tar压缩包流到标准输出。

Options:
  -a, --archive       归档模式(复制所有uid/gid信息)
  -L, --follow-link   始终遵循SRC_PATH中的符号链接


# 示例1：复制容器a12中的文件 /applog/root.log 复制到 主机的/root 目录
docker cp a12:/applog/root.log /root


```
