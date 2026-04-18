"""Test MCP server architecture tools."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from server import (
    _create_architecture_diagram,
    _create_architecture_from_template,
    _list_architecture_templates,
)


async def test_list_templates():
    """Test listing architecture templates."""
    print("\n=== Test 1: List Architecture Templates ===")
    result = await _list_architecture_templates()
    print(result[0].text)
    print("✓ Test passed")


async def test_create_from_template():
    """Test creating diagram from template."""
    print("\n=== Test 2: Create from Template ===")

    args = {
        "template_name": "transformer_encoder",
        "output_path": "test_output/mcp_transformer.pdf",
        "figsize": [10, 12],
        "dpi": 300,
        "template_params": {
            "num_layers": 6,
            "d_model": 512,
            "num_heads": 8,
        }
    }

    result = await _create_architecture_from_template(args)
    print(result[0].text)
    print("✓ Test passed")


async def test_create_from_description():
    """Test creating diagram from natural language."""
    print("\n=== Test 3: Create from Natural Language ===")

    description = """
    A Vision Transformer (ViT) model.
    Input: Image patches [196, 768]
    - Patch Embedding layer
    - 12 Transformer Encoder layers with 12 attention heads
    - Classification head
    Output: Class probabilities [1000]
    """

    args = {
        "description": description,
        "output_path": "test_output/mcp_vit.pdf",
        "figsize": [10, 14],
        "style": "transformer",
        "dpi": 300,
    }

    result = await _create_architecture_diagram(args)
    print(result[0].text)
    print("✓ Test passed")


async def test_create_from_json():
    """Test creating diagram from JSON."""
    print("\n=== Test 4: Create from JSON ===")

    description = {
        "name": "Multi-Modal Fusion",
        "style": "multimodal",
        "layers": [
            {
                "name": "Text Encoder",
                "type": "input",
                "output_shape": "[seq_len, 512]",
                "color": "#FFD700"
            },
            {
                "name": "Image Encoder",
                "type": "input",
                "output_shape": "[196, 768]",
                "color": "#87CEEB"
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
            }
        ]
    }

    args = {
        "description": description,
        "output_path": "test_output/mcp_multimodal.pdf",
        "figsize": [12, 10],
        "dpi": 300,
    }

    result = await _create_architecture_diagram(args)
    print(result[0].text)
    print("✓ Test passed")


async def main():
    """Run all tests."""
    import os
    os.makedirs("test_output", exist_ok=True)

    print("=" * 60)
    print("MCP Architecture Tools Test")
    print("=" * 60)

    try:
        await test_list_templates()
        await test_create_from_template()
        await test_create_from_description()
        await test_create_from_json()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("Check 'test_output/' for generated diagrams")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
