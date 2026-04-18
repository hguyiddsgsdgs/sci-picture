"""Direct test for architecture diagram functionality."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Direct imports to avoid loading other chart modules
from core.arch_parser import parse_architecture
from core.arch_templates import ArchitectureTemplates
from core.arch_renderer import ArchitectureRenderer


def test_parser():
    """Test architecture parser."""
    print("Testing parser...")

    description = """
    A Transformer Encoder with 6 layers.
    Multi-Head Attention with 8 heads
    Feed-Forward Network
    """

    try:
        spec = parse_architecture(description)
        print(f"  Parsed {len(spec.layers)} layers")
        print(f"  Model name: {spec.name}")
        print(f"  Style: {spec.style}")
        print("✓ Parser test passed")
        return True
    except Exception as e:
        print(f"✗ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template():
    """Test template system."""
    print("Testing templates...")

    try:
        templates = ArchitectureTemplates.list_templates()
        print(f"  Found {len(templates)} templates")

        # Test one template
        template_dict = ArchitectureTemplates.get_template("transformer_encoder", num_layers=3)
        print(f"  Template has {len(template_dict['layers'])} layers")
        print("✓ Template test passed")
        return True
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_renderer():
    """Test renderer."""
    print("Testing renderer...")

    try:
        # Create simple spec
        spec_dict = {
            "name": "Test Model",
            "layers": [
                {"name": "Input", "type": "input"},
                {"name": "Attention", "type": "attention"},
                {"name": "Output", "type": "output"}
            ]
        }

        spec = parse_architecture(spec_dict)
        renderer = ArchitectureRenderer(spec, figsize=(8, 10))
        fig = renderer.render()

        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_renderer.png", dpi=150, bbox_inches='tight')
        plt.close(fig)

        print("✓ Renderer test passed")
        return True
    except Exception as e:
        print(f"✗ Renderer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Architecture Diagram Core Tests")
    print("=" * 60)

    results = []
    results.append(("Parser", test_parser()))
    results.append(("Templates", test_template()))
    results.append(("Renderer", test_renderer()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All core tests passed!")
    else:
        print(f"\n✗ {total - passed} test(s) failed.")

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
