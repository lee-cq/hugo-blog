---
title: "Hugo无法解析md中HTML代码"
date: 2021-06-20T00:33:55+08:00
description: Hugo 解析markdown时， 无法显示其中的HTML语句段
draft: false
tags: 
  - 建站
  - Hugo
categories: 
  - "技术"
series: 
  - Hugo
---

## Hugo 解析markdown时， 无法显示其中的HTML语句段

- **问题**： hugo默认情况下无法正常显示markdown中内嵌的html，在生成的网页中，html代码会被`<!-- raw HTML omitted -->`替代。 

- **原因**： 在2019年11月的hugo更新中，使用了Goldmark作为默认库，该库认为在md文档中嵌入HTML是不安全的行为；

- **解决方法**： 在Hogo的配置文件中添加如下代码段，以屏蔽其安全机制：
  ```toml
  [markup]
  [markup.goldmark]
  [markup.goldmark.renderer]
    unsafe = true
  ```

  或者是yaml:
  
  ```yaml
  # 注意yaml的缩进可能不适用于你的文件
  markup:
    goldmark:
      renderer:
        unsafe: true
  ```
  
  
  
- **来源**： 作者：new房昭之 https://www.bilibili.com/read/cv4516916 出处：bilibili



### 例子

#### code 向网页注入video标签

```html
<video src="https://alist.leecq.cn/d/onedrive/1_1_48ed6325509e3d97c2b6eed7eabd821dc61c7518.mp4" controls width=100% >你的浏览器不支持video标签,是时候换浏览器了</video> 

```

<video src="https://alist.leecq.cn/d/onedrive/1_1_48ed6325509e3d97c2b6eed7eabd821dc61c7518.mp4" controls width=100% >你的浏览器不支持video标签<br/>是时候换浏览器了</video> 	

