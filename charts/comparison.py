"""Comparison chart creation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.axes import Axes


def create_comparison_chart(ax: Axes, data: pd.DataFrame, config):
    """Create comparison charts using matplotlib.

    Args:
        ax: Matplotlib axes
        data: Input data
        config: Plot configuration
    """
    chart_type = config.chart_type

    if chart_type == "comp_bar":
        _create_bar_chart(ax, data, config)
    elif chart_type == "comp_grouped_bar":
        _create_grouped_bar_chart(ax, data, config)
    elif chart_type == "comp_stacked_bar":
        _create_stacked_bar_chart(ax, data, config)
    elif chart_type == "comp_radar":
        _create_radar_chart(data, config)
    else:
        raise ValueError(f"Unknown comparison chart type: {chart_type}")


def _create_bar_chart(ax: Axes, data: pd.DataFrame, config):
    """Create simple bar chart."""
    kwargs = config.extra_kwargs
    error_bars = kwargs.pop("error_bars", False)

    if len(data.columns) == 1:
        # Single series
        bars = ax.bar(data.index, data.iloc[:, 0], **kwargs)
        ax.set_ylabel(data.columns[0])
    else:
        # Multiple series - use first column as values
        bars = ax.bar(data.index, data.iloc[:, 0], **kwargs)
        ax.set_ylabel("Value")

    ax.set_xlabel("Category")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def _create_grouped_bar_chart(ax: Axes, data: pd.DataFrame, config):
    """Create grouped bar chart."""
    kwargs = config.extra_kwargs
    bar_width = kwargs.pop("bar_width", 0.35)

    n_groups = len(data.index)
    n_bars = len(data.columns)
    x = np.arange(n_groups)

    for i, col in enumerate(data.columns):
        offset = (i - n_bars / 2) * bar_width + bar_width / 2
        ax.bar(x + offset, data[col], bar_width, label=col, **kwargs)

    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.set_xticks(x)
    ax.set_xticklabels(data.index, rotation=45, ha='right')


def _create_stacked_bar_chart(ax: Axes, data: pd.DataFrame, config):
    """Create stacked bar chart."""
    kwargs = config.extra_kwargs

    bottom = np.zeros(len(data))
    for col in data.columns:
        ax.bar(data.index, data[col], label=col, bottom=bottom, **kwargs)
        bottom += data[col].values

    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def _create_radar_chart(data: pd.DataFrame, config):
    """Create radar chart."""
    kwargs = config.extra_kwargs
    fill = kwargs.pop("fill", True)
    alpha = kwargs.pop("alpha", 0.25)

    # Number of variables
    categories = list(data.columns)
    n_cats = len(categories)

    # Compute angle for each axis
    angles = [n / float(n_cats) * 2 * np.pi for n in range(n_cats)]
    angles += angles[:1]  # Complete the circle

    # Create figure
    fig, ax = plt.subplots(figsize=config.figsize, subplot_kw=dict(projection='polar'))

    # Plot each row
    for idx, row in data.iterrows():
        values = row.values.tolist()
        values += values[:1]  # Complete the circle

        ax.plot(angles, values, 'o-', linewidth=2, label=idx, **kwargs)
        if fill:
            ax.fill(angles, values, alpha=alpha)

    # Fix axis to go in the right order
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, data.values.max() * 1.1)

    return fig


def create_comparison_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create comparison charts using plotly.

    Args:
        data: Input data
        config: Plot configuration

    Returns:
        Plotly figure
    """
    chart_type = config.chart_type

    if chart_type == "comp_bar":
        return _create_bar_chart_plotly(data, config)
    elif chart_type == "comp_grouped_bar":
        return _create_grouped_bar_chart_plotly(data, config)
    elif chart_type == "comp_stacked_bar":
        return _create_stacked_bar_chart_plotly(data, config)
    elif chart_type == "comp_radar":
        return _create_radar_chart_plotly(data, config)
    else:
        raise ValueError(f"Unknown comparison chart type: {chart_type}")


def _create_bar_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create bar chart with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Bar(
            x=data.index,
            y=data[col],
            name=col
        ))

    return fig


def _create_grouped_bar_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create grouped bar chart with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Bar(
            x=data.index,
            y=data[col],
            name=col
        ))

    fig.update_layout(barmode='group')
    return fig


def _create_stacked_bar_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create stacked bar chart with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Bar(
            x=data.index,
            y=data[col],
            name=col
        ))

    fig.update_layout(barmode='stack')
    return fig


def _create_radar_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create radar chart with plotly."""
    fig = go.Figure()
    kwargs = config.extra_kwargs

    for idx, row in data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=row.values.tolist() + [row.values[0]],  # Complete the circle
            theta=list(data.columns) + [data.columns[0]],
            fill='toself' if kwargs.get("fill", True) else None,
            name=str(idx),
            opacity=kwargs.get("alpha", 0.5)
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, data.values.max() * 1.1]
            )
        )
    )

    return fig
