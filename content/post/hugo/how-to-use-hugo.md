---
title: "Hugo 快速开始"
date: 2021-05-29T00:33:55+08:00
description: Hugo是最流行的开源静态站点生成器之一, 简单的介绍它的使用方式。
image: img/hugo-hone-page.png
draft: false
tags: 
  - 建站
  - Hugo
categories: 
  - "技术"
series: 
  - Hugo
---



> ## The world’s fastest framework for building websites.



Hugo是最流行的开源静态站点生成器之一。凭借其惊人的速度和灵活性，Hugo使构建网站再次变得有趣。

===

## 安装

​		Hugo是由Go语言开发的软件, 你可以在 [GitHub ](https://github.com/gohugoio/hugo)或者 [镜像地址]()上获取到它的源码, 自行编译; 或者在 [Releases · gohugoio/hugo · GitHub](https://github.com/gohugoio/hugo/releases/) 获取到预编译版本 . 



​		或者使用下面的指令一键安装

### 1. Windows 

    ```powershell
    # 1. 安装包管理工具 choco
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    # 2. 安装 Hugo
    choco install hugo -confirm
    # 如果你需要安转拓展的 Sass/SCSS 版本执行:
    choco install hugo-extended -confirm
    ```



### 2. Mac OS

    ```shell
    # 1. 安装包管理工具 Brew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # 2. 安装hugo
    brew install hugo
    ```

    

### 3. Linux 

    ```shell
    # Debian / Armbian / Ubuntu
    apt install hugo
    # CentOS
    yum install hugo
    ```

    

## 快速开始

​		快速的建立一个hugo构建的blog.

### 1. **初始化:  **
`hugo new site <BlogName>`
    执行此步骤后会在工作目录中创建一个名为 `BlogName`的目录, 其中包含了站点的基本元素;

    ```sh
    <BlogName>
    |   config.toml   # 项目配置文件
    +-+-archetypes    # 
    | \--   default.md
    +---content       # 内容, 创作的blog放在这个目录下
    +---data          # 
    +---layouts
    +---static        # 静态文件
    \---themes        # 主题文件
    ```

    

### 2. **添加主题:**

    > 推荐的主题:  [Next](https://leecq.lanzoui.com/ijqbUpki8vc )

    你可以查看[themes.gohugo.io](themes.gohugo.io)上的主题列表。或者在社区中搜索你喜欢的主题样式.

    把主题下载下来后添加到项目的`themes`目录

    最后修改项目目录下的 `config.toml`  使其`theme=<你下载的主题名字>`

    

### 3. **添加内容: **
`hugo new posts/my-first-post.md`

    > 注意: 他需要当前工作目录是你的项目目录, 否则会报错. 找不到config.toml

    执行此步骤会在`content/` 下创建 `posts/my-first-post.md` 文件作为一篇文章.

    使用`MarkDown`标记语法构建.

    

### 4. **编辑和修改你的文章**

    如果你想编辑新创建的内容文件，它会像这样开始:

```markdown
---
title: "My First Post"
date: 20121-05-29T08:47:11+08:00
draft: true  
---

# 草稿不会被部署;一旦你完成了一篇文章，更新文章标题，写上draft: false
```

### 5. **启动Hugo服务器 **

    `hugo server -D`
    现在，启动Hugo服务器并启用草稿:

    新网站一般会被部署在 `http://localhost:1313/`。

### 6. 自定义主题

    打开并编辑`config.toml`文件.

```toml
baseURL = "https://example.org/"
languageCode = "en-us"
title = "My New Hugo Site"
theme = "ananke"
```

    用一自己的东西替换上面的标题。

    另外，如果您已经准备好了一个域名，那么设置baseURL。注意，运行本地开发服务器时不需要这个值。

    > 提示:
    >
    > ​		当Hugo服务器运行时，对站点配置或站点中的任何其他文件进行更改，您将立即在浏览器中看到更改，但您可能需要清空缓存。

    *有关特定于主题的配置选项，请参阅[主题站点](https://github.com/theNewDynamic/gohugo-theme-ananke)。*

    

### 7. **构建静态页面 `hugo -D`** 

    默认情况下输出将在`./public/ `目录下.

    你可以使用 `-d / --destination `标记来显示的指定输出位置.

