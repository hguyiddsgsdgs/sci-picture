"""Examples for architecture diagram generation."""

import matplotlib.pyplot as plt
from charts.architecture import (
    create_architecture_diagram,
    create_architecture_diagram_from_template,
    list_architecture_templates,
    create_transformer_diagram,
    create_vit_diagram,
    create_multimodal_diagram,
)


def example_1_natural_language():
    """Example 1: Create diagram from natural language description."""
    print("\n=== Example 1: Natural Language Input ===")

    description = """
    A Transformer Encoder with 6 layers.
    Input: [batch, seq_len, 512]
    Each layer contains:
    - Multi-Head Attention with 8 heads
    - Feed-Forward Network with 2048 hidden units
    - Layer Normalization
    Output: [batch, seq_len, 512]
    """

    fig = create_architecture_diagram(
        description,
        figsize=(10, 12),
        style="transformer"
    )
    fig.savefig("output/arch_example1_natural_language.pdf", dpi=300, bbox_inches='tight')
    print("✓ Saved to output/arch_example1_natural_language.pdf")
    plt.close(fig)


def example_2_json_input():
    """Example 2: Create diagram from JSON description."""
    print("\n=== Example 2: JSON Input ===")

    description = {
        "name": "Custom Vision Model",
        "style": "modern",
        "layout": "vertical",
        "layers": [
            {
                "name": "Image Input",
                "type": "input",
                "input_shape": "224×224×3",
                "color": "#667EEA"
            },
            {
                "name": "Conv Block 1",
                "type": "conv",
                "output_shape": "112×112×64",
                "params": "1.7K",
                "color": "#764BA2"
            },
            {
                "name": "Conv Block 2",
                "type": "conv",
                "output_shape": "56×56×128",
                "params": "73K",
                "color": "#F093FB"
            },
            {
                "name": "Global Pooling",
                "type": "pooling",
                "output_shape": "128",
                "color": "#4FACFE"
            },
            {
                "name": "Classification",
                "type": "linear",
                "output_shape": "1000",
                "params": "128K",
                "color": "#00F2FE"
            }
        ]
    }

    fig = create_architecture_diagram(
        description,
        figsize=(10, 12)
    )
    fig.savefig("output/arch_example2_json.pdf", dpi=300, bbox_inches='tight')
    print("✓ Saved to output/arch_example2_json.pdf")
    plt.close(fig)


def example_3_transformer_template():
    """Example 3: Use Transformer template."""
    print("\n=== Example 3: Transformer Template ===")

    fig = create_transformer_diagram(
        num_layers=6,
        d_model=512,
        num_heads=8,
        d_ff=2048,
        encoder=True,
        figsize=(10, 14),
        output_path="output/arch_example3_transformer.pdf"
    )
    print("✓ Saved to output/arch_example3_transformer.pdf")
    plt.close(fig)


def example_4_vit_template():
    """Example 4: Vision Transformer template."""
    print("\n=== Example 4: Vision Transformer ===")

    fig = create_vit_diagram(
        patch_size=16,
        d_model=768,
        num_layers=12,
        num_heads=12,
        figsize=(10, 12),
        output_path="output/arch_example4_vit.pdf"
    )
    print("✓ Saved to output/arch_example4_vit.pdf")
    plt.close(fig)


def example_5_multimodal_template():
    """Example 5: Multi-modal fusion (similar to reference image 1)."""
    print("\n=== Example 5: Multi-Modal Fusion ===")

    fig = create_multimodal_diagram(
        d_text=512,
        d_image=2048,
        d_fusion=768,
        figsize=(12, 10),
        output_path="output/arch_example5_multimodal.pdf"
    )
    print("✓ Saved to output/arch_example5_multimodal.pdf")
    plt.close(fig)


def example_6_cross_attention():
    """Example 6: Cross-attention module (like reference image 1)."""
    print("\n=== Example 6: Cross-Attention Module ===")

    fig = create_architecture_diagram_from_template(
        "cross_attention",
        d_model=512,
        num_heads=8,
        figsize=(12, 10),
        output_path="output/arch_example6_cross_attention.pdf"
    )
    print("✓ Saved to output/arch_example6_cross_attention.pdf")
    plt.close(fig)


def example_7_deformable_conv():
    """Example 7: Deformable convolution (like reference image 2)."""
    print("\n=== Example 7: Deformable Convolution ===")

    fig = create_architecture_diagram_from_template(
        "deformable_conv",
        in_channels=64,
        out_channels=64,
        figsize=(14, 8),
        output_path="output/arch_example7_deformable_conv.pdf"
    )
    print("✓ Saved to output/arch_example7_deformable_conv.pdf")
    plt.close(fig)


def example_8_bert_layer():
    """Example 8: BERT encoder layer."""
    print("\n=== Example 8: BERT Layer ===")

    fig = create_architecture_diagram_from_template(
        "bert_layer",
        d_model=768,
        num_heads=12,
        d_ff=3072,
        figsize=(10, 12),
        output_path="output/arch_example8_bert.pdf"
    )
    print("✓ Saved to output/arch_example8_bert.pdf")
    plt.close(fig)


def example_9_gpt_decoder():
    """Example 9: GPT decoder."""
    print("\n=== Example 9: GPT Decoder ===")

    fig = create_architecture_diagram_from_template(
        "gpt_decoder",
        num_layers=12,
        d_model=768,
        num_heads=12,
        d_ff=3072,
        figsize=(10, 14),
        output_path="output/arch_example9_gpt.pdf"
    )
    print("✓ Saved to output/arch_example9_gpt.pdf")
    plt.close(fig)


def example_10_resnet_block():
    """Example 10: ResNet residual block."""
    print("\n=== Example 10: ResNet Block ===")

    fig = create_architecture_diagram_from_template(
        "resnet_block",
        channels=64,
        figsize=(10, 12),
        output_path="output/arch_example10_resnet.pdf"
    )
    print("✓ Saved to output/arch_example10_resnet.pdf")
    plt.close(fig)


def list_all_templates():
    """List all available templates."""
    print("\n=== Available Architecture Templates ===")
    templates = list_architecture_templates()
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template}")


def run_all_examples():
    """Run all examples."""
    import os
    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("Architecture Diagram Examples")
    print("=" * 60)

    list_all_templates()

    try:
        example_1_natural_language()
        example_2_json_input()
        example_3_transformer_template()
        example_4_vit_template()
        example_5_multimodal_template()
        example_6_cross_attention()
        example_7_deformable_conv()
        example_8_bert_layer()
        example_9_gpt_decoder()
        example_10_resnet_block()

        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("Check the 'output/' directory for generated diagrams.")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_examples()
