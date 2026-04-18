"""Command-line interface for the scientific plotter."""

import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table

from core.plotter import ScientificPlotter, PlotConfig

app = typer.Typer(help="Scientific Plotting Tool")
console = Console()


@app.command()
def create(
    data_path: Path = typer.Argument(..., help="Path to data file"),
    chart_type: str = typer.Option(..., "--type", "-t", help="Chart type"),
    output: Path = typer.Option("output.png", "--output", "-o", help="Output path"),
    title: Optional[str] = typer.Option(None, help="Chart title"),
    xlabel: Optional[str] = typer.Option(None, help="X-axis label"),
    ylabel: Optional[str] = typer.Option(None, help="Y-axis label"),
    style: str = typer.Option("default", help="Style preset"),
    width: int = typer.Option(10, help="Figure width"),
    height: int = typer.Option(6, help="Figure height"),
    dpi: int = typer.Option(300, help="DPI for output"),
    interactive: bool = typer.Option(False, help="Create interactive chart"),
):
    """Create a chart from data."""
    plotter = ScientificPlotter()

    config = PlotConfig(
        chart_type=chart_type,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        style=style,
        figsize=(width, height),
        dpi=dpi,
        interactive=interactive,
    )

    try:
        fig = plotter.create_chart(data_path, config)
        fig.save(output)
        console.print(f"✅ Chart saved to [green]{output}[/green]")
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
        raise typer.Exit(1)


@app.command()
def template(
    data_path: Path = typer.Argument(..., help="Path to data file"),
    template_name: str = typer.Option(..., "--template", "-t", help="Template name"),
    output: Path = typer.Option("output.png", "--output", "-o", help="Output path"),
):
    """Create a chart from a template."""
    plotter = ScientificPlotter()

    try:
        fig = plotter.create_from_template(template_name, data_path)
        fig.save(output)
        console.print(f"✅ Chart saved to [green]{output}[/green]")
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
        raise typer.Exit(1)


@app.command()
def auto(
    data_path: Path = typer.Argument(..., help="Path to data file"),
    output: Path = typer.Option("output.png", "--output", "-o", help="Output path"),
    style: str = typer.Option("default", help="Style preset"),
):
    """Automatically create appropriate chart based on data."""
    plotter = ScientificPlotter()
    from core.utils import auto_select_chart_type

    try:
        data = plotter.data_loader.load(data_path)
        chart_type = auto_select_chart_type(data)

        console.print(f"📊 Auto-selected chart type: [cyan]{chart_type}[/cyan]")

        config = PlotConfig(chart_type=chart_type, style=style)
        fig = plotter.create_chart(data, config)
        fig.save(output)

        console.print(f"✅ Chart saved to [green]{output}[/green]")
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
        raise typer.Exit(1)


@app.command()
def list_types():
    """List all available chart types."""
    plotter = ScientificPlotter()
    chart_types = plotter.list_chart_types()

    table = Table(title="Available Chart Types")
    table.add_column("Category", style="cyan")
    table.add_column("Chart Type", style="green")

    categories = {
        "Statistical": [ct for ct in chart_types if ct.startswith("stat_")],
        "Time Series": [ct for ct in chart_types if ct.startswith("ts_")],
        "Comparison": [ct for ct in chart_types if ct.startswith("comp_")],
        "Scientific": [ct for ct in chart_types if ct.startswith("sci_")],
        "ML/AI": [ct for ct in chart_types if ct.startswith("ml_")],
    }

    for category, types in categories.items():
        for i, ct in enumerate(types):
            table.add_row(category if i == 0 else "", ct)

    console.print(table)


@app.command()
def list_templates():
    """List all available templates."""
    plotter = ScientificPlotter()
    categories = plotter.template_manager.get_templates_by_category()

    table = Table(title="Available Templates")
    table.add_column("Category", style="cyan")
    table.add_column("Template Name", style="green")

    for category, templates in categories.items():
        for i, template in enumerate(templates):
            table.add_row(category if i == 0 else "", template)

    console.print(table)


@app.command()
def list_styles():
    """List all available styles."""
    plotter = ScientificPlotter()
    styles = plotter.list_styles()

    table = Table(title="Available Styles")
    table.add_column("Style Name", style="cyan")
    table.add_column("Description", style="white")

    descriptions = {
        "nature": "Nature journal style",
        "science": "Science journal style",
        "ieee": "IEEE conference style",
        "acm": "ACM conference style",
        "springer": "Springer journal style",
        "default": "Default matplotlib style",
        "minimal": "Minimal clean style",
        "colorblind": "Colorblind-friendly palette",
    }

    for style in styles:
        desc = descriptions.get(style, "Custom style")
        table.add_row(style, desc)

    console.print(table)


@app.command()
def batch(
    data_dir: Path = typer.Argument(..., help="Directory containing data files"),
    output_dir: Path = typer.Option("output", help="Output directory"),
    chart_type: str = typer.Option(..., "--type", "-t", help="Chart type for all"),
    style: str = typer.Option("default", help="Style preset"),
    format: str = typer.Option("png", help="Output format"),
):
    """Create charts for all data files in a directory."""
    plotter = ScientificPlotter()

    if not data_dir.is_dir():
        console.print(f"❌ Error: [red]{data_dir} is not a directory[/red]")
        raise typer.Exit(1)

    # Find all data files
    data_files = list(data_dir.glob("*.csv")) + list(data_dir.glob("*.xlsx"))

    if not data_files:
        console.print(f"❌ No data files found in [red]{data_dir}[/red]")
        raise typer.Exit(1)

    console.print(f"📁 Found {len(data_files)} data files")

    # Create configs
    configs = [PlotConfig(chart_type=chart_type, style=style) for _ in data_files]

    try:
        output_paths = plotter.batch_create(data_files, configs, output_dir, format=format)
        console.print(f"✅ Created {len(output_paths)} charts in [green]{output_dir}[/green]")
    except Exception as e:
        console.print(f"❌ Error: [red]{e}[/red]")
        raise typer.Exit(1)


@app.command()
def clear_cache():
    """Clear the plot cache."""
    plotter = ScientificPlotter()
    if plotter.cache_manager:
        size_before = plotter.cache_manager.get_cache_size()
        plotter.cache_manager.clear()
        console.print(f"✅ Cleared cache ({size_before / 1024 / 1024:.2f} MB)")
    else:
        console.print("ℹ️  Cache is disabled")


if __name__ == "__main__":
    app()
