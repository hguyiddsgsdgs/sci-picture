# HTTP API 使用指南

## 启动服务

### 方式1：直接启动
```bash
python3 api_server.py
```

### 方式2：使用uvicorn（推荐生产环境）
```bash
# 开发模式（自动重载）
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

# 生产模式
uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

### 方式3：后台运行
```bash
nohup python3 api_server.py > api_server.log 2>&1 &
```

服务启动后访问：`http://服务器IP:8000`

## API文档

启动服务后，访问自动生成的交互式文档：
- Swagger UI: `http://服务器IP:8000/docs`
- ReDoc: `http://服务器IP:8000/redoc`

## API接口

### 1. 健康检查
```bash
curl http://服务器IP:8000/health
```

### 2. 列出可用选项
```bash
# 列出图表类型
curl http://服务器IP:8000/list_chart_types

# 列出模板
curl http://服务器IP:8000/list_templates

# 列出样式
curl http://服务器IP:8000/list_styles

# 列出架构模板
curl http://服务器IP:8000/list_architecture_templates
```

### 3. 创建图表
```bash
curl -X POST "http://服务器IP:8000/create_chart" \
  -F "file=@data.csv" \
  -F "chart_type=sci_scatter_regression" \
  -F "title=My Chart" \
  -F "style=nature" \
  -F "format=png" \
  -o output.png
```

### 4. 使用模板创建图表
```bash
curl -X POST "http://服务器IP:8000/create_from_template" \
  -F "file=@data.csv" \
  -F "template_name=nature_figure" \
  -F "format=pdf" \
  -o output.pdf
```

### 5. 自动选择图表类型
```bash
curl -X POST "http://服务器IP:8000/auto_chart" \
  -F "file=@data.csv" \
  -F "style=default" \
  -F "format=png" \
  -o output.png
```

### 6. 创建架构图
```bash
curl -X POST "http://服务器IP:8000/create_architecture" \
  -F "description=A Transformer with 6 layers" \
  -F "style=transformer" \
  -F "format=pdf" \
  -o architecture.pdf
```

### 7. 使用模板创建架构图
```bash
curl -X POST "http://服务器IP:8000/create_architecture_from_template" \
  -F "template_name=transformer_encoder" \
  -F "template_params={\"num_layers\":6,\"d_model\":512}" \
  -F "format=pdf" \
  -o architecture.pdf
```

## Python客户端示例

```python
import requests

# 创建图表
url = "http://服务器IP:8000/create_chart"
files = {'file': open('data.csv', 'rb')}
data = {
    'chart_type': 'sci_scatter_regression',
    'title': 'My Chart',
    'style': 'nature',
    'format': 'png'
}

response = requests.post(url, files=files, data=data)
with open('output.png', 'wb') as f:
    f.write(response.content)
```

## 测试

运行测试脚本：
```bash
# 先启动服务
python3 api_server.py

# 在另一个终端运行测试
python3 test_api.py
```

## 防火墙设置

```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## 与MCP服务器的区别

| 特性 | MCP服务器 (server.py) | HTTP API (api_server.py) |
|------|---------------------|------------------------|
| 通信方式 | stdio | HTTP |
| 访问方式 | 本地配置JSON | 网络端口访问 |
| 客户端 | Claude Desktop等MCP客户端 | 任何HTTP客户端 |
| 使用场景 | 本地AI助手集成 | 远程服务调用 |

**两者可以同时运行，互不影响！**
