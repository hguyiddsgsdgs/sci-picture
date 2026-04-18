"""MCP server for scientific plotting."""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from core.plotter import PlotConfig, ScientificPlotter
from core.utils import auto_select_chart_type
from charts.architecture import (
    create_architecture_diagram,
    create_architecture_diagram_from_template,
    list_architecture_templates,
)


# Initialize the plotter
plotter = ScientificPlotter(enable_cache=True)

# Create MCP server
app = Server("scientific-plotter")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="create_chart",
            description="Create a scientific chart from data",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_path": {
                        "type": "string",
                        "description": "Path to data file (CSV, Excel, JSON, etc.)",
                    },
                    "chart_type": {
                        "type": "string",
                        "description": "Type of chart to create",
                        "enum": plotter.list_chart_types(),
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the chart",
                    },
                    "title": {
                        "type": "string",
                        "description": "Chart title",
                    },
                    "xlabel": {
                        "type": "string",
                        "description": "X-axis label",
                    },
                    "ylabel": {
                        "type": "string",
                        "description": "Y-axis label",
                    },
                    "style": {
                        "type": "string",
                        "description": "Style preset",
                        "enum": plotter.list_styles(),
                        "default": "default",
                    },
                    "figsize": {
                        "type": "array",
                        "description": "Figure size [width, height]",
                        "items": {"type": "number"},
                        "default": [10, 6],
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "DPI for output",
                        "default": 300,
                    },
                    "interactive": {
                        "type": "boolean",
                        "description": "Create interactive plotly chart",
                        "default": False,
                    },
                    "extra_kwargs": {
                        "type": "object",
                        "description": "Additional chart-specific parameters",
                        "default": {},
                    },
                },
                "required": ["data_path", "chart_type", "output_path"],
            },
        ),
        Tool(
            name="create_from_template",
            description="Create a chart from a predefined template",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_name": {
                        "type": "string",
                        "description": "Name of the template",
                        "enum": plotter.list_templates(),
                    },
                    "data_path": {
                        "type": "string",
                        "description": "Path to data file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the chart",
                    },
                    "overrides": {
                        "type": "object",
                        "description": "Parameters to override in template",
                        "default": {},
                    },
                },
                "required": ["template_name", "data_path", "output_path"],
            },
        ),
        Tool(
            name="batch_create",
            description="Create multiple charts in batch",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_paths": {
                        "type": "array",
                        "description": "List of data file paths",
                        "items": {"type": "string"},
                    },
                    "configs": {
                        "type": "array",
                        "description": "List of chart configurations",
                        "items": {"type": "object"},
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory",
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["png", "pdf", "svg", "eps"],
                        "default": "png",
                    },
                },
                "required": ["data_paths", "configs", "output_dir"],
            },
        ),
        Tool(
            name="auto_chart",
            description="Automatically select and create appropriate chart based on data",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_path": {
                        "type": "string",
                        "description": "Path to data file",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the chart",
                    },
                    "style": {
                        "type": "string",
                        "description": "Style preset",
                        "default": "default",
                    },
                },
                "required": ["data_path", "output_path"],
            },
        ),
        Tool(
            name="list_chart_types",
            description="List all available chart types",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="list_templates",
            description="List all available templates",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="list_styles",
            description="List all available styles",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="create_architecture_diagram",
            description="Create neural network architecture diagram from natural language or JSON description",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": ["string", "object"],
                        "description": "Natural language description or JSON structure of the architecture",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the diagram",
                    },
                    "figsize": {
                        "type": "array",
                        "description": "Figure size [width, height]",
                        "items": {"type": "number"},
                        "default": [12, 8],
                    },
                    "style": {
                        "type": "string",
                        "description": "Visual style (transformer, multimodal, modern, academic)",
                        "enum": ["transformer", "multimodal", "modern", "academic"],
                        "default": "transformer",
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "DPI for output",
                        "default": 300,
                    },
                    "format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["pdf", "png", "svg"],
                        "default": "pdf",
                    },
                },
                "required": ["description", "output_path"],
            },
        ),
        Tool(
            name="create_architecture_from_template",
            description="Create architecture diagram from predefined template (Transformer, BERT, GPT, ViT, ResNet, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_name": {
                        "type": "string",
                        "description": "Name of the template",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path to save the diagram",
                    },
                    "figsize": {
                        "type": "array",
                        "description": "Figure size [width, height]",
                        "items": {"type": "number"},
                        "default": [12, 8],
                    },
                    "dpi": {
                        "type": "integer",
                        "description": "DPI for output",
                        "default": 300,
                    },
                    "template_params": {
                        "type": "object",
                        "description": "Template-specific parameters (e.g., num_layers, d_model, num_heads)",
                        "default": {},
                    },
                },
                "required": ["template_name", "output_path"],
            },
        ),
        Tool(
            name="list_architecture_templates",
            description="List all available architecture templates",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "create_chart":
            return await _create_chart(arguments)
        elif name == "create_from_template":
            return await _create_from_template(arguments)
        elif name == "batch_create":
            return await _batch_create(arguments)
        elif name == "auto_chart":
            return await _auto_chart(arguments)
        elif name == "list_chart_types":
            return await _list_chart_types()
        elif name == "list_templates":
            return await _list_templates()
        elif name == "list_styles":
            return await _list_styles()
        elif name == "create_architecture_diagram":
            return await _create_architecture_diagram(arguments)
        elif name == "create_architecture_from_template":
            return await _create_architecture_from_template(arguments)
        elif name == "list_architecture_templates":
            return await _list_architecture_templates()
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def _create_chart(args: Dict[str, Any]) -> List[TextContent]:
    """Create a chart."""
    data_path = args["data_path"]
    output_path = args["output_path"]

    # Build config
    config = PlotConfig(
        chart_type=args["chart_type"],
        title=args.get("title"),
        xlabel=args.get("xlabel"),
        ylabel=args.get("ylabel"),
        style=args.get("style", "default"),
        figsize=tuple(args.get("figsize", [10, 6])),
        dpi=args.get("dpi", 300),
        interactive=args.get("interactive", False),
        extra_kwargs=args.get("extra_kwargs", {}),
    )

    # Create chart
    fig = plotter.create_chart(data_path, config)

    # Save
    output_path = Path(output_path)
    fig.save(output_path)

    return [
        TextContent(
            type="text",
            text=f"Chart created successfully and saved to {output_path}",
        )
    ]


async def _create_from_template(args: Dict[str, Any]) -> List[TextContent]:
    """Create chart from template."""
    template_name = args["template_name"]
    data_path = args["data_path"]
    output_path = args["output_path"]
    overrides = args.get("overrides", {})

    # Create chart
    fig = plotter.create_from_template(template_name, data_path, **overrides)

    # Save
    output_path = Path(output_path)
    fig.save(output_path)

    return [
        TextContent(
            type="text",
            text=f"Chart created from template '{template_name}' and saved to {output_path}",
        )
    ]


async def _batch_create(args: Dict[str, Any]) -> List[TextContent]:
    """Create multiple charts in batch."""
    data_paths = args["data_paths"]
    configs = args["configs"]
    output_dir = args["output_dir"]
    format = args.get("format", "png")

    # Convert configs to PlotConfig objects
    plot_configs = [PlotConfig(**cfg) for cfg in configs]

    # Create charts
    output_paths = plotter.batch_create(
        data_paths, plot_configs, output_dir, format=format
    )

    return [
        TextContent(
            type="text",
            text=f"Created {len(output_paths)} charts in {output_dir}:\n"
            + "\n".join(f"- {p}" for p in output_paths),
        )
    ]


async def _auto_chart(args: Dict[str, Any]) -> List[TextContent]:
    """Automatically create appropriate chart."""
    data_path = args["data_path"]
    output_path = args["output_path"]
    style = args.get("style", "default")

    # Load data and infer chart type
    data = plotter.data_loader.load(data_path)
    chart_type = auto_select_chart_type(data)

    # Create config
    config = PlotConfig(
        chart_type=chart_type,
        style=style,
    )

    # Create chart
    fig = plotter.create_chart(data, config)

    # Save
    output_path = Path(output_path)
    fig.save(output_path)

    return [
        TextContent(
            type="text",
            text=f"Auto-selected chart type '{chart_type}' and saved to {output_path}",
        )
    ]


async def _list_chart_types() -> List[TextContent]:
    """List all chart types."""
    chart_types = plotter.list_chart_types()
    return [
        TextContent(
            type="text",
            text="Available chart types:\n" + "\n".join(f"- {ct}" for ct in chart_types),
        )
    ]


async def _list_templates() -> List[TextContent]:
    """List all templates."""
    templates = plotter.list_templates()
    return [
        TextContent(
            type="text",
            text="Available templates:\n" + "\n".join(f"- {t}" for t in templates),
        )
    ]


async def _list_styles() -> List[TextContent]:
    """List all styles."""
    styles = plotter.list_styles()
    return [
        TextContent(
            type="text",
            text="Available styles:\n" + "\n".join(f"- {s}" for s in styles),
        )
    ]


async def _create_architecture_diagram(args: Dict[str, Any]) -> List[TextContent]:
    """Create architecture diagram from description."""
    description = args["description"]
    output_path = args["output_path"]
    figsize = tuple(args.get("figsize", [12, 8]))
    style = args.get("style", "transformer")
    dpi = args.get("dpi", 300)
    format = args.get("format", "pdf")

    # Create diagram
    fig = create_architecture_diagram(
        description=description,
        figsize=figsize,
        style=style,
        dpi=dpi,
        format=format,
    )

    # Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')

    return [
        TextContent(
            type="text",
            text=f"Architecture diagram created successfully and saved to {output_path}",
        )
    ]


async def _create_architecture_from_template(args: Dict[str, Any]) -> List[TextContent]:
    """Create architecture diagram from template."""
    template_name = args["template_name"]
    output_path = args["output_path"]
    figsize = tuple(args.get("figsize", [12, 8]))
    dpi = args.get("dpi", 300)
    template_params = args.get("template_params", {})

    # Create diagram
    fig = create_architecture_diagram_from_template(
        template_name=template_name,
        figsize=figsize,
        output_path=None,
        dpi=dpi,
        **template_params,
    )

    # Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')

    return [
        TextContent(
            type="text",
            text=f"Architecture diagram created from template '{template_name}' and saved to {output_path}",
        )
    ]


async def _list_architecture_templates() -> List[TextContent]:
    """List all architecture templates."""
    templates = list_architecture_templates()
    return [
        TextContent(
            type="text",
            text="Available architecture templates:\n" + "\n".join(f"- {t}" for t in templates),
        )
    ]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
