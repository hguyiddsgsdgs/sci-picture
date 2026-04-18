"""Environment verification script for AutoDL platform."""

import sys
import importlib

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_package(package_name, display_name=None):
    """Check if a package is installed and return its version."""
    if display_name is None:
        display_name = package_name

    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {display_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {display_name}: NOT INSTALLED")
        return False

def main():
    print("="*60)
    print("🔍 Scientific Plotting MCP - Environment Verification")
    print("="*60)
    print()

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python Version: {py_version}")
    print()

    # Check core dependencies
    print("📦 Core Dependencies:")
    packages = [
        ('mcp', 'MCP'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
        ('plotly', 'Plotly'),
        ('scipy', 'SciPy'),
        ('sklearn', 'Scikit-learn'),
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
    ]

    all_installed = True
    for pkg, name in packages:
        if not check_package(pkg, name):
            all_installed = False

    print()
    print("="*60)

    if all_installed:
        print("✅ All dependencies installed successfully!")
        print()
        print("🚀 Ready to start the server:")
        print("   bash start.sh")
        print()
        print("   or")
        print()
        print("   python api_server.py")
        return 0
    else:
        print("❌ Some dependencies are missing!")
        print("   Please run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
