# Scientific Plotting MCP Server

A powerful Model Context Protocol (MCP) server for scientific data visualization and analysis.

## Features

### 📊 Chart Types
- **Statistical Plots**: Box plots, violin plots, distribution plots, correlation heatmaps
- **Time Series**: Line plots, area plots, candlestick charts
- **Comparison**: Bar charts, grouped bars, stacked bars, radar charts
- **Scientific**: Scatter plots with regression, contour plots, 3D surface plots
- **ML/AI**: Confusion matrix, ROC curves, learning curves, feature importance
- **Architecture Diagrams**: Neural network model architecture visualization with 3D effects
- **Publication**: High-quality figures with customizable styles (Nature, Science, IEEE)

### 🎨 Advanced Features
- **Template System**: Pre-configured templates for different publication venues
- **Batch Processing**: Process multiple datasets/experiments at once
- **Style Presets**: Academic, minimal, colorblind-friendly palettes
- **Export Formats**: PNG, PDF, SVG, EPS (publication-ready)
- **Interactive**: Plotly-based interactive charts with zoom, pan, hover
- **Statistical Analysis**: Built-in statistical tests and annotations
- **Experiment Tracking**: Compare multiple experiments with metrics
- **Cache System**: Fast re-rendering with intelligent caching
- **Architecture Visualization**: 3D model diagrams with natural language or JSON input
- **Pre-built Templates**: Transformer, BERT, GPT, ViT, ResNet, and more

### 🔧 Technical Advantages
- **Flexible Input**: CSV, JSON, Pickle, HDF5, Excel
- **Smart Defaults**: Automatic layout optimization
- **Type Safety**: Full type hints and validation
- **Extensible**: Easy to add custom chart types
- **Performance**: Optimized for large datasets
- **Memory Efficient**: Streaming support for big data

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### As MCP Server
```bash
python server.py
```

### As Python Library

#### Data Visualization
```python
from core.plotter import ScientificPlotter, PlotConfig

plotter = ScientificPlotter()
config = PlotConfig(chart_type="scatter_regression", style="nature")
fig = plotter.create_chart(data=df, config=config)
fig.save("output.pdf")
```

#### Architecture Diagrams
```python
from charts.architecture import create_architecture_diagram

# Natural language input
fig = create_architecture_diagram("""
    A Transformer Encoder with 6 layers.
    Multi-Head Attention with 8 heads.
    Feed-Forward Network with 2048 hidden units.
""")
fig.savefig("architecture.pdf", dpi=300)

# Or use templates
from charts.architecture import create_transformer_diagram
fig = create_transformer_diagram(num_layers=6, d_model=512, num_heads=8)
```

## Project Structure

```
picture/
├── server.py              # MCP server entry point
├── core/
│   ├── plotter.py        # Main plotting engine
│   ├── styles.py         # Style configurations
│   ├── templates.py      # Chart templates
│   └── utils.py          # Utility functions
├── charts/
│   ├── statistical.py    # Statistical charts
│   ├── timeseries.py     # Time series charts
│   ├── comparison.py     # Comparison charts
│   ├── scientific.py     # Scientific charts
│   └── ml.py            # ML/AI specific charts
├── analysis/
│   ├── statistics.py     # Statistical analysis
│   ├── metrics.py        # Metrics calculation
│   └── comparison.py     # Experiment comparison
├── export/
│   └── formats.py        # Export handlers
└── tests/
    └── test_plotter.py   # Unit tests
```

## License

MIT License
