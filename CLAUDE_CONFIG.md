# Claude Desktop Configuration Guide

## Configuration for Windows

### Option 1: Full Configuration (Recommended)

Add this to your Claude Desktop configuration file:

**Location**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### Option 2: Using Python Virtual Environment

If you're using a virtual environment:

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "C:\\path\\to\\your\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### Option 3: With Specific Python Version

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python3",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Configuration for macOS/Linux

**Location**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python3",
      "args": [
        "/path/to/picture/server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Setup Steps

### 1. Install Dependencies

```bash
cd C:\download\agent\MCP\picture
pip install -r requirements.txt
```

### 2. Test the Server

```bash
python server.py
```

If it starts without errors, press Ctrl+C to stop it.

### 3. Add Configuration to Claude Desktop

1. Open the configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/.config/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. If the file doesn't exist, create it with the content above.

3. If the file exists and has other MCP servers, add the `scientific-plotter` entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### 4. Restart Claude Desktop

Close and reopen Claude Desktop for the changes to take effect.

### 5. Verify Installation

In Claude Desktop, you should now see the scientific-plotter tools available. Try asking:

```
"Can you list the available chart types from the scientific plotter?"
```

Claude should be able to call the `list_chart_types` tool.

## Available Tools

Once configured, Claude can use these tools:

1. **create_chart** - Create a chart from data
2. **create_from_template** - Use a predefined template
3. **batch_create** - Create multiple charts
4. **auto_chart** - Automatically select chart type
5. **list_chart_types** - List all chart types
6. **list_templates** - List all templates
7. **list_styles** - List all styles

## Example Usage in Claude

After configuration, you can ask Claude:

```
"Create a scatter plot with regression from my data.csv file and save it as chart.png"
```

```
"Use the nature_figure template to create a publication-ready figure from data.csv"
```

```
"Create a confusion matrix from my ML results in results.csv"
```

```
"Show me all available chart types"
```

## Troubleshooting

### Issue: Server doesn't start

**Solution**: Check Python installation
```bash
python --version
# Should be Python 3.8+
```

### Issue: Import errors

**Solution**: Install dependencies
```bash
cd C:\download\agent\MCP\picture
pip install -r requirements.txt
```

### Issue: Path not found

**Solution**: Use absolute paths in configuration
```json
"args": [
  "C:\\download\\agent\\MCP\\picture\\server.py"
]
```

### Issue: Permission denied

**Solution**: Check file permissions
```bash
# Windows
icacls C:\download\agent\MCP\picture\server.py

# macOS/Linux
chmod +x /path/to/picture/server.py
```

### Issue: Server starts but tools not available

**Solution**: Check Claude Desktop logs
- Windows: `%APPDATA%\Claude\logs\`
- macOS: `~/Library/Logs/Claude/`
- Linux: `~/.config/Claude/logs/`

### Issue: Python not found

**Solution**: Use full path to Python executable
```json
"command": "C:\\Python39\\python.exe"
```

Or find Python path:
```bash
# Windows
where python

# macOS/Linux
which python3
```

## Advanced Configuration

### Enable Debug Logging

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8",
        "DEBUG": "true"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### Disable Caching

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8",
        "DISABLE_CACHE": "true"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

### Custom Cache Directory

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8",
        "CACHE_DIR": "C:\\Users\\YourName\\.cache\\scientific_plotter"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Security Considerations

### Always Allow Specific Tools

If you want to auto-approve certain tools:

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": [
        "list_chart_types",
        "list_templates",
        "list_styles"
      ]
    }
  }
}
```

### Restrict File Access

Add environment variables to restrict file access:

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8",
        "ALLOWED_PATHS": "C:\\Users\\YourName\\Documents\\data"
      },
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## Testing the Configuration

### 1. Test Server Directly

```bash
cd C:\download\agent\MCP\picture
python server.py
```

### 2. Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

### 3. Test in Claude Desktop

Ask Claude:
```
"List all available chart types from the scientific plotter"
```

Expected response should include the list of 25+ chart types.

## Complete Example Configuration

Here's a complete, production-ready configuration:

```json
{
  "mcpServers": {
    "scientific-plotter": {
      "command": "python",
      "args": [
        "C:\\download\\agent\\MCP\\picture\\server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\download\\agent\\MCP\\picture",
        "PYTHONIOENCODING": "utf-8"
      },
      "disabled": false,
      "alwaysAllow": [
        "list_chart_types",
        "list_templates",
        "list_styles"
      ]
    }
  },
  "globalShortcut": "CommandOrControl+Shift+Space"
}
```

## Next Steps

After successful configuration:

1. ✅ Test basic chart creation
2. ✅ Try different chart types
3. ✅ Use templates
4. ✅ Create publication-ready figures
5. ✅ Explore batch processing

Enjoy using the Scientific Plotting MCP! 📊
