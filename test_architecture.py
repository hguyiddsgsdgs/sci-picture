"""Quick test for architecture diagram functionality."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt
from charts.architecture import (
    create_architecture_diagram,
    create_transformer_diagram,
    list_architecture_templates
)


def test_natural_language():
    """Test natural language input."""
    print("Testing natural language input...")

    description = """
    A simple Transformer Encoder.
    Input: [batch, seq_len, 512]
    Multi-Head Attention with 8 heads
    Feed-Forward Network
    Output: [batch, seq_len, 512]
    """

    try:
        fig = create_architecture_diagram(description, figsize=(8, 10))
        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_natural_language.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("✓ Natural language test passed")
        return True
    except Exception as e:
        print(f"✗ Natural language test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_json_input():
    """Test JSON input."""
    print("Testing JSON input...")

    description = {
        "name": "Simple Model",
        "layers": [
            {"name": "Input", "type": "input", "input_shape": "[B, 512]"},
            {"name": "Attention", "type": "attention", "color": "#87CEEB"},
            {"name": "FFN", "type": "ffn", "color": "#98FB98"},
            {"name": "Output", "type": "output", "output_shape": "[B, 512]"}
        ]
    }

    try:
        fig = create_architecture_diagram(description, figsize=(8, 10))
        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_json.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("✓ JSON test passed")
        return True
    except Exception as e:
        print(f"✗ JSON test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template():
    """Test template usage."""
    print("Testing template...")

    try:
        fig = create_transformer_diagram(
            num_layers=3,
            d_model=256,
            num_heads=4,
            figsize=(8, 10)
        )
        os.makedirs("test_output", exist_ok=True)
        fig.savefig("test_output/test_template.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("✓ Template test passed")
        return True
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_list_templates():
    """Test listing templates."""
    print("Testing template listing...")

    try:
        templates = list_architecture_templates()
        print(f"  Found {len(templates)} templates:")
        for t in templates:
            print(f"    - {t}")
        print("✓ Template listing passed")
        return True
    except Exception as e:
        print(f"✗ Template listing failed: {e}")
        return False


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Architecture Diagram Quick Tests")
    print("=" * 60)

    results = []

    results.append(("List Templates", test_list_templates()))
    results.append(("Natural Language", test_natural_language()))
    results.append(("JSON Input", test_json_input()))
    results.append(("Template", test_template()))

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
        print("\n✓ All tests passed! Check test_output/ for generated diagrams.")
    else:
        print(f"\n✗ {total - passed} test(s) failed.")

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
