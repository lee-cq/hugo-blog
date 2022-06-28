+++
title= "Docker基本命令"
date= "2021-06-22"
description = "Docker系列文章 - 基本命令集"
draft=false
tags= ["Docker", "--help", "-h"] 
categories = ["技术"]
series= ["Container"]
type="new"
+++

# Docker基本命令



> 详细信息参见： [Use the Docker command line | Docker Documentation](https://docs.docker.com/engine/reference/commandline/cli/)



## Docker 全局选项 - OPTIONS

```tex
Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers
容器自给自足的运行时

Options:
      --config string      Location of client config files (default "/root/.docker")
                           客户端配置文件的位置(默认“/root/.docker”)
  -c, --context string     Name of the context to use to connect to the daemon 
                           (overrides DOCKER_HOST env var and default context set with 
                           "docker context use")
                           用于连接守护进程的上下文的名称
                           (用"docker context use"重写DOCKER_HOST环境变量的值)
  
  -D, --debug              Enable debug mode
                            启用debug模式
  -H, --host list          Daemon socket(s) to connect to
                           需要连接的守护socket
                              
  -l, --log-level string   Set the logging level 
                           ("debug"|"info"|"warn"|"error"|"fatal") (default "info")
                          设置日志级别(默认INFO)
                              
      --tls                Use TLS; implied by --tlsverify
                              使用TLS；
      --tlscacert string   Trust certs signed only by this CA 
                            (default "/root/.docker/ca.pem")
                            仅信任由此CA签署的证书
                              
      --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
                          TLS证书文件路径
                              
      --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
                          TLS证书key路径
                              
      --tlsverify          Use TLS and verify the remote
                            使用TLS并验证远程证书
      
  -v, --version            Print version information and quit
                          打印版本信息并退出
```

## Docker管理指令
```tex
Management Commands:  管理指令
  app*        Docker App (Docker Inc., v0.9.1-beta3)
  builder     Manage builds
  buildx*     Build with BuildKit (Docker Inc., v0.5.1-docker)
  config      Manage Docker configs
  container   Manage containers  管理容器
  context     Manage contexts  管理上下文
  image       Manage images
  manifest    Manage Docker image manifests and manifest lists  》》 ？？？？ 《《
  network     Manage networks
  node        Manage Swarm nodes  管理集群节点
  plugin      Manage plugins   管理插件
  secret      Manage Docker secrets  
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes
```

## Docker普通指令
```tex
Commands:
  attach      Attach local standard input, output, and error streams to a running container
                将本地标准输入、输出和错误流附加到正在运行的容器中
  build       Build an image from a Dockerfile
                从Dockerfile构建一个镜像
  commit      Create a new image from a container's changes
                根据容器的更改创建一个新映像
  cp          Copy files/folders between a container and the local filesystem
                在容器和本地文件系统之间复制文件/文件夹
  create      Create a new container
                创建一个新的容器
  diff        Inspect changes to files or directories on a container's filesystem
                检查容器文件系统中文件或目录的更改
  events      Get real time events from the server
                 从服务器获取实时事件
  exec        Run a command in a running container
                在正在运行的容器中运行命令
  export      Export a container's filesystem as a tar archive
              导出容器的文件系统作为tar存档
  history     Show the history of an image
              展示一个镜像的历史版本
  images      List images
  import      Import the contents from a tarball to create a filesystem image
              从tar存档导入内容以创建文件系统映像
  info        Display system-wide information
              显示全系统信息    
  inspect     Return low-level information on Docker objects
              返回Docker对象的低级信息
  kill        Kill one or more running containers
              杀死一个或多个正在运行的容器
  load        Load an image from a tar archive or STDIN
              从tar或者STDIN加载镜像
  login       Log in to a Docker registry
                登录到Docker注册表
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
              收集容器的日志
  pause       Pause all processes within one or more containers
              暂停一个或多个容器内的所有过程
  port        List port mappings or a specific mapping for the container
              列出容器的端口映射或特定映射
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
              将图像或存储库推送到注册表
  rename      Rename a container
              重命名一个容器
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
              将一个或多个镜像保存到tar存档(默认情况下流至STDOUT)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
              启动一个或多个停止的容器
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
              创建一个引用SOURCE_IMAGE的标记TARGET_IMAGE
  top         Display the running processes of a container
              显示容器的运行过程
  unpause     Unpause all processes within one or more containers
              取消暂停一个或多个容器内的所有进程
  update      Update configuration of one or more containers
              更新一个或多个容器的配置
  version     Show the Docker version information
              显示Docker版本信息
  wait        Block until one or more containers stop, then print their exit codes
              阻塞直到一个或多个容器停止，然后打印它们的退出代码

Run 'docker COMMAND --help' for more information on a command.
运行“docker COMMAND --help”获得更多关于命令的信息。

To get more help with docker, check out our guides at https://docs.docker.com/go/guides/
为了得到更多的帮助码头，看看我们的指南在https://docs.docker.com/go/guides/
```







