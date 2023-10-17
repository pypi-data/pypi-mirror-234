# Autowork命令行工具
本地运行：安装命令工具
```shell
poetry install
```

进入poetry shell
```shell
poetry shell
```

启动工具
```shell
autowork --help 
```

# 操作系统全局安装
首先安装pipx
pip3 install pipx

再安装本地代码或者git库地址
pipx install ~/Git/finbot/autowork-cli

可能要重启终端才能生效
autowork --help

# 命令行颜色规范
- 蓝色：执行命令
- 绿色：成功消息
- 红色：失败消息

# 常用命令
```shell
poetry run autowork cf --help
```

```shell
poetry run autowork sidecar start
```

```shell
poetry run autowork sidecar status
```

本地调测请求
```shell
app_id="sf_example"
func_id="hello_world"

# JSON数据
json_data='{"name": "Jack"}'

# 发送POST请求
curl -X POST \
  -H "Content-Type: application/json" \
  -d "$json_data" \
  "http://localhost:9000/sandbox/call/$app_id/$func_id"
```

