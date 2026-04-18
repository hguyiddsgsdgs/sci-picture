"""Environment test script for AutoDL platform审核.

This script tests that the environment is properly configured
and the code can execute successfully.
"""

import sys
import os

def test_environment():
    """Test that all core functionality works."""
    print("="*60)
    print("Scientific Plotting MCP - Environment Test")
    print("="*60)
    print()

    # Test 1: Import core modules
    print("Test 1: Importing core modules...")
    try:
        from core.plotter import ScientificPlotter, PlotConfig
        from core.utils import auto_select_chart_type
        from charts.architecture import create_architecture_diagram
        print("  ✓ All core modules imported successfully")
    except Exception as e:
        print(f"  ✗ Failed to import modules: {e}")
        return False

    # Test 2: Create plotter instance
    print("\nTest 2: Creating plotter instance...")
    try:
        plotter = ScientificPlotter(enable_cache=False)
        print("  ✓ Plotter instance created")
    except Exception as e:
        print(f"  ✗ Failed to create plotter: {e}")
        return False

    # Test 3: Test data generation
    print("\nTest 3: Generating test data...")
    try:
        import pandas as pd
        import numpy as np

        # Create simple test data
        np.random.seed(42)
        x = np.linspace(0, 10, 50)
        y = 2 * x + 1 + np.random.normal(0, 1, 50)
        test_data = pd.DataFrame({"x": x, "y": y})
        print("  ✓ Test data generated")
    except Exception as e:
        print(f"  ✗ Failed to generate data: {e}")
        return False

    # Test 4: Create a simple chart
    print("\nTest 4: Creating a simple chart...")
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend

        config = PlotConfig(
            chart_type="sci_scatter_regression",
            title="Environment Test Chart",
            xlabel="X",
            ylabel="Y",
            style="default",
            figsize=(8, 6)
        )

        fig = plotter.create_chart(test_data, config)

        # Save to test output
        os.makedirs("test_output", exist_ok=True)
        output_path = "test_output/env_test.png"
        fig.save(output_path)

        print(f"  ✓ Chart created and saved to {output_path}")
    except Exception as e:
        print(f"  ✗ Failed to create chart: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 5: Test API server imports
    print("\nTest 5: Testing API server...")
    try:
        from fastapi import FastAPI
        from api_server import app
        print("  ✓ API server can be imported")
    except Exception as e:
        print(f"  ✗ Failed to import API server: {e}")
        return False

    # Test 6: List available features
    print("\nTest 6: Checking available features...")
    try:
        chart_types = plotter.list_chart_types()
        templates = plotter.list_templates()
        styles = plotter.list_styles()

        print(f"  ✓ {len(chart_types)} chart types available")
        print(f"  ✓ {len(templates)} templates available")
        print(f"  ✓ {len(styles)} styles available")
    except Exception as e:
        print(f"  ✗ Failed to list features: {e}")
        return False

    print()
    print("="*60)
    print("✓ All tests passed! Environment is properly configured.")
    print("="*60)
    return True


if __name__ == "__main__":
    try:
        success = test_environment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Environment test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
