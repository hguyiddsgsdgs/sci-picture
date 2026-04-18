# Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Scientific Plotting MCP                           │
│                              v1.0.0                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           User Interfaces                                │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│   Python API    │   MCP Server    │   CLI Tool      │   Examples       │
│   (Direct)      │   (Remote)      │   (Command)     │   (Tutorial)     │
└────────┬────────┴────────┬────────┴────────┬────────┴────────┬─────────┘
         │                 │                 │                 │
         └─────────────────┴─────────────────┴─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Core Plotter Engine                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ScientificPlotter                                                       │
│  ├─ create_chart()          : Create chart from config                  │
│  ├─ create_from_template()  : Use predefined template                   │
│  ├─ batch_create()          : Process multiple charts                   │
│  └─ auto_select()           : Smart chart type selection                │
└────────┬────────────────────────────────────────────────────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┬──────────────┐
         ▼              ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Style      │ │   Template   │ │   Data       │ │   Cache      │ │   Utils      │
│   Manager    │ │   Manager    │ │   Loader     │ │   Manager    │ │   Module     │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│ • Nature     │ │ • Statistical│ │ • CSV        │ │ • Hash-based │ │ • Validation │
│ • Science    │ │ • TimeSeries │ │ • Excel      │ │ • Intelligent│ │ • Type Infer │
│ • IEEE       │ │ • Comparison │ │ • JSON       │ │ • Fast       │ │ • Auto Select│
│ • ACM        │ │ • Scientific │ │ • HDF5       │ │ • Persistent │ │ • Helpers    │
│ • Springer   │ │ • ML/AI      │ │ • Parquet    │ │              │ │              │
│ • Minimal    │ │ • Publication│ │ • Pickle     │ │              │ │              │
│ • Colorblind │ │              │ │              │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
         │              │              │              │              │
         └──────────────┴──────────────┴──────────────┴──────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Chart Implementations                            │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│ Statistical  │ Time Series  │ Comparison   │ Scientific   │   ML/AI    │
├──────────────┼──────────────┼──────────────┼──────────────┼────────────┤
│ • Boxplot    │ • Line       │ • Bar        │ • Scatter    │ • Confusion│
│ • Violin     │ • Area       │ • Grouped    │ • Contour    │ • ROC      │
│ • Distrib.   │ • Candlestick│ • Stacked    │ • 3D Surface │ • Learning │
│ • Corr. Heat │ • Decompose  │ • Radar      │ • Vector     │ • Feature  │
│ • Pairplot   │              │              │              │ • Precision│
└──────────────┴──────────────┴──────────────┴──────────────┴────────────┘
         │              │              │              │              │
         └──────────────┴──────────────┴──────────────┴──────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Rendering Backends                               │
├─────────────────────────────────┬───────────────────────────────────────┤
│         Matplotlib              │            Plotly                     │
├─────────────────────────────────┼───────────────────────────────────────┤
│ • Static figures                │ • Interactive charts                  │
│ • Publication quality           │ • Web-based                           │
│ • Vector formats (PDF, SVG, EPS)│ • Zoom, pan, hover                    │
│ • Raster formats (PNG, JPG)     │ • HTML export                         │
│ • High DPI support              │ • Responsive design                   │
└─────────────────────────────────┴───────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Output Formats                                │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────────────┤
│   PNG    │   PDF    │   SVG    │   EPS    │   HTML   │   Interactive   │
│ (Raster) │ (Vector) │ (Vector) │ (Vector) │  (Web)   │   (Plotly)      │
└──────────┴──────────┴──────────┴──────────┴──────────┴─────────────────┘
```

## Data Flow

```
┌──────────────┐
│  User Input  │
│  (Data Path) │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│   Data Loader    │
│  • Auto-detect   │
│  • Parse format  │
│  • Validate      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Type Inference  │
│  • Column types  │
│  • Relationships │
│  • Dimensions    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐     ┌──────────────────┐
│  Auto Selection  │────▶│  User Config     │
│  (Optional)      │     │  (Override)      │
└──────┬───────────┘     └────────┬─────────┘
       │                          │
       └──────────┬───────────────┘
                  │
                  ▼
┌──────────────────────────────────┐
│         Cache Check              │
│  Hash(data + config) → Cache?   │
└──────┬───────────────────┬───────┘
       │ Hit               │ Miss
       ▼                   ▼
┌──────────────┐    ┌──────────────────┐
│ Return Cache │    │  Apply Style     │
└──────────────┘    └──────┬───────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Create Chart    │
                    │  (Backend)       │
                    └──────┬───────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Apply Layout    │
                    │  • Title         │
                    │  • Labels        │
                    │  • Legend        │
                    │  • Grid          │
                    └──────┬───────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Cache Result    │
                    └──────┬───────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Return Figure   │
                    └──────┬───────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │  Save to File    │
                    │  (Format)        │
                    └──────────────────┘
```

## Component Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                      ScientificPlotter                           │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │   Style    │  │  Template  │  │    Data    │  │  Cache   │ │
│  │  Manager   │  │  Manager   │  │   Loader   │  │ Manager  │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └────┬─────┘ │
│        │               │               │              │        │
│        └───────────────┴───────────────┴──────────────┘        │
│                            │                                    │
│                            ▼                                    │
│                    ┌───────────────┐                           │
│                    │  Chart Router │                           │
│                    └───────┬───────┘                           │
│                            │                                    │
│        ┌───────────────────┼───────────────────┐              │
│        │                   │                   │              │
│        ▼                   ▼                   ▼              │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│  │Statistical│      │TimeSeries│      │Comparison│           │
│  └──────────┘      └──────────┘      └──────────┘           │
│        │                   │                   │              │
│        └───────────────────┼───────────────────┘              │
│                            │                                    │
│        ┌───────────────────┼───────────────────┐              │
│        │                   │                   │              │
│        ▼                   ▼                   ▼              │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│  │Scientific│      │   ML/AI  │      │  Custom  │           │
│  └──────────┘      └──────────┘      └──────────┘           │
│        │                   │                   │              │
│        └───────────────────┴───────────────────┘              │
│                            │                                    │
│                            ▼                                    │
│                    ┌───────────────┐                           │
│                    │Backend Selector│                          │
│                    └───────┬───────┘                           │
│                            │                                    │
│                ┌───────────┴───────────┐                       │
│                │                       │                       │
│                ▼                       ▼                       │
│        ┌──────────────┐       ┌──────────────┐               │
│        │  Matplotlib  │       │    Plotly    │               │
│        └──────────────┘       └──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Extension Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    Extension Architecture                        │
└─────────────────────────────────────────────────────────────────┘

1. Add New Chart Type
   ┌──────────────────────────────────────────────────────────┐
   │ charts/custom.py                                          │
   │                                                           │
   │ def create_custom_chart(ax, data, config):               │
   │     # Your implementation                                │
   │     pass                                                  │
   │                                                           │
   │ def create_custom_chart_plotly(data, config):            │
   │     # Your plotly implementation                         │
   │     pass                                                  │
   └──────────────────────────────────────────────────────────┘

2. Add New Style
   ┌──────────────────────────────────────────────────────────┐
   │ core/styles.py                                            │
   │                                                           │
   │ style_manager.create_custom_style("my_style", {          │
   │     "font.size": 10,                                     │
   │     "axes.linewidth": 1.0,                               │
   │     # ... more settings                                  │
   │ })                                                        │
   └──────────────────────────────────────────────────────────┘

3. Add New Template
   ┌──────────────────────────────────────────────────────────┐
   │ core/templates.py                                         │
   │                                                           │
   │ template_manager.add_template("my_template",             │
   │     PlotConfig(                                          │
   │         chart_type="custom_chart",                       │
   │         style="my_style",                                │
   │         # ... more config                                │
   │     )                                                     │
   │ )                                                         │
   └──────────────────────────────────────────────────────────┘

4. Add New Data Format
   ┌──────────────────────────────────────────────────────────┐
   │ core/utils.py                                             │
   │                                                           │
   │ class DataLoader:                                         │
   │     def load(self, path):                                │
   │         if path.suffix == '.custom':                     │
   │             return self._load_custom(path)               │
   │         # ... existing formats                           │
   └──────────────────────────────────────────────────────────┘
```

## Performance Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│                    Performance Strategy                          │
└─────────────────────────────────────────────────────────────────┘

1. Caching Layer
   ┌──────────────────────────────────────────────────────────┐
   │ Hash(data + config) → Cache Key                          │
   │                                                           │
   │ First Render:  ~2.0s                                     │
   │ Cached Render: ~0.1s (20x faster)                        │
   └──────────────────────────────────────────────────────────┘

2. Batch Processing
   ┌──────────────────────────────────────────────────────────┐
   │ Sequential: N × 2s = 20s (for 10 charts)                │
   │ Batch:      15s (25% faster)                             │
   │ Parallel:   8s (60% faster) [planned v1.1]              │
   └──────────────────────────────────────────────────────────┘

3. Memory Management
   ┌──────────────────────────────────────────────────────────┐
   │ • Streaming data loading                                 │
   │ • Automatic figure cleanup                               │
   │ • Lazy template loading                                  │
   │ • Cache size limits                                      │
   └──────────────────────────────────────────────────────────┘

4. Smart Defaults
   ┌──────────────────────────────────────────────────────────┐
   │ • Auto DPI selection (screen vs. print)                  │
   │ • Adaptive figure sizing                                 │
   │ • Intelligent downsampling                               │
   │ • Format-specific optimization                           │
   └──────────────────────────────────────────────────────────┘
```

## Security Considerations

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Measures                             │
└─────────────────────────────────────────────────────────────────┘

1. Input Validation
   ┌──────────────────────────────────────────────────────────┐
   │ • Pydantic models for type checking                      │
   │ • Path validation (no directory traversal)               │
   │ • File size limits                                       │
   │ • Format whitelist                                       │
   └──────────────────────────────────────────────────────────┘

2. Resource Limits
   ┌──────────────────────────────────────────────────────────┐
   │ • Maximum figure size                                    │
   │ • Cache size limits                                      │
   │ • Timeout for long operations                            │
   │ • Memory usage monitoring                                │
   └──────────────────────────────────────────────────────────┘

3. Safe Execution
   ┌──────────────────────────────────────────────────────────┐
   │ • No eval() or exec()                                    │
   │ • Sandboxed data loading                                 │
   │ • Safe pickle handling                                   │
   │ • Error handling and logging                             │
   └──────────────────────────────────────────────────────────┘
```
