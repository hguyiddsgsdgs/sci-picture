# 镜像构建

## 基本环境

- **框架及版本**: Python 3.9+, FastAPI 0.104.0+, MCP 1.0.0+
- **CUDA版本**: 无需CUDA（纯CPU计算即可，如需GPU加速可选CUDA 11.8+）

## 构建过程

### 代码Clone

```bash
cd /root
git clone https://github.com/your-username/Sci-drawing.git
cd Sci-drawing
```

### 依赖安装

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**依赖列表** (`requirements.txt`):
```
# Core dependencies
mcp>=1.0.0
pandas>=2.0.0
numpy>=1.24.0

# Plotting libraries
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0
kaleido>=0.2.1

# Scientific computing
scipy>=1.10.0
scikit-learn>=1.3.0

# Data handling
openpyxl>=3.1.0
tables>=3.8.0
pyarrow>=12.0.0

# Utilities
pydantic>=2.0.0
typer>=0.9.0
rich>=13.0.0
tqdm>=4.65.0

# Optional
networkx>=3.1
pillow>=10.0.0

# HTTP API server
fastapi>=0.104.0
uvicorn>=0.24.0
```

## 环境验证代码

### 步骤1: 检查依赖安装

执行命令: 
```bash
python verify.py
```

**预期输出**:
```
============================================================
🔍 Scientific Plotting MCP - Environment Verification
============================================================

🐍 Python Version: 3.9.x

📦 Core Dependencies:
✅ MCP: 1.0.0
✅ Pandas: 2.0.0
✅ NumPy: 1.24.0
✅ Matplotlib: 3.7.0
✅ Seaborn: 0.12.0
✅ Plotly: 5.14.0
✅ SciPy: 1.10.0
✅ Scikit-learn: 1.3.0
✅ FastAPI: 0.104.0
✅ Uvicorn: 0.24.0
✅ Pydantic: 2.0.0

============================================================
✅ All dependencies installed successfully!

🚀 Ready to start the server:
   bash start.sh

   or

   python api_server.py
```

### 步骤2: 执行功能测试（审核必需）

执行命令:
```bash
python test_env.py
```

**预期输出**:
```
============================================================
Scientific Plotting MCP - Environment Test
============================================================

Test 1: Importing core modules...
  ✓ All core modules imported successfully

Test 2: Creating plotter instance...
  ✓ Plotter instance created

Test 3: Generating test data...
  ✓ Test data generated

Test 4: Creating a simple chart...
  ✓ Chart created and saved to test_output/env_test.png

Test 5: Testing API server...
  ✓ API server can be imported

Test 6: Checking available features...
  ✓ 15 chart types available
  ✓ 8 templates available
  ✓ 5 styles available

============================================================
✓ All tests passed! Environment is properly configured.
============================================================
```

**说明**: 此测试脚本会实际运行代码并生成图表，证明环境配置正确且代码可以正常执行。

## 启动命令

```bash
bash start.sh
```

或直接运行:
```bash
python api_server.py
```

**服务端口**: 6006 (AutoDL平台Web UI端口)

**启动后输出**:
```
==========================================================
🎨 Scientific Plotting API Server
==========================================================

📡 Server: http://0.0.0.0:6006
📚 API Docs: http://0.0.0.0:6006/docs
💚 Health: http://0.0.0.0:6006/health

==========================================================

📋 MCP Configuration for Remote Client (Claude Desktop):

{
  "mcpServers": {
    "scientific-plotting": {
      "url": "http://your-autodl-instance-url:6006",
      "transport": "http"
    }
  }
}

⚠️  Replace 'your-autodl-instance-url' with your actual AutoDL instance URL

==========================================================
```

## 使用说明

### HTTP API访问
- 访问 `http://your-autodl-instance:6006/docs` 查看交互式API文档
- 健康检查: `http://your-autodl-instance:6006/health`

### MCP客户端配置
将上述JSON配置添加到Claude Desktop的配置文件中，即可通过MCP协议调用科研绘图功能。

### 主要功能
- 📊 统计图表：箱线图、小提琴图、分布图、相关性热图
- 📈 时间序列：折线图、面积图、K线图
- 🔬 科学图表：散点回归图、等高线图、3D曲面图
- 🤖 机器学习：混淆矩阵、ROC曲线、学习曲线、特征重要性
- 🏗️ 架构图：神经网络模型架构可视化（支持自然语言描述）
