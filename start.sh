#!/bin/bash

# Scientific Plotting MCP Server Startup Script
# For AutoDL Platform

echo "=========================================="
echo "🎨 Scientific Plotting MCP Server"
echo "=========================================="
echo ""

# Display MCP configuration for remote client
echo "📋 MCP Configuration for Remote Client (Claude Desktop):"
echo ""
echo "Replace 'your-autodl-instance-url' with your actual AutoDL URL"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "scientific-plotting": {
      "url": "http://your-autodl-instance-url:6006",
      "transport": "http"
    }
  }
}
EOF
echo ""
echo "=========================================="
echo ""

# Start the HTTP API server on port 6006
echo "🚀 Starting HTTP API Server on port 6006..."
echo ""
echo "API Endpoints:"
echo "  - Root: http://0.0.0.0:6006/"
echo "  - Docs: http://0.0.0.0:6006/docs"
echo "  - Health: http://0.0.0.0:6006/health"
echo ""
echo "=========================================="
echo ""

# Run the server
python api_server.py
