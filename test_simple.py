"""Simple test for architecture diagram functionality."""

import sys
import os

# Add to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import in correct order
import arch_parser
import arch_templates
import arch_elements
import arch_renderer


def test_basic():
    """Test basic functionality."""
    print("=" * 60)
    print("Architecture Diagram Basic Test")
    print("=" * 60)

    # Test 1: Parser
    print("\n1. Testing Parser...")
    try:
        spec_dict = {
            "name": "Simple Model",
            "layers": [
                {"name": "Input", "type": "input", "color": "#87CEEB"},
                {"name": "Attention", "type": "attention", "color": "#98FB98"},
                {"name": "Output", "type": "output", "color": "#FFB6C1"}
            ]
        }
        spec = arch_parser.parse_architecture(spec_dict)
        print(f"   ✓ Parsed {len(spec.layers)} layers")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    # Test 2: Templates
    print("\n2. Testing Templates...")
    try:
        templates = arch_templates.ArchitectureTemplates.list_templates()
        print(f"   ✓ Found {len(templates)} templates")
        for t in templates[:3]:
            print(f"      - {t}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

    # Test 3: Renderer
    print("\n3. Testing Renderer...")
    try:
        renderer = arch_renderer.ArchitectureRenderer(spec, figsize=(8, 10))
        fig = renderer.render()

        os.makedirs("test_output", exist_ok=True)
        output_path = "test_output/test_basic.png"
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        print(f"   ✓ Saved to {output_path}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 4: Template rendering
    print("\n4. Testing Template Rendering...")
    try:
        template_dict = arch_templates.ArchitectureTemplates.get_template(
            "transformer_encoder",
            num_layers=3,
            d_model=256,
            num_heads=4
        )
        spec = arch_parser.parse_architecture(template_dict)
        renderer = arch_renderer.ArchitectureRenderer(spec, figsize=(10, 12))
        fig = renderer.render()

        output_path = "test_output/test_transformer.png"
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        print(f"   ✓ Saved to {output_path}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("Check test_output/ directory for generated diagrams.")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = test_basic()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
