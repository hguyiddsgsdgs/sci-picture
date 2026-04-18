"""Test script for HTTP API server."""

import requests
import pandas as pd
import numpy as np
import io

# API base URL
BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_list_endpoints():
    """Test listing endpoints."""
    print("Testing list endpoints...")

    # List chart types
    response = requests.get(f"{BASE_URL}/list_chart_types")
    print(f"Chart types: {len(response.json()['chart_types'])} types")

    # List templates
    response = requests.get(f"{BASE_URL}/list_templates")
    print(f"Templates: {len(response.json()['templates'])} templates")

    # List styles
    response = requests.get(f"{BASE_URL}/list_styles")
    print(f"Styles: {len(response.json()['styles'])} styles")

    # List architecture templates
    response = requests.get(f"{BASE_URL}/list_architecture_templates")
    print(f"Architecture templates: {len(response.json()['templates'])} templates")
    print()


def test_create_chart():
    """Test creating a chart."""
    print("Testing create_chart...")

    # Create sample data
    data = pd.DataFrame({
        'x': np.linspace(0, 10, 50),
        'y': np.linspace(0, 10, 50) + np.random.randn(50)
    })

    # Convert to CSV bytes
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()

    # Send request
    files = {'file': ('data.csv', csv_bytes, 'text/csv')}
    data_form = {
        'chart_type': 'sci_scatter_regression',
        'title': 'Test Chart',
        'style': 'nature',
        'format': 'png'
    }

    response = requests.post(f"{BASE_URL}/create_chart", files=files, data=data_form)

    if response.status_code == 200:
        # Save the image
        with open('test_output/api_test_chart.png', 'wb') as f:
            f.write(response.content)
        print(f"✓ Chart created and saved to test_output/api_test_chart.png")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
    print()


def test_auto_chart():
    """Test auto chart creation."""
    print("Testing auto_chart...")

    # Create sample data
    data = pd.DataFrame({
        'x': np.linspace(0, 10, 50),
        'y': np.linspace(0, 10, 50) + np.random.randn(50)
    })

    # Convert to CSV bytes
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()

    # Send request
    files = {'file': ('data.csv', csv_bytes, 'text/csv')}
    data_form = {'style': 'default', 'format': 'png'}

    response = requests.post(f"{BASE_URL}/auto_chart", files=files, data=data_form)

    if response.status_code == 200:
        chart_type = response.headers.get('X-Chart-Type', 'unknown')
        with open('test_output/api_test_auto.png', 'wb') as f:
            f.write(response.content)
        print(f"✓ Auto chart created (type: {chart_type}) and saved to test_output/api_test_auto.png")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
    print()


def test_architecture_diagram():
    """Test architecture diagram creation."""
    print("Testing create_architecture...")

    description = """
    A simple neural network with:
    - Input layer (784 units)
    - Hidden layer (256 units)
    - Output layer (10 units)
    """

    data_form = {
        'description': description,
        'style': 'transformer',
        'format': 'png'
    }

    response = requests.post(f"{BASE_URL}/create_architecture", data=data_form)

    if response.status_code == 200:
        with open('test_output/api_test_architecture.png', 'wb') as f:
            f.write(response.content)
        print(f"✓ Architecture diagram created and saved to test_output/api_test_architecture.png")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
    print()


if __name__ == "__main__":
    import os
    os.makedirs('test_output', exist_ok=True)

    print("=" * 60)
    print("HTTP API Server Test")
    print("=" * 60)
    print()

    try:
        test_health()
        test_list_endpoints()
        test_create_chart()
        test_auto_chart()
        test_architecture_diagram()

        print("=" * 60)
        print("✓ All API tests completed!")
        print("Check test_output/ directory for generated files.")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("✗ Error: Cannot connect to API server.")
        print("Please start the server first: python api_server.py")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
