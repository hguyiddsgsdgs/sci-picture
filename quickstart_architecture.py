"""Quick start example for architecture diagrams."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from arch_parser import parse_architecture
from arch_templates import ArchitectureTemplates
from arch_renderer import ArchitectureRenderer


def example_1_simple():
    """Example 1: Simple 3-layer model."""
    print("\n=== Example 1: Simple Model ===")

    spec_dict = {
        "name": "Simple Neural Network",
        "layers": [
            {"name": "Input Layer", "type": "input", "input_shape": "[B, 784]", "color": "#87CEEB"},
            {"name": "Hidden Layer", "type": "linear", "output_shape": "[B, 256]", "params": "200K", "color": "#98FB98"},
            {"name": "Output Layer", "type": "output", "output_shape": "[B, 10]", "color": "#FFB6C1"}
        ]
    }

    spec = parse_architecture(spec_dict)
    renderer = ArchitectureRenderer(spec, figsize=(8, 10))
    fig = renderer.render()

    os.makedirs("quickstart_output", exist_ok=True)
    fig.savefig("quickstart_output/example1_simple.png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("✓ Saved to quickstart_output/example1_simple.png")


def example_2_transformer():
    """Example 2: Transformer Encoder (using template)."""
    print("\n=== Example 2: Transformer Encoder ===")

    template_dict = ArchitectureTemplates.get_template(
        "transformer_encoder",
        num_layers=6,
        d_model=512,
        num_heads=8,
        d_ff=2048
    )

    spec = parse_architecture(template_dict)
    renderer = ArchitectureRenderer(spec, figsize=(10, 14))
    fig = renderer.render()

    fig.savefig("quickstart_output/example2_transformer.png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("✓ Saved to quickstart_output/example2_transformer.png")


def example_3_multimodal():
    """Example 3: Multi-modal architecture (like reference image 1)."""
    print("\n=== Example 3: Multi-Modal Fusion ===")

    template_dict = ArchitectureTemplates.get_template(
        "cross_attention",
        d_model=512,
        num_heads=8
    )

    spec = parse_architecture(template_dict)
    renderer = ArchitectureRenderer(spec, figsize=(12, 10))
    fig = renderer.render()

    fig.savefig("quickstart_output/example3_multimodal.png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("✓ Saved to quickstart_output/example3_multimodal.png")


def example_4_vit():
    """Example 4: Vision Transformer."""
    print("\n=== Example 4: Vision Transformer ===")

    template_dict = ArchitectureTemplates.get_template(
        "vit",
        patch_size=16,
        d_model=768,
        num_layers=12,
        num_heads=12
    )

    spec = parse_architecture(template_dict)
    renderer = ArchitectureRenderer(spec, figsize=(10, 12))
    fig = renderer.render()

    fig.savefig("quickstart_output/example4_vit.png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("✓ Saved to quickstart_output/example4_vit.png")


def example_5_custom():
    """Example 5: Custom architecture with connections."""
    print("\n=== Example 5: Custom Architecture ===")

    spec_dict = {
        "name": "Custom CNN with Skip Connections",
        "style": "modern",
        "layers": [
            {"name": "Input", "type": "input", "input_shape": "224×224×3", "color": "#667EEA"},
            {"name": "Conv1", "type": "conv", "output_shape": "112×112×64", "color": "#764BA2"},
            {"name": "Conv2", "type": "conv", "output_shape": "56×56×128", "color": "#F093FB"},
            {"name": "Conv3", "type": "conv", "output_shape": "28×28×256", "color": "#4FACFE"},
            {"name": "Global Pool", "type": "pooling", "output_shape": "256", "color": "#00F2FE"},
            {"name": "Output", "type": "output", "output_shape": "1000", "color": "#FFB6C1"}
        ],
        "connections": [
            {"from": "Input", "to": "Conv1"},
            {"from": "Conv1", "to": "Conv2"},
            {"from": "Conv2", "to": "Conv3"},
            {"from": "Conv1", "to": "Conv3", "style": "curved", "label": "skip"},
            {"from": "Conv3", "to": "Global Pool"},
            {"from": "Global Pool", "to": "Output"}
        ]
    }

    spec = parse_architecture(spec_dict)
    renderer = ArchitectureRenderer(spec, figsize=(10, 12))
    fig = renderer.render()

    fig.savefig("quickstart_output/example5_custom.png", dpi=200, bbox_inches='tight')
    plt.close(fig)
    print("✓ Saved to quickstart_output/example5_custom.png")


def main():
    """Run all quick start examples."""
    print("=" * 60)
    print("Architecture Diagram - Quick Start Examples")
    print("=" * 60)

    try:
        example_1_simple()
        example_2_transformer()
        example_3_multimodal()
        example_4_vit()
        example_5_custom()

        print("\n" + "=" * 60)
        print("✓ All examples completed!")
        print("Check quickstart_output/ directory for generated diagrams.")
        print("=" * 60)

        print("\n📚 Next Steps:")
        print("1. Read ARCHITECTURE_GUIDE.md for detailed documentation")
        print("2. Run examples_architecture.py for more examples")
        print("3. Check IMPLEMENTATION_SUMMARY.md for technical details")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
