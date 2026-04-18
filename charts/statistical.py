"""Statistical chart creation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from matplotlib.axes import Axes
from scipy import stats


def create_statistical_chart(ax: Axes, data: pd.DataFrame, config):
    """Create statistical charts using matplotlib.

    Args:
        ax: Matplotlib axes
        data: Input data
        config: Plot configuration
    """
    chart_type = config.chart_type

    if chart_type == "stat_boxplot":
        _create_boxplot(ax, data, config)
    elif chart_type == "stat_violin":
        _create_violin(ax, data, config)
    elif chart_type == "stat_distribution":
        _create_distribution(ax, data, config)
    elif chart_type == "stat_correlation_heatmap":
        _create_correlation_heatmap(ax, data, config)
    elif chart_type == "stat_pairplot":
        _create_pairplot(data, config)
    else:
        raise ValueError(f"Unknown statistical chart type: {chart_type}")


def _create_boxplot(ax: Axes, data: pd.DataFrame, config):
    """Create box plot."""
    kwargs = config.extra_kwargs

    if len(data.columns) == 1:
        # Single variable
        ax.boxplot(data.iloc[:, 0].dropna(), **kwargs)
        ax.set_xticklabels([data.columns[0]])
    else:
        # Multiple variables
        ax.boxplot([data[col].dropna() for col in data.columns],
                   labels=data.columns, **kwargs)

    ax.set_ylabel("Value")


def _create_violin(ax: Axes, data: pd.DataFrame, config):
    """Create violin plot."""
    kwargs = config.extra_kwargs

    # Prepare data for seaborn
    data_melted = data.melt(var_name="Variable", value_name="Value")

    sns.violinplot(data=data_melted, x="Variable", y="Value", ax=ax, **kwargs)
    ax.set_xlabel("")


def _create_distribution(ax: Axes, data: pd.DataFrame, config):
    """Create distribution plot."""
    kwargs = config.extra_kwargs
    kde = kwargs.pop("kde", True)
    bins = kwargs.pop("bins", 30)

    for col in data.columns:
        values = data[col].dropna()
        ax.hist(values, bins=bins, alpha=0.6, label=col, **kwargs)

        if kde:
            # Add KDE
            kde_x = np.linspace(values.min(), values.max(), 100)
            kde_y = stats.gaussian_kde(values)(kde_x)
            # Scale KDE to match histogram
            kde_y = kde_y * len(values) * (values.max() - values.min()) / bins
            ax.plot(kde_x, kde_y, linewidth=2)

    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")


def _create_correlation_heatmap(ax: Axes, data: pd.DataFrame, config):
    """Create correlation heatmap."""
    kwargs = config.extra_kwargs

    # Calculate correlation matrix
    corr = data.corr()

    # Create heatmap
    sns.heatmap(corr, ax=ax, **kwargs)


def _create_pairplot(data: pd.DataFrame, config):
    """Create pair plot (returns figure, not using ax)."""
    kwargs = config.extra_kwargs

    # Seaborn pairplot creates its own figure
    g = sns.pairplot(data, **kwargs)
    return g.fig


def create_statistical_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create statistical charts using plotly.

    Args:
        data: Input data
        config: Plot configuration

    Returns:
        Plotly figure
    """
    chart_type = config.chart_type

    if chart_type == "stat_boxplot":
        return _create_boxplot_plotly(data, config)
    elif chart_type == "stat_violin":
        return _create_violin_plotly(data, config)
    elif chart_type == "stat_distribution":
        return _create_distribution_plotly(data, config)
    elif chart_type == "stat_correlation_heatmap":
        return _create_correlation_heatmap_plotly(data, config)
    else:
        raise ValueError(f"Unknown statistical chart type: {chart_type}")


def _create_boxplot_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create box plot with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Box(
            y=data[col].dropna(),
            name=col,
            boxmean='sd'  # Show mean and std
        ))

    return fig


def _create_violin_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create violin plot with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Violin(
            y=data[col].dropna(),
            name=col,
            box_visible=True,
            meanline_visible=True
        ))

    return fig


def _create_distribution_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create distribution plot with plotly."""
    fig = go.Figure()
    kwargs = config.extra_kwargs
    bins = kwargs.get("bins", 30)

    for col in data.columns:
        fig.add_trace(go.Histogram(
            x=data[col].dropna(),
            name=col,
            nbinsx=bins,
            opacity=0.7
        ))

    fig.update_layout(barmode='overlay')
    return fig


def _create_correlation_heatmap_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create correlation heatmap with plotly."""
    kwargs = config.extra_kwargs

    # Calculate correlation matrix
    corr = data.corr()

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale=kwargs.get("cmap", "RdBu"),
        zmid=kwargs.get("center", 0),
        text=corr.values if kwargs.get("annot", False) else None,
        texttemplate='%{text:.2f}' if kwargs.get("annot", False) else None,
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        xaxis=dict(side="bottom"),
        yaxis=dict(autorange="reversed")
    )

    return fig
