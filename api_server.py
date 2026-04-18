"""HTTP API server for scientific plotting."""

import io
import json
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from core.plotter import PlotConfig, ScientificPlotter
from core.utils import auto_select_chart_type
from charts.architecture import (
    create_architecture_diagram,
    create_architecture_diagram_from_template,
    list_architecture_templates,
)

# Initialize FastAPI app
app = FastAPI(
    title="Scientific Plotting API",
    description="HTTP API for scientific data visualization and architecture diagrams",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize plotter
plotter = ScientificPlotter(enable_cache=True)


@app.get("/")
async def root():
    """Root endpoint with configuration guide."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scientific Plotting MCP Server</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; margin-top: 0; }
            h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            .config-box {
                background: #2c3e50;
                color: #ecf0f1;
                padding: 20px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                overflow-x: auto;
                position: relative;
            }
            .copy-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
            }
            .copy-btn:hover { background: #2980b9; }
            .warning {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }
            .links {
                display: flex;
                gap: 15px;
                margin: 30px 0;
            }
            .link-btn {
                flex: 1;
                text-align: center;
                padding: 15px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            .link-btn:hover { background: #2980b9; }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .feature {
                background: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 Scientific Plotting MCP Server</h1>
            <p>欢迎使用科研绘图MCP服务器！本服务提供强大的科学数据可视化和架构图绘制功能。</p>

            <h2>📋 MCP客户端配置</h2>
            <p>将以下配置添加到您的 Claude Desktop 配置文件中：</p>
            <div class="config-box">
                <button class="copy-btn" onclick="copyConfig()">复制</button>
                <pre id="config">{
  "mcpServers": {
    "scientific-plotting": {
      "url": "http://<span style="color:#f39c12">YOUR_AUTODL_URL</span>:6006",
      "transport": "http"
    }
  }
}</pre>
            </div>

            <div class="warning">
                <strong>⚠️ 注意：</strong>请将 <code>YOUR_AUTODL_URL</code> 替换为您的AutoDL实例公网地址（在AutoDL控制台的"自定义服务"中查看）
            </div>

            <h2>🚀 快速开始</h2>
            <div class="links">
                <a href="/docs" class="link-btn">📚 API文档</a>
                <a href="/health" class="link-btn">💚 健康检查</a>
            </div>

            <h2>✨ 主要功能</h2>
            <div class="features">
                <div class="feature">📊 统计图表</div>
                <div class="feature">📈 时间序列</div>
                <div class="feature">🔬 科学图表</div>
                <div class="feature">🤖 机器学习</div>
                <div class="feature">🏗️ 架构图</div>
                <div class="feature">📑 批量处理</div>
            </div>

            <h2>📖 API端点</h2>
            <ul>
                <li><code>POST /create_chart</code> - 创建图表</li>
                <li><code>POST /create_architecture</code> - 创建架构图</li>
                <li><code>POST /auto_chart</code> - 自动选择图表类型</li>
                <li><code>GET /list_chart_types</code> - 列出所有图表类型</li>
                <li><code>GET /docs</code> - 完整API文档</li>
            </ul>
        </div>

        <script>
            function copyConfig() {
                const config = document.getElementById('config').innerText;
                navigator.clipboard.writeText(config).then(() => {
                    const btn = document.querySelector('.copy-btn');
                    btn.textContent = '已复制!';
                    setTimeout(() => btn.textContent = '复制', 2000);
                });
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/create_chart")
async def create_chart(
    file: UploadFile = File(...),
    chart_type: str = Form(...),
    title: Optional[str] = Form(None),
    xlabel: Optional[str] = Form(None),
    ylabel: Optional[str] = Form(None),
    style: str = Form("default"),
    figsize_width: float = Form(10),
    figsize_height: float = Form(6),
    dpi: int = Form(300),
    format: str = Form("png"),
    interactive: bool = Form(False),
):
    """Create a chart from uploaded data file."""
    try:
        # Read uploaded file
        content = await file.read()

        # Determine file type and load data
        if file.filename.endswith('.csv'):
            data = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            data = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV, Excel, or JSON.")

        # Create plot config
        config = PlotConfig(
            chart_type=chart_type,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            style=style,
            figsize=(figsize_width, figsize_height),
            dpi=dpi,
            interactive=interactive,
        )

        # Create chart (pass DataFrame directly, not BytesIO)
        fig = plotter.create_chart(data, config)

        # Save to bytes
        buf = io.BytesIO()
        if interactive and format == "html":
            fig.fig.write_html(buf)
            media_type = "text/html"
        else:
            # Save matplotlib figure to BytesIO
            if hasattr(fig.fig, 'savefig'):
                fig.fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
            else:
                fig.save(buf, format=format, dpi=dpi)
            media_type = f"image/{format}"

        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=chart.{format}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_from_template")
async def create_from_template(
    file: UploadFile = File(...),
    template_name: str = Form(...),
    format: str = Form("png"),
    dpi: int = Form(300),
):
    """Create a chart from a predefined template."""
    try:
        # Read uploaded file
        content = await file.read()

        # Load data
        if file.filename.endswith('.csv'):
            data = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            data = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Create chart from template (pass DataFrame directly)
        fig = plotter.create_from_template(template_name, data)

        # Save to bytes
        buf = io.BytesIO()
        if hasattr(fig.fig, 'savefig'):
            fig.fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        else:
            fig.save(buf, format=format, dpi=dpi)
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type=f"image/{format}",
            headers={"Content-Disposition": f"attachment; filename=chart.{format}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auto_chart")
async def auto_chart(
    file: UploadFile = File(...),
    style: str = Form("default"),
    format: str = Form("png"),
    dpi: int = Form(300),
):
    """Automatically select and create appropriate chart based on data."""
    try:
        # Read uploaded file
        content = await file.read()

        # Load data
        if file.filename.endswith('.csv'):
            data = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            data = pd.read_excel(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            data = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Auto-select chart type
        chart_type = auto_select_chart_type(data)

        # Create config
        config = PlotConfig(chart_type=chart_type, style=style)

        # Create chart (pass DataFrame directly)
        fig = plotter.create_chart(data, config)

        # Save to bytes
        buf = io.BytesIO()
        if hasattr(fig.fig, 'savefig'):
            fig.fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        else:
            fig.save(buf, format=format, dpi=dpi)
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type=f"image/{format}",
            headers={
                "Content-Disposition": f"attachment; filename=chart.{format}",
                "X-Chart-Type": chart_type
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_architecture")
async def create_architecture(
    description: str = Form(...),
    figsize_width: float = Form(12),
    figsize_height: float = Form(8),
    style: str = Form("transformer"),
    dpi: int = Form(300),
    format: str = Form("pdf"),
):
    """Create architecture diagram from natural language or JSON description."""
    try:
        # Parse description if it's JSON
        try:
            desc = json.loads(description)
        except:
            desc = description

        # Create diagram
        fig = create_architecture_diagram(
            description=desc,
            figsize=(figsize_width, figsize_height),
            style=style,
            dpi=dpi,
            format=format,
        )

        # Save to bytes
        buf = io.BytesIO()
        fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type=f"image/{format}",
            headers={"Content-Disposition": f"attachment; filename=architecture.{format}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_architecture_from_template")
async def create_architecture_from_template(
    template_name: str = Form(...),
    figsize_width: float = Form(12),
    figsize_height: float = Form(8),
    dpi: int = Form(300),
    format: str = Form("pdf"),
    template_params: Optional[str] = Form(None),
):
    """Create architecture diagram from predefined template."""
    try:
        # Parse template params if provided
        params = {}
        if template_params:
            try:
                params = json.loads(template_params)
            except:
                raise HTTPException(status_code=400, detail="Invalid template_params JSON")

        # Create diagram
        fig = create_architecture_diagram_from_template(
            template_name=template_name,
            figsize=(figsize_width, figsize_height),
            output_path=None,
            dpi=dpi,
            **params,
        )

        # Save to bytes
        buf = io.BytesIO()
        fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        buf.seek(0)

        return StreamingResponse(
            buf,
            media_type=f"image/{format}",
            headers={"Content-Disposition": f"attachment; filename=architecture.{format}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list_chart_types")
async def list_chart_types():
    """List all available chart types."""
    return JSONResponse(content={
        "chart_types": plotter.list_chart_types()
    })


@app.get("/list_templates")
async def list_templates():
    """List all available templates."""
    return JSONResponse(content={
        "templates": plotter.list_templates()
    })


@app.get("/list_styles")
async def list_styles():
    """List all available styles."""
    return JSONResponse(content={
        "styles": plotter.list_styles()
    })


@app.get("/list_architecture_templates")
async def list_arch_templates():
    """List all available architecture templates."""
    return JSONResponse(content={
        "templates": list_architecture_templates()
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "scientific-plotting-api"}


if __name__ == "__main__":
    import uvicorn
    import os

    # Use port 6006 for AutoDL platform (Web UI port)
    port = int(os.getenv("PORT", 6006))

    # Get AutoDL instance URL from environment or use placeholder
    autodl_url = os.getenv("AUTODL_URL", "your-autodl-instance-url")

    print("\n" + "="*60)
    print("🎨 Scientific Plotting API Server")
    print("="*60)
    print(f"\n📡 Server: http://0.0.0.0:{port}")
    print(f"📚 API Docs: http://0.0.0.0:{port}/docs")
    print(f"💚 Health: http://0.0.0.0:{port}/health")
    print("\n" + "="*60)
    print("\n📋 MCP Configuration for Remote Client (Claude Desktop):")
    print(f"""
{{
  "mcpServers": {{
    "scientific-plotting": {{
      "url": "http://{autodl_url}:{port}",
      "transport": "http"
    }}
  }}
}}
""")
    print("⚠️  Replace '{autodl_url}' with your actual AutoDL instance URL")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=port)
