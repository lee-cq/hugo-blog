---

---

## 目标
编写一个简洁的Loki配置文件，要求：
1. 单一部署，(=target=all)
2. 使用本次磁盘作为存储(数据根目录：/opt/app/loki/data)
3. 监听在端口3100上
4. 使用简单的用户名密码认证(由Nginx实现，Loki不包含认证服务)


## 配置文件
```yaml
# loki-config.yaml

auth_enabled: false
server:
  http_listen_port: 3100

common:
  path_prefix: /opt/app/loki/data
  storage:
    filesystem:
      chunks_directory: /opt/app/loki/data/chunks
      rules_directory: /opt/app/loki/data/rules
  replication_factor: 1
  ring:
    instance_addr: localhost
    kvstore:
      store: inmemory

query_scheduler:
  # the TSDB index dispatches many more, but each individually smaller, requests.
  # We increase the pending request queue sizes to compensate.
  max_outstanding_requests_per_tenant: 32768

schema_config:
  configs:
    - from: 2000-07-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  filesystem:
    directory: /opt/app/loki/data
```

## 启动命令

单节点启动：`nohup loki-linux-amd64 -target=all -config.file=loki-config.yaml`
