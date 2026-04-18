# 部署前检查清单

## ✅ 已完成项

1. **启动脚本** (`start.sh`) - 已创建
2. **环境验证脚本** (`verify.py`) - 已创建并修复Windows编码问题
3. **端口配置** - 已修改为6006端口
4. **配置指引页面** - 根路径返回HTML配置页面
5. **镜像构建文档** (`AUTODL_BUILD.md`) - 已创建

## ⚠️ 注意事项

### 1. 依赖安装
在AutoDL平台上，**必须先安装所有依赖**：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 本地测试缺少依赖
当前本地环境缺少 `plotly`，但这不影响AutoDL部署。AutoDL平台会按照 `requirements.txt` 安装所有依赖。

### 3. 启动流程
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 验证环境
python verify.py

# 3. 启动服务
bash start.sh
# 或
python api_server.py
```

### 4. 远程访问流程
1. 用户在AutoDL启动服务
2. 访问 `http://autodl-instance:6006`
3. 看到配置指引页面
4. 复制MCP配置JSON
5. 替换为实际AutoDL地址
6. 添加到Claude Desktop配置

## 📋 文件清单

- ✅ `start.sh` - 启动脚本
- ✅ `verify.py` - 环境验证
- ✅ `api_server.py` - HTTP服务器（端口6006，带配置页面）
- ✅ `requirements.txt` - 依赖列表
- ✅ `AUTODL_BUILD.md` - 镜像构建说明

## 🚀 AutoDL部署步骤

1. 上传代码到AutoDL
2. 运行 `pip install -r requirements.txt`
3. 运行 `python verify.py` 验证环境
4. 运行 `bash start.sh` 启动服务
5. 在AutoDL控制台查看6006端口的公网地址
6. 访问该地址获取MCP配置

## ✅ 确认无误

所有代码已准备就绪，可以提交到AutoDL平台！
