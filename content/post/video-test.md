---
title: "video-test"
date: 2021-07-31T00:33:55+08:00
description: 测试Hugo对HTML video标签的解析能力
image: https://one.p.leecq.cn/E5Drive/imgs/1.jpg
typora-copy-images-to: ../../static/img
draft: false
tags: 
  - 建站
  - Hugo
categories: 
  - "测试"
series: 
  - Hugo
---

 



# video test

支持的 Shortcodes 详见: https://docs.stack.jimmycai.com/zh/writing/shortcodes

## HTML Code

```html
    <video src="https://alist.leecq.cn/onedrive/1_1_48ed6325509e3d97c2b6eed7eabd821dc61c7518.mp4" controls  ></video>
```

![](../../static/img/test.jpg)

## HTML video 测试1
<video controls="controls" preload controls width=100%>
  <source src="https://alist.leecq.cn/d/onedrive/1_1_48ed6325509e3d97c2b6eed7eabd821dc61c7518.mp4" type="video/mp4" />
Your browser does not support the video tag.
</video>





## HTML video 测试2
<video src="https://alist.leecq.cn/d/onedrive/%E4%B8%AD%E5%9B%BD%E6%9C%BA%E9%95%BF1080P.mp4?sign=dc625e8ea4bb25a8" controls preload width=100% > </video>

## Shortcodes bilibili 测试

{{< bilibili BV1Ht4y1p7aA >}}



## Shortcodes 腾讯视频

{{< tencent  b31563j0jqw >}}

## Shortcodes 本地视频
```html
<!-- just video src -->
{{< video "./video.mp4">}}

<!-- Other option -->
{{< video src="./video.mp4" autoplay="true" poster="./video-poster.png" >}}
```

{{< video "https://alist.leecq.cn/d/onedrive/1_1_48ed6325509e3d97c2b6eed7eabd821dc61c7518.mp4">}}

## 