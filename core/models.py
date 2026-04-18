"""Shared data models for the scientific plotter."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PlotConfig(BaseModel):
    """Configuration for a plot."""

    chart_type: str = Field(..., description="Type of chart to create")
    title: Optional[str] = Field(None, description="Chart title")
    xlabel: Optional[str] = Field(None, description="X-axis label")
    ylabel: Optional[str] = Field(None, description="Y-axis label")
    style: str = Field("default", description="Style preset")
    figsize: tuple[float, float] = Field((10, 6), description="Figure size")
    dpi: int = Field(300, description="DPI for raster output")
    interactive: bool = Field(False, description="Use interactive plotly")
    show_grid: bool = Field(True, description="Show grid")
    show_legend: bool = Field(True, description="Show legend")
    color_palette: Optional[str] = Field(None, description="Color palette name")
    font_size: int = Field(12, description="Base font size")
    extra_kwargs: Dict[str, Any] = Field(default_factory=dict, description="Extra parameters")
