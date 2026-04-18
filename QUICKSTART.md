# Quick Start Guide

## Installation

```bash
cd C:/download/agent/MCP/picture
pip install -r requirements.txt
```

## 5-Minute Tutorial

### 1. Create Your First Chart (30 seconds)

```python
from core.plotter import ScientificPlotter, PlotConfig
import pandas as pd
import numpy as np

# Create sample data
data = pd.DataFrame({
    'x': np.linspace(0, 10, 50),
    'y': np.linspace(0, 10, 50) + np.random.randn(50)
})

# Create plotter
plotter = ScientificPlotter()

# Create chart
config = PlotConfig(
    chart_type="sci_scatter_regression",
    title="My First Chart",
    style="nature"
)

fig = plotter.create_chart(data, config)
fig.save("my_first_chart.png")
```

### 2. Use a Template (15 seconds)

```python
# Even simpler with templates
fig = plotter.create_from_template(
    "scatter_regression",
    data,
    title="Using Template"
)
fig.save("template_chart.png")
```

### 3. Auto Chart Selection (10 seconds)

```python
from core.utils import auto_select_chart_type

# Let the library choose the best chart
chart_type = auto_select_chart_type(data)
config = PlotConfig(chart_type=chart_type)
fig = plotter.create_chart(data, config)
fig.save("auto_chart.png")
```

### 4. Publication-Ready Figure (20 seconds)

```python
# Create Nature journal style figure
fig = plotter.create_from_template(
    "nature_figure",
    data,
    title="Publication Ready"
)
fig.save("nature_figure.pdf", format="pdf", dpi=300)
```

### 5. Interactive Chart (15 seconds)

```python
# Create interactive plotly chart
config = PlotConfig(
    chart_type="sci_scatter_regression",
    interactive=True
)
fig = plotter.create_chart(data, config)
fig.save("interactive.html")
# Open interactive.html in browser
```

## Common Tasks

### Load Data from File

```python
# Supports CSV, Excel, JSON, HDF5, Parquet, Pickle
fig = plotter.create_chart("data.csv", config)
```

### Batch Processing

```python
# Process multiple files at once
output_paths = plotter.batch_create(
    data_list=["data1.csv", "data2.csv", "data3.csv"],
    config_list=[config1, config2, config3],
    output_dir="output",
    format="png"
)
```

### ML/AI Charts

```python
# Confusion Matrix
config = PlotConfig(
    chart_type="ml_confusion_matrix",
    style="minimal"
)

# ROC Curve
config = PlotConfig(
    chart_type="ml_roc_curve",
    style="nature"
)

# Feature Importance
config = PlotConfig(
    chart_type="ml_feature_importance",
    extra_kwargs={"top_n": 20, "horizontal": True}
)
```

### Time Series

```python
# Time series data (index must be datetime)
dates = pd.date_range('2023-01-01', periods=100)
ts_data = pd.DataFrame({'value': np.random.randn(100)}, index=dates)

config = PlotConfig(chart_type="ts_line")
fig = plotter.create_chart(ts_data, config)
```

## Command Line Usage

```bash
# Create a chart
python cli.py create data.csv --type sci_scatter_regression --output chart.png

# Use a template
python cli.py template data.csv --template nature_figure --output fig.pdf

# Auto-select chart type
python cli.py auto data.csv --output chart.png

# List available options
python cli.py list-types
python cli.py list-templates
python cli.py list-styles

# Batch processing
python cli.py batch data_dir/ --type comp_bar --output-dir output/
```

## MCP Server

```bash
# Start the server
python server.py

# The server provides these tools:
# - create_chart
# - create_from_template
# - batch_create
# - auto_chart
# - list_chart_types
# - list_templates
# - list_styles
```

## Run Examples

```bash
# Run all examples
python examples.py

# Check output in examples/output/
```

## Next Steps

1. **Read the User Guide**: See `GUIDE.md` for comprehensive documentation
2. **Explore Templates**: Run `python cli.py list-templates`
3. **Try Different Styles**: Run `python cli.py list-styles`
4. **Check Examples**: Look at `examples.py` for more use cases
5. **Read Comparison**: See `COMPARISON.md` to understand advantages

## Troubleshooting

**Import Error:**
```bash
pip install -r requirements.txt
```

**Font Warning:**
- Install Arial, Helvetica, or Times New Roman fonts
- Or use `style="default"` which uses system fonts

**Memory Error:**
- Reduce figure DPI: `dpi=150`
- Process files in smaller batches
- Enable caching: `ScientificPlotter(enable_cache=True)`

## Getting Help

- **User Guide**: `GUIDE.md`
- **Examples**: `examples.py`
- **Tests**: `tests/test_plotter.py`
- **Comparison**: `COMPARISON.md`

## Key Concepts

1. **PlotConfig**: Configuration object for charts
2. **Templates**: Pre-configured settings for common tasks
3. **Styles**: Publication-ready styling presets
4. **Backends**: Matplotlib (static) or Plotly (interactive)
5. **Caching**: Automatic performance optimization

## Tips

- Use templates for quick results
- Use styles for publication-ready figures
- Enable caching for repeated operations
- Use batch processing for multiple files
- Use interactive mode for exploration
- Use PDF/SVG for publications
- Use PNG for presentations
- Use HTML for web sharing

Enjoy creating beautiful scientific visualizations! 📊
