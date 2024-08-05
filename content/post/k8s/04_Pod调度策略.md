---
title: "Kubernetes调度流程及策略"
author: "Li, Caleb Chaoqun"
date: "2024-08-05"
description: "在Kubernetes中，调度是指将Pod放置到合适的Node上，然后对应Node上的Kubelet才能够运行这些pod。"
typora-copy-images-to: ""
tags:
  - "K8s"
  - "Kubernetes"
  - "运维"
  - "调度"
---

# Kubernetes调度流程及策略

在Kubernetes中，调度是指将Pod放置到合适的Node上，然后对应Node上的Kubelet才能够运行这些pod。

## Predicates vs. Priorities

### Predicates函数
先于Priority函数执行，用于硬条件过滤。常见策略如：

- CheckNodeCondition: 检查Node是否符合调度条件。
- HostName：检查Node的名称是否为Pod的指定的Hostname。
- MatchNodeSeletctor：检查Node的标签是否满足Pod的nodeSelector属性hard选择器需求。requiredDuringSchedulingIgnoredDuringExecution
- PodFitsResources：检查Node的资源是否满足Pod的需求。
- Taint&Toleration：Pod容忍度设置NoSchedule或NoExecute，用来避免Pod被分配到不合适的节点上。

### Priorities函数
将Predicate函数执行结果进行计算评分后排序，得分最高Node进行Pod调度。常见策略如：

- LeastRequested：按空闲度（空闲容量/总容量）进行Node排序。
- BalanceResourceAllocation：资源均匀分布，必须与LeastRequested同时使用。
- SelectorSpreading：对于属于同一个service、rc的Pod，尽量分散在不同的主机上。
- NodeAffinity：检查Node的标签是否满足Pod的nodeSelector属性soft选择器需求。preferresDuringSchedulingIgnoredDuringExecution
- Taint&Toleration：Pod容忍度设置PreferNoSchedule。

## NodeName
Kubernetes支持多种自定义调度方式，指定NodeName调度是最简单的一种，可以将Pod调度到期望的节点上。

通过spec.spec.nodeName字段强制约束将Pod调度到指定的Node节点上，这里说是“调度”，但其实指定了nodeName的Pod会直接跳过Scheduler的调度逻辑，直接写入PodList列表，该匹配规则是强制匹配。

```yaml
apiVersion: extensions/v1beta1
kind: Deployment

metadata:
  name: tomcat-deploy
  
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: tomcat-app
  spec:
    nodeName: k8s.node1 #指定调度节点为k8s.node1
    containers:
    - name: tomcat
      image: tomcat:8.0
      ports:
      - containerPort: 8080
```

## nodeSelector

通过kubernetes的label-selector机制进行节点选择，由scheduler调度策略MatchNodeSelector进行label匹配，调度pod到目标节点，启用NodeSelector的步骤为：
- 为指定Node添加label标记。
- Pod定义spec.nodeSelector字段，指定key-value键值。

`$ kubectl label nodes k8s.node1 App=tomcat Phase=prod`
```yaml
apiVersion: extensions/v1beta1
kind: Deployment

metadata:
  name: tomcat-deploy

spec:
  replicas: 1
  template:
  metadata:
    labels:
      app: tomcat-app
  spec:
    nodeSelector:
    - App: tomcat
    - Phase: prod #指定调度节点为带有label标记为：App=tomcat, Phase=prod的node节点
    containers:
    - name: tomcat
      image: tomcat:8.0
      ports:
      - containerPort: 8080
```

## nodeAffinity

相较nodeName和nodeSelector，Affinity/Anti-affinity极大地拓展了可以表达的约束类型，语法更灵活，不仅仅支持“与”（AND），且可以指明非强制规则（preferred），以及你可以使用拓扑分布来约束Pod在集群内的分布。

目前支持两种类型的Node Affinity，可以视它们为“硬需求”和“软需求”。  
`requiredDuringSchedulingIgnoredDuringExecution`  && `
preferredDuringSchedulingIgnoredDuringExecution`

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: with-node-affinity
spec:
  affinity:  # 亲和关系
    nodeAffinity: # 节点亲和
      requiredDuringSchedulingIgnoredDuringExecution: # 硬需求 - 强制需要
        nodeSelectorTerms:  
        - matchExpressions:
          - key: kubernetes.io/os
            operator: In
            values: linux
      preferredDuringSchedulingIgnoredDuringExecution: # 软需求 - 优先需要
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values: another-node-label-value
  containers:
  - name: with-node-affinity
    image: k8s.gcr.io/pause:2.0
```

## PodAffinity

Podaffinity/anti-affinity让我们基于Pod标签，而不是基于节点上的标签来约束Pod可以调度到的节点。与节点亲和性一样，当前有两种类型的podAffinity:
- `requiredDuringSchedulingIgnoredDuringExecution`
- `preferredDuringSchedulingIgnoredDuringExecution`

Pod间亲和性通过pod.spec中affinity字段下的podAffinity字段进行指定；而Pod间反亲和性通过pod.spec中affinity字段下的podAntiAffinity字段进行指定。

```yaml
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
        matchExpressions:
        - key: security
          operator: In
          values: S1
          topologyKey: topology.kubernetes.io/zone
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
      labelSelector:
      matchExpressions:
      - key: security
        operator: In
        values: S2
      topologyKey: topology.kubernetes.io/zone
```

## Taint(污点) & Toleration(容忍度)

节点亲和性是Pod的一种属性，它能让Pod被调度到一类特定的节点上。而污点则相反，它使节点排斥一类特定的Pod（由容忍度决定），从而避免Pod调度到该节点上。

**污点（Taint）：** 每个节点上都可以应用一个或多个污点，污点是与“效果”相关联的键值对，效果包括：
- NoSchedule：不能容忍此污点的Pod不会被调度到节点上；现有Pod不会从节点中逐出。
- PreferNoSchedule：Kubernetes会避免将不能容忍此污点的Pod安排到节点上。
- NoExecute：如果Pod已在节点上运行，则会将该Pod从节点中逐出；如果尚未在节点上运行，则不会将其安排到节点上。


**容忍度（Tolerations）：** 容忍度应用于Pod上，允许（但并不要求）Pod调度到带有与之匹配的污点的节点上。

### 操作方法：

通过kubectl给Node1增加污点：  
`$ kubectl taint nodes node1 key1=value1:NoSchedule`

移除上述污点：  
`$ kubectl taint nodes node1 key1=value1:NoSchedule-`

我们可以在pod.spec中定义Pod的容忍度。下面2个的忍度均与上面例子中使用`kubectl taint`命令创建的污点相匹配，因此如果一个Pod拥有其中的任何一个容忍度都能够被分配到node1。

```yaml
Kind: Pod
...
spec:
  tolerations:
  - key: "key1"
    operator: "Equal"
    value: "value1"
    effect: "NoSchedule"
...
```
```yaml
tolerations:
- key: "key1"
  operator: "Exists"
  effect: "NoSchedule"
```

