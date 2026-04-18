# MCP Architecture Tools Integration Guide

## ✅ Integration Complete

The Scientific Plotting MCP Server now includes **3 new architecture diagram tools** that Claude can use directly!

## 🎯 Available MCP Tools

### 1. `list_architecture_templates`
List all available pre-built architecture templates.

**Usage in Claude:**
```
Can you list all available architecture templates?
```

**Available Templates:**
- `transformer_encoder` - Transformer encoder with multi-head attention
- `transformer_decoder` - Transformer decoder with masked attention
- `cross_attention` - Cross-attention module for multi-modal fusion
- `self_attention` - Self-attention mechanism
- `resnet_block` - ResNet residual block
- `vit` - Vision Transformer (ViT)
- `bert_layer` - BERT encoder layer
- `gpt_decoder` - GPT decoder layer
- `multimodal_fusion` - Multi-modal fusion architecture
- `deformable_conv` - Deformable convolution module

### 2. `create_architecture_from_template`
Create architecture diagram from a pre-built template.

**Parameters:**
- `template_name` (required): Name of the template
- `output_path` (required): Where to save the diagram
- `figsize` (optional): Figure size [width, height], default [12, 8]
- `dpi` (optional): DPI for output, default 300
- `template_params` (optional): Template-specific parameters

**Usage in Claude:**
```
Create a Transformer encoder diagram with 6 layers, 512 dimensions, 
and 8 attention heads. Save it to transformer.pdf
```

**Example template_params:**
```json
{
  "num_layers": 6,
  "d_model": 512,
  "num_heads": 8,
  "d_ff": 2048
}
```

### 3. `create_architecture_diagram`
Create architecture diagram from natural language or JSON description.

**Parameters:**
- `description` (required): Natural language string or JSON object
- `output_path` (required): Where to save the diagram
- `figsize` (optional): Figure size [width, height], default [12, 8]
- `style` (optional): Visual style - "transformer", "multimodal", "modern", "academic"
- `dpi` (optional): DPI for output, default 300
- `format` (optional): Output format - "pdf", "png", "svg"

**Usage in Claude (Natural Language):**
```
Create an architecture diagram for a Vision Transformer:
- Input: Image patches [196, 768]
- 12 Transformer layers with 12 heads
- Classification head
Save it to vit.pdf
```

**Usage in Claude (JSON):**
```
Create an architecture diagram with this structure:
{
  "name": "My Model",
  "style": "transformer",
  "layers": [
    {"name": "Input", "type": "input", "output_shape": "[batch, 512]"},
    {"name": "Attention", "type": "attention", "details": {"heads": 8}},
    {"name": "Output", "type": "output", "output_shape": "[batch, 1000]"}
  ]
}
Save to my_model.pdf
```

## 🎨 Visual Styles

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

## 📝 Example Prompts for Claude

### Example 1: Quick Template
```
Use the transformer_encoder template to create a diagram with 6 layers.
Save it to diagrams/transformer.pdf
```

### Example 2: Custom Description
```
Create an architecture diagram for a multi-modal model:
- Text encoder: BERT-style, 512 dimensions
- Image encoder: ViT-style, 768 dimensions  
- Cross-attention fusion with 8 heads
- Classification head
Use the multimodal style and save to diagrams/multimodal.pdf
```

### Example 3: Detailed JSON
```
Create an architecture diagram with this exact structure:
{
  "name": "Custom CNN",
  "style": "modern",
  "layers": [
    {"name": "Conv1", "type": "conv", "output_shape": "112×112×64", "color": "#764BA2"},
    {"name": "Conv2", "type": "conv", "output_shape": "56×56×128", "color": "#F093FB"},
    {"name": "Pool", "type": "pooling", "output_shape": "128", "color": "#4FACFE"},
    {"name": "FC", "type": "linear", "output_shape": "1000", "color": "#00F2FE"}
  ]
}
Save to diagrams/cnn.pdf at 300 DPI
```

## 🔧 Configuration

The MCP server is configured in `claude_config.json`:

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "C:\\download\\Anaconda\\ancoda\\python.exe",
      "args": ["C:\\download\\agent\\MCP\\picture\\server.py"],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## 🚀 How to Use

### Step 1: Restart Claude Code
After integration, restart Claude Code to load the new MCP tools.

### Step 2: Verify Tools are Available
Ask Claude:
```
What MCP tools do you have available?
```

You should see the 3 architecture tools listed.

### Step 3: Start Creating Diagrams
Just describe what you want in natural language, and Claude will use the appropriate MCP tool!

## ✅ Verification

Run the test suite to verify everything works:

```bash
python test_mcp_architecture.py
```

This will create 3 example diagrams in `test_output/`:
- `mcp_transformer.pdf` - Transformer encoder from template
- `mcp_vit.pdf` - Vision Transformer from natural language
- `mcp_multimodal.pdf` - Multi-modal fusion from JSON

## 📊 Output Quality

All diagrams are generated with:
- **300 DPI** by default (publication quality)
- **Vector PDF** format (scalable, editable)
- **Professional 3D effects** (gradients, shadows, textures)
- **Clean typography** (suitable for papers)

## 🎓 Tips for Best Results

1. **Be specific** - Include layer dimensions, parameter counts
2. **Use templates** - Faster for common architectures
3. **Choose the right style** - Match your paper's aesthetic
4. **Export as PDF** - Best for LaTeX papers
5. **Test locally first** - Run `examples_architecture.py` to see all capabilities

## 🔗 Related Documentation

- `ARCHITECTURE_GUIDE.md` - Detailed architecture visualization guide
- `examples_architecture.py` - 10 complete examples
- `QUICKSTART.md` - General MCP server usage

## 🐛 Troubleshooting

### Claude doesn't see the tools
1. Check `claude_config.json` is in the project root
2. Restart Claude Code
3. Verify Python path is correct

### Import errors
```bash
pip install -r requirements.txt
```

### Server won't start
```bash
# Test manually
python server.py
```

## 🎉 Success!

You can now ask Claude to create publication-quality architecture diagrams directly in your conversation!
