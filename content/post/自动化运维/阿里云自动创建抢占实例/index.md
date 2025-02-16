---
title: "阿里云自动创建抢占实例"
description: 
date: 2025-02-15T17:24:41+08:00
image: 
math: 
license: 
hidden: false
comments: true
draft: false
tags:
  - 运维
  - aliyun
  - 自动化

---



# Aliyun快速创建ECS实例 - Clash

1. 设置合适的安全组
在控制台中设置安全组并记录组ID：开放22, 80, 443, 3389端口。

2. 编写启动脚本
克隆项目，或从OSS下载启动文件, 。
从蓝奏云上下载数据，并部署
```bash
自定义
```

3. 运行实例
使用模板或者使用自定义参数。
```json
{
  "RegionId": "cn-shenzhen",  # 区域

  "InstanceType": "ecs.e-c1m1.large",   
  "ImageId": "ubuntu_24_04_x64_20G_alibase_20250113.vhd",
  "SystemDisk.Size": 20,  # 系统盘大小
  "SystemDisk.Category": "cloud_essd_entry", # 系统盘类型
  "SecurityEnhancementStrategy": "Active",  # 安全加固Active：启用安全加固，Deactive：不启用安全加固

  "InstanceChargeType": "PostPaid",  # 实例计费类型 - 后付费
  "SpotStrategy": "SpotAsPriceGo",  # 按量付费实例的竞价策略。SpotAsPriceGo - 系统自动出价，跟随当前市场实际价格
  "SpotInterruptionBehavior": "Terminate",  # 抢占实例中断模式。 Terminate：直接释放实例。
  "InternetChargeType": "PayByTraffic",  # 网络计费类型，按流量
  "AutoRenew": false,  # 自动续费

  "InternetMaxBandwidthIn": 100,
  "InternetMaxBandwidthOut": 10,  # 出带宽大于0 自动分配公网IP
  "VSwitchId": "vsw-wz9q3hnkysu1p4sc*****",  # 绑定交换机
  "SecurityGroupId": "sg-wz9etfd2xhsxa1p*****", # 绑定安全组
  
  "ResourceGroupId": "rg-acfmvpl4ra*****",  # 资源组
  "InstanceName": "api-test",  # 实例名字
  "HostName": "api-test",  # 主机名
  "Password": "****",  # 密码
  "UserData": "Iy9iaW4vYmFzaAplY2hvICJzdGFydCBFQ1MiID4gdGVzdC50eHQ=",  # 用户脚本
  "DryRun": false,  # 测试运行
}
```

Aliyun CLI 参数
```bash
user_data="Iy9iaW4vYmFzaAplY2hvICJzdGFydCBFQ1MiID4gdGVzdC50eHQ"
ecs_password="*******"
relase_time=$(date --date="@$(date -d '+4 hours' +%s)" +'%Y-%m-%dT%H:%M:%SZ' -u)  # 获取4小时后的UTC时间

# 查询价格
aliyun ecs DescribePrice --force --RegionId cn-shenzhen --ImageId "ubuntu_24_04_x64_20G_alibase_20250113.vhd" \
    --InstanceType "ecs.e-c1m1.large" --SystemDisk.Category cloud_essd_entry --SystemDisk.Size 20 \
    --InstanceChargeType PostPaid --SpotStrategy SpotAsPriceGo --SpotInterruptionBehavior Terminate \
    --InternetChargeType PayByTraffic --InternetMaxBandwidthOut 10 --InternetMaxBandwidthIn 100 \
    --VSwitchId vsw-wz9q3hnkysu1p4scm**** --SecurityGroupId sg-wz9etfd2xhsxa1p**** \
    --HostName "api-test" --Password "${ecs_password}"  --DryRun true

# 创建实例
ecs_password="*******"
aliyun ecs RunInstances --RegionId cn-shenzhen --ImageId "ubuntu_24_04_x64_20G_alibase_20250113.vhd" \
    --InstanceType "ecs.e-c1m1.large" --SystemDisk.Category cloud_essd_entry --SystemDisk.Size 20 \
    --InstanceChargeType PostPaid --SpotStrategy SpotAsPriceGo --SpotInterruptionBehavior Terminate \
    --InternetChargeType PayByTraffic --InternetMaxBandwidthOut 10 --InternetMaxBandwidthIn 100 \
    --VSwitchId vsw-wz9q3hnkysu1p4scm**** --SecurityGroupId sg-wz9etfd2xhsxa1p**** \
    --HostName "api-test" --Password "${ecs_password}"  --UserData ${user_data} --AutoReleaseTime ${relase_time} \
    --DryRun true
```
返回结果：{
  "InstanceIdSets": {
    "InstanceIdSet": [
      "i-wz91g5uy6dgm8gas****"
    ]
  },
  "RequestId": "C449D45D-CC95-5BDD-9438-9DD139679A48"
}

得到实例ID： `jq -r '.InstanceIdSets.InstanceIdSet[0]`

4. 分配IP地址
使用StartInstance创建实例时，需要手动调用分配公网IP API（出带宽必须大于0）；
使用RunInstancesces创建实例时，当出带宽打于0时，自动分配IP。

5. 查询ECS信息
调用查询接口 
```bash
aliyun ecs DescribeInstanceAttribute --region cn-shenzhen --InstanceId 'i-wz91g5uy6dgm8gas****'
```
返回：{
        "ClusterId": "",
        "Cpu": 2,
        "CreationTime": "2025-02-15T09:52:38Z",
        "CreditSpecification": "",
        ......
        "Memory": 2048,
        "OperationLocks": {
                "LockReason": []
        },
        "PublicIpAddress": {
                "IpAddress": [
                        "47.119.180.220"
                ]
        },
        "RegionId": "cn-shenzhen",
        ......
        },
        "ZoneId": "cn-shenzhen-e"
}

查询公网IP地址。aliyun ecs DescribeInstanceAttribute  --InstanceId 'i-wz91g5uy6dgm8gas****' |jq .PublicIpAddress.IpAddress[0] -r

6. 更新DNS到主机
更新IP地址信息到DNSPOD。

```bash
curl -X POST https://dnsapi.cn/Record.Modify --header 'User-Agent: HostCreate/v0.1(lee-cq@qq.com)' \
    -d 'login_token=${LOGIN_TOKEN}&format=json&domain=${DOMAIN}&sub_domain=ali-host&record_type=A&record_line_id=10%3D0&value=${pub_ip}'

# Aliyun DNS
aliyun alidns AddDomainRecord --region cn-shenzhen --DomainName 'DOMAIN' --RR 'api-test' --Type A --Value ${pub_ip}
```


7. 手动释放实例
```bash
aliyun ecs DeleteInstance --region cn-shenzhen --InstanceId 'i-wz91g5uy6dgm8gasp6ac' --Force true # 强制释放实例

record_id=$(curl -X POST https://dnsapi.cn/Record.List --header 'User-Agent: HostCreate/V0.1(lee-cq@qq.com)' \
    -d 'login_token=${LOGIN_TOKEN}&format=json&domain_id=${DOMAIN}&sub_domain=ali-host' | jq -r '.records[0].id')

# 删除DNS解析
curl -X POST https://dnsapi.cn/Record.Remove --header 'User-Agent: HostCreate/V0.1(lee-cq@qq.com)' \
    -d 'login_token=${LOGIN_TOKEN}&format=json&domain=${DOMAIN}&record_id=${record_id}'
```



## 完整脚本
```bash
user_data="Iy9iaW4vYmFzaAplY2hvICJzdGFydCBFQ1MiID4gdGVzdC50eHQ"
ecs_password="*******"
relase_time=$(date --date="@$(date -d '+4 hours' +%s)" +'%Y-%m-%dT%H:%M:%SZ' -u)  # 获取4小时后的UTC时间
DOMAIN=""

# 查询价格
aliyun ecs DescribePrice --force --RegionId cn-shenzhen --ImageId "ubuntu_24_04_x64_20G_alibase_20250113.vhd" \
    --InstanceType "ecs.e-c1m1.large" --SystemDisk.Category cloud_essd_entry --SystemDisk.Size 20 \
    --InstanceChargeType PostPaid --SpotStrategy SpotAsPriceGo --SpotInterruptionBehavior Terminate \
    --InternetChargeType PayByTraffic --InternetMaxBandwidthOut 10 --InternetMaxBandwidthIn 100 \
    --VSwitchId vsw-wz9q3hnkysu1p4scm**** --SecurityGroupId sg-wz9etfd2xhsxa1p**** \
    --HostName "api-test" --Password "${ecs_password}"  --DryRun true

# 创建实例
ecs_password="*******"
aliyun ecs RunInstances --RegionId cn-shenzhen --ImageId "ubuntu_24_04_x64_20G_alibase_20250113.vhd" \
    --InstanceType "ecs.e-c1m1.large" --SystemDisk.Category cloud_essd_entry --SystemDisk.Size 20 \
    --InstanceChargeType PostPaid --SpotStrategy SpotAsPriceGo --SpotInterruptionBehavior Terminate \
    --InternetChargeType PayByTraffic --InternetMaxBandwidthOut 10 --InternetMaxBandwidthIn 100 \
    --VSwitchId vsw-wz9q3hnkysu1p4scm**** --SecurityGroupId sg-wz9etfd2xhsxa1p**** \
    --HostName "api-test" --Password "${ecs_password}"  --UserData ${user_data} \
    --AutoReleaseTime ${relase_time} | tee /dev/tty |jq -r '.InstanceIdSets.InstanceIdSet[0]' > ecs-instance-id

# 查询公网IP地址
aliyun ecs DescribeInstanceAttribute --region cn-shenzhen --InstanceId "$(cat ecs-instance-id)" | tee /dev/tty | jq -r .PublicIpAddress.IpAddress[0] > ecs-instanse-ip

# 将公网IP地址注册到DNSPOD
curl -X POST https://dnsapi.cn/Record.Modify --header 'User-Agent: HostCreate/v0.1(lee-cq@qq.com)' \
    -d "login_token=${LOGIN_TOKEN}&format=json&domain=${DOMAIN}&sub_domain=ali-host&record_type=A&record_line_id=10%3D0&value=$(cat ecs-instanse-ip)"
```