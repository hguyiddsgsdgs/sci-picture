"""Direct test for architecture diagram functionality - bypass __init__.py."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Direct imports bypassing __init__.py
import importlib.util

def load_module(name, path):
    """Load module directly from file."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules
base_dir = os.path.dirname(os.path.abspath(__file__))
arch_parser = load_module("arch_parser", os.path.join(base_dir, "core", "arch_parser.py"))
arch_templates = load_module("arch_templates", os.path.join(base_dir, "core", "arch_templates.py"))
arch_elements = load_module("arch_elements", os.path.join(base_dir, "core", "arch_elements.py"))
arch_renderer = load_module("arch_renderer", os.path.join(base_dir, "core", "arch_renderer.py"))


def test_parser():
    """Test architecture parser."""
    print("Testing parser...")

    description = """
    A Transformer Encoder with 6 layers.
    Multi-Head Attention with 8 heads
    Feed-Forward Network
    """

    try:
        spec = arch_parser.parse_architecture(description)
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
        templates = arch_templates.ArchitectureTemplates.list_templates()
        print(f"  Found {len(templates)} templates:")
        for t in templates[:5]:
            print(f"    - {t}")

        # Test one template
        template_dict = arch_templates.ArchitectureTemplates.get_template(
            "transformer_encoder", num_layers=3
        )
        print(f"  Template 'transformer_encoder' has {len(template_dict['layers'])} layers")
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
                {"name": "Input", "type": "input", "color": "#87CEEB"},
                {"name": "Attention", "type": "attention", "color": "#98FB98"},
                {"name": "Output", "type": "output", "color": "#FFB6C1"}
            ]
        }

        spec = arch_parser.parse_architecture(spec_dict)
        renderer = arch_renderer.ArchitectureRenderer(spec, figsize=(8, 10))
        fig = renderer.render()

        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_renderer.png", dpi=150, bbox_inches='tight')
        plt.close(fig)

        print("  Saved to test_output/test_renderer.png")
        print("✓ Renderer test passed")
        return True
    except Exception as e:
        print(f"✗ Renderer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_pipeline():
    """Test full pipeline with template."""
    print("Testing full pipeline...")

    try:
        # Get template
        template_dict = arch_templates.ArchitectureTemplates.get_template(
            "transformer_encoder",
            num_layers=6,
            d_model=512,
            num_heads=8
        )

        # Parse
        spec = arch_parser.parse_architecture(template_dict)

        # Render
        renderer = arch_renderer.ArchitectureRenderer(spec, figsize=(10, 12))
        fig = renderer.render()

        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_transformer.png", dpi=150, bbox_inches='tight')
        plt.close(fig)

        print("  Saved to test_output/test_transformer.png")
        print("✓ Full pipeline test passed")
        return True
    except Exception as e:
        print(f"✗ Full pipeline test failed: {e}")
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
    results.append(("Full Pipeline", test_full_pipeline()))

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
        print("Check test_output/ directory for generated diagrams.")
    else:
        print(f"\n✗ {total - passed} test(s) failed.")

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
