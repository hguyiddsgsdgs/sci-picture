# Architecture Diagram Visualization Guide

## Overview

The Scientific Plotting MCP Server now includes **neural network architecture diagram generation** with publication-quality 3D effects, similar to top-tier conference papers (Transformer, BERT, GPT, etc.).

## Features

✅ **Natural Language Input** - Describe your model in plain English  
✅ **JSON Input** - Precise control with structured descriptions  
✅ **Pre-built Templates** - 10+ common architectures ready to use  
✅ **3D Effects** - Professional 3D boxes, gradients, and textures  
✅ **Multiple Styles** - Transformer, Multi-modal, Modern, Academic  
✅ **Publication Ready** - PDF/PNG/SVG output at 300+ DPI  

## Quick Start

### Method 1: Natural Language

```python
from charts.architecture import create_architecture_diagram

description = """
A Transformer Encoder with 6 layers.
Input: [batch, seq_len, 512]
Each layer has Multi-Head Attention with 8 heads
and Feed-Forward Network with 2048 hidden units.
"""

fig = create_architecture_diagram(description)
fig.savefig("transformer.pdf", dpi=300)
```

### Method 2: JSON Description

```python
description = {
    "name": "Vision Transformer",
    "style": "transformer",
    "layers": [
        {
            "name": "Patch Embedding",
            "type": "embedding",
            "input_shape": "224×224×3",
            "output_shape": "196×768",
            "color": "#DDA0DD"
        },
        {
            "name": "Transformer Encoder",
            "type": "attention",
            "details": {"layers": 12, "heads": 12},
            "params": "85M",
            "color": "#87CEEB"
        },
        {
            "name": "Classification Head",
            "type": "linear",
            "output_shape": "1000",
            "color": "#98FB98"
        }
    ]
}

fig = create_architecture_diagram(description)
fig.savefig("vit.pdf", dpi=300)
```

### Method 3: Pre-built Templates

```python
from charts.architecture import create_transformer_diagram

fig = create_transformer_diagram(
    num_layers=6,
    d_model=512,
    num_heads=8,
    d_ff=2048,
    figsize=(10, 14),
    output_path="transformer.pdf"
)
```

## Available Templates

```python
from charts.architecture import list_architecture_templates

templates = list_architecture_templates()
# Returns:
# - transformer_encoder
# - transformer_decoder
# - cross_attention
# - self_attention
# - resnet_block
# - vit (Vision Transformer)
# - bert_layer
# - gpt_decoder
# - multimodal_fusion
# - deformable_conv
```

## Template Examples

### Transformer Encoder

```python
from charts.architecture import create_transformer_diagram

fig = create_transformer_diagram(
    num_layers=6,
    d_model=512,
    num_heads=8,
    d_ff=2048,
    encoder=True
)
```

### Vision Transformer

```python
from charts.architecture import create_vit_diagram

fig = create_vit_diagram(
    patch_size=16,
    d_model=768,
    num_layers=12,
    num_heads=12
)
```

### Multi-Modal Fusion

```python
from charts.architecture import create_multimodal_diagram

fig = create_multimodal_diagram(
    d_text=512,
    d_image=2048,
    d_fusion=768
)
```

### ResNet Block

```python
from charts.architecture import create_resnet_diagram

fig = create_resnet_diagram(channels=64)
```

### Cross-Attention (Multi-Modal)

```python
from charts.architecture import create_architecture_diagram_from_template

fig = create_architecture_diagram_from_template(
    "cross_attention",
    d_model=512,
    num_heads=8
)
```

## Visual Styles

### Transformer Style (Default)
- Blue-green gradient colors
- Clean, modern look
- Best for: Attention mechanisms, Transformer models

### Multi-Modal Style
- Gold (text) + Sky blue (image) + Green (fusion)
- Distinct modality colors
- Best for: Multi-modal architectures, cross-attention

### Modern Style
- Purple-blue gradient
- Contemporary design
- Best for: CNNs, ResNets, modern architectures

### Academic Style
- Deep blue professional colors
- Nature/Science journal aesthetic
- Best for: Publication figures

## Customization

### Layer Types and Colors

```python
description = {
    "name": "Custom Model",
    "layers": [
        {"name": "Input", "type": "input", "color": "#87CEEB"},
        {"name": "Conv", "type": "conv", "color": "#98FB98"},
        {"name": "Attention", "type": "attention", "color": "#FFD700"},
        {"name": "FFN", "type": "ffn", "color": "#DDA0DD"},
        {"name": "Output", "type": "output", "color": "#FFB6C1"}
    ]
}
```

### Layout Options

```python
description = {
    "name": "My Model",
    "layout": "vertical",  # or "horizontal", "hierarchical"
    "layers": [...]
}
```

### Adding Annotations

```python
description = {
    "name": "My Model",
    "layers": [...],
    "annotations": {
        "note": "Custom architecture for X task",
        "highlight": ["Attention Layer"]
    }
}
```

## Advanced Features

### 3D Visualization

For input/output feature maps, add 3D effects:

```python
{
    "name": "Image Features",
    "type": "input",
    "input_shape": "[H, W, C]",
    "details": {
        "3d": True,
        "texture": "grid"  # or "diagonal", "gradient"
    }
}
```

### Custom Connections

```python
description = {
    "name": "Model with Skip Connections",
    "layers": [
        {"name": "Layer1", "type": "conv"},
        {"name": "Layer2", "type": "conv"},
        {"name": "Layer3", "type": "conv"}
    ],
    "connections": [
        {"from": "Layer1", "to": "Layer2"},
        {"from": "Layer2", "to": "Layer3"},
        {"from": "Layer1", "to": "Layer3", "style": "curved", "label": "skip"}
    ]
}
```

## Output Formats

```python
# PDF (vector, best for papers)
fig.savefig("model.pdf", dpi=300, bbox_inches='tight')

# PNG (raster, high quality)
fig.savefig("model.png", dpi=300, bbox_inches='tight')

# SVG (editable vector)
fig.savefig("model.svg", bbox_inches='tight')
```

## Complete Example

```python
from charts.architecture import create_architecture_diagram

# Define a custom multi-modal architecture
description = {
    "name": "Multi-Modal Transformer",
    "style": "multimodal",
    "layout": "hierarchical",
    "layers": [
        {
            "name": "Text Encoder",
            "type": "input",
            "output_shape": "[seq_len, 512]",
            "color": "#FFD700",
            "details": {"texture": "diagonal"}
        },
        {
            "name": "Image Encoder",
            "type": "input",
            "output_shape": "[196, 768]",
            "color": "#87CEEB",
            "details": {"texture": "grid", "3d": True}
        },
        {
            "name": "Cross-Attention",
            "type": "attention",
            "details": {"heads": 8},
            "color": "#98FB98"
        },
        {
            "name": "Fusion Layer",
            "type": "ffn",
            "params": "2M",
            "color": "#F0E68C"
        },
        {
            "name": "Classification",
            "type": "output",
            "output_shape": "num_classes",
            "color": "#FFB6C1"
        }
    ],
    "connections": [
        {"from": "Text Encoder", "to": "Cross-Attention", "label": "K,V"},
        {"from": "Image Encoder", "to": "Cross-Attention", "label": "Q"},
        {"from": "Cross-Attention", "to": "Fusion Layer"},
        {"from": "Fusion Layer", "to": "Classification"}
    ]
}

# Create diagram
fig = create_architecture_diagram(
    description,
    figsize=(12, 10)
)

# Save
fig.savefig("multimodal_transformer.pdf", dpi=300, bbox_inches='tight')
```

## Tips for Best Results

1. **Use descriptive layer names** - "Multi-Head Attention (8 heads)" is better than "Attention"
2. **Include dimensions** - Show input/output shapes for clarity
3. **Add parameter counts** - Helps readers understand model size
4. **Choose appropriate colors** - Use the color schemes that match your paper style
5. **Keep it simple** - For large models, use abstraction (e.g., "× 12 layers")
6. **Test different layouts** - Try vertical, horizontal, and hierarchical
7. **Export as PDF** - Vector format is best for papers

## Troubleshooting

### Import Error
If you get import errors, make sure you're importing from the correct module:

```python
# Correct
from charts.architecture import create_architecture_diagram

# Not from core or other modules
```

### Layout Issues
If layers overlap, try:
- Increasing `figsize`
- Changing `layout` parameter
- Reducing number of layers shown

### Color Not Showing
Make sure to specify colors in hex format:
```python
"color": "#87CEEB"  # Correct
"color": "skyblue"  # May not work
```

## Examples Directory

Run the examples to see all features:

```bash
python examples_architecture.py
```

This will generate 10 example diagrams in the `output/` directory.

## Integration with Existing Features

The architecture visualization is fully integrated with the existing MCP server:

```python
# You can still use all existing data visualization features
from core.plotter import ScientificPlotter, PlotConfig

# Data visualization
plotter = ScientificPlotter()
fig = plotter.create_chart("data.csv", PlotConfig(chart_type="ml_learning_curve"))

# Architecture visualization
from charts.architecture import create_transformer_diagram
fig = create_transformer_diagram(num_layers=6)
```

Both features work independently without conflicts!
