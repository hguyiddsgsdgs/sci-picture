# Scientific Plotting MCP - User Guide

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run examples
python examples.py
```

### Basic Usage

```python
from core.plotter import ScientificPlotter, PlotConfig

# Initialize plotter
plotter = ScientificPlotter()

# Create a chart
config = PlotConfig(
    chart_type="sci_scatter_regression",
    title="My Chart",
    style="nature"
)

fig = plotter.create_chart("data.csv", config)
fig.save("output.png")
```

## Chart Types

### Statistical Charts

- `stat_boxplot` - Box plot for distribution comparison
- `stat_violin` - Violin plot with distribution shape
- `stat_distribution` - Histogram with KDE
- `stat_correlation_heatmap` - Correlation matrix heatmap
- `stat_pairplot` - Pairwise relationships

### Time Series Charts

- `ts_line` - Line chart for time series
- `ts_area` - Area chart with fill
- `ts_candlestick` - OHLC candlestick chart
- `ts_decomposition` - Seasonal decomposition

### Comparison Charts

- `comp_bar` - Simple bar chart
- `comp_grouped_bar` - Grouped bar chart
- `comp_stacked_bar` - Stacked bar chart
- `comp_radar` - Radar/spider chart

### Scientific Charts

- `sci_scatter_regression` - Scatter with regression line
- `sci_contour` - Contour plot
- `sci_3d_surface` - 3D surface plot
- `sci_vector_field` - Vector field plot

### ML/AI Charts

- `ml_confusion_matrix` - Confusion matrix heatmap
- `ml_roc_curve` - ROC curve with AUC
- `ml_learning_curve` - Training/validation curves
- `ml_feature_importance` - Feature importance bar chart
- `ml_precision_recall` - Precision-recall curve

## Styles

### Publication Styles

- `nature` - Nature journal style (8pt font, tight layout)
- `science` - Science journal style (7pt font)
- `ieee` - IEEE conference style (serif font)
- `acm` - ACM conference style
- `springer` - Springer journal style

### General Styles

- `default` - Standard matplotlib style
- `minimal` - Clean minimal style
- `colorblind` - Colorblind-friendly colors

## Templates

Templates provide pre-configured settings for common use cases:

```python
# Use a template
fig = plotter.create_from_template(
    "nature_figure",
    "data.csv",
    title="My Figure"
)
```

### Available Templates

**Statistical:**
- `boxplot_comparison` - Box plot comparison
- `distribution_analysis` - Distribution with KDE
- `correlation_matrix` - Correlation heatmap

**Time Series:**
- `timeseries_basic` - Basic time series
- `timeseries_forecast` - With confidence intervals

**Comparison:**
- `bar_comparison` - Bar chart with error bars
- `grouped_comparison` - Grouped bars
- `radar_comparison` - Radar chart

**Scientific:**
- `scatter_regression` - Scatter with regression
- `contour_plot` - Contour plot
- `surface_3d` - 3D surface

**ML/AI:**
- `confusion_matrix` - Confusion matrix
- `roc_curve` - ROC curve
- `learning_curve` - Learning curves
- `feature_importance` - Feature importance

**Publication:**
- `nature_figure` - Nature single column (3.5" × 3.5")
- `science_figure` - Science single column (3.3" × 2.5")
- `ieee_figure` - IEEE single column (3.5" × 2.5")

## Advanced Features

### Batch Processing

```python
# Process multiple files
output_paths = plotter.batch_create(
    data_list=["data1.csv", "data2.csv"],
    config_list=[config1, config2],
    output_dir="output",
    format="pdf"
)
```

### Auto Chart Selection

```python
from core.utils import auto_select_chart_type

# Automatically select appropriate chart
data = plotter.data_loader.load("data.csv")
chart_type = auto_select_chart_type(data)

config = PlotConfig(chart_type=chart_type)
fig = plotter.create_chart(data, config)
```

### Interactive Charts

```python
# Create interactive plotly chart
config = PlotConfig(
    chart_type="sci_scatter_regression",
    interactive=True
)

fig = plotter.create_chart("data.csv", config)
fig.save("output.html")  # Save as HTML
```

### Caching

```python
# Enable caching for faster re-rendering
plotter = ScientificPlotter(enable_cache=True)

# Clear cache
plotter.cache_manager.clear()
```

## Command-Line Interface

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

# Clear cache
python cli.py clear-cache
```

## MCP Server

Start the MCP server:

```bash
python server.py
```

The server provides these tools:
- `create_chart` - Create a chart
- `create_from_template` - Use a template
- `batch_create` - Batch processing
- `auto_chart` - Auto chart selection
- `list_chart_types` - List chart types
- `list_templates` - List templates
- `list_styles` - List styles

## Data Format Requirements

### Scatter Regression
- 2 columns: x, y

### Time Series
- Index: datetime
- Columns: values

### Candlestick
- Columns: Open, High, Low, Close

### Contour/3D Surface
- 3 columns: x, y, z

### Confusion Matrix
- 2 columns: y_true, y_pred

### ROC Curve
- 2 columns: y_true, y_score

### Feature Importance
- 2 columns: feature, importance

## Tips & Best Practices

1. **Publication Figures:**
   - Use `nature`, `science`, or `ieee` styles
   - Set appropriate DPI (300+ for print)
   - Use vector formats (PDF, SVG, EPS)

2. **Large Datasets:**
   - Enable caching for repeated operations
   - Use batch processing for multiple files
   - Consider downsampling for visualization

3. **Color Choices:**
   - Use `colorblind` style for accessibility
   - Avoid red-green combinations
   - Use sequential colormaps for continuous data

4. **Font Sizes:**
   - Nature: 8pt base
   - Science: 7pt base
   - IEEE: 8pt base
   - Adjust based on figure size

5. **Figure Sizes:**
   - Nature single column: 3.5" (89mm)
   - Nature double column: 7.0" (183mm)
   - Science single column: 3.3" (84mm)
   - IEEE single column: 3.5" (88mm)

## Troubleshooting

**Issue: Fonts not rendering correctly**
- Install required fonts (Arial, Helvetica, Times New Roman)
- Use `font.family` in custom styles

**Issue: Large file sizes**
- Use raster formats (PNG) instead of vector for complex plots
- Reduce DPI for screen display (100-150)
- Simplify plots (fewer data points, simpler styles)

**Issue: Slow rendering**
- Enable caching
- Use batch processing
- Reduce data resolution

**Issue: Memory errors**
- Process files in smaller batches
- Reduce figure DPI
- Close figures after saving

## Examples

See `examples.py` for comprehensive examples covering:
- Basic usage
- Templates
- Publication-ready figures
- ML/AI charts
- Interactive charts
- Batch processing
- Auto chart selection
