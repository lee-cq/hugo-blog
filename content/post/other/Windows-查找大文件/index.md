---
title: "Windows-查找大文件"
date: 2025-09-13T14:33:55+08:00
description: Windows-查找大文件
image: 
draft: false
tags: 
  - Windows
  - 运维
categories: 
  - 
---

# Windows-查找大文件

使用命令：

```bat
forfiles /p E:\ /s /m *.* /c "cmd /c if @fsize geq 104857600 (echo @path @fsize)" > E:\big_files.txt
```

将结果导入Excel进行排序和分析

