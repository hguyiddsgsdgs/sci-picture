"""Time series chart creation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.axes import Axes


def create_timeseries_chart(ax: Axes, data: pd.DataFrame, config):
    """Create time series charts using matplotlib.

    Args:
        ax: Matplotlib axes
        data: Input data (index should be datetime)
        config: Plot configuration
    """
    chart_type = config.chart_type

    if chart_type == "ts_line":
        _create_line_chart(ax, data, config)
    elif chart_type == "ts_area":
        _create_area_chart(ax, data, config)
    elif chart_type == "ts_candlestick":
        _create_candlestick_chart(ax, data, config)
    elif chart_type == "ts_decomposition":
        _create_decomposition_chart(data, config)
    else:
        raise ValueError(f"Unknown time series chart type: {chart_type}")


def _create_line_chart(ax: Axes, data: pd.DataFrame, config):
    """Create line chart."""
    kwargs = config.extra_kwargs
    marker = kwargs.pop("marker", None)
    markersize = kwargs.pop("markersize", 4)

    for col in data.columns:
        ax.plot(data.index, data[col], label=col, marker=marker,
                markersize=markersize, **kwargs)

    ax.set_xlabel("Time")
    ax.set_ylabel("Value")

    # Rotate x-axis labels for better readability
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def _create_area_chart(ax: Axes, data: pd.DataFrame, config):
    """Create area chart."""
    kwargs = config.extra_kwargs
    alpha = kwargs.pop("alpha", 0.5)

    for col in data.columns:
        ax.fill_between(data.index, data[col], alpha=alpha, label=col, **kwargs)

    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def _create_candlestick_chart(ax: Axes, data: pd.DataFrame, config):
    """Create candlestick chart (requires OHLC data)."""
    # Expect columns: Open, High, Low, Close
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in data.columns for col in required_cols):
        raise ValueError(f"Candlestick chart requires columns: {required_cols}")

    # Calculate colors
    colors = ['g' if data['Close'].iloc[i] >= data['Open'].iloc[i] else 'r'
              for i in range(len(data))]

    # Plot candlesticks
    for i in range(len(data)):
        # High-Low line
        ax.plot([i, i], [data['Low'].iloc[i], data['High'].iloc[i]],
                color='black', linewidth=0.5)

        # Open-Close box
        height = abs(data['Close'].iloc[i] - data['Open'].iloc[i])
        bottom = min(data['Open'].iloc[i], data['Close'].iloc[i])
        ax.bar(i, height, bottom=bottom, color=colors[i], width=0.6, alpha=0.8)

    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.index, rotation=45, ha='right')


def _create_decomposition_chart(data: pd.DataFrame, config):
    """Create time series decomposition chart."""
    from statsmodels.tsa.seasonal import seasonal_decompose

    kwargs = config.extra_kwargs
    period = kwargs.get("period", None)

    # Decompose the first column
    col = data.columns[0]
    decomposition = seasonal_decompose(data[col].dropna(), period=period)

    # Create subplots
    fig, axes = plt.subplots(4, 1, figsize=config.figsize)

    decomposition.observed.plot(ax=axes[0], title='Observed')
    decomposition.trend.plot(ax=axes[1], title='Trend')
    decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
    decomposition.resid.plot(ax=axes[3], title='Residual')

    plt.tight_layout()
    return fig


def create_timeseries_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create time series charts using plotly.

    Args:
        data: Input data
        config: Plot configuration

    Returns:
        Plotly figure
    """
    chart_type = config.chart_type

    if chart_type == "ts_line":
        return _create_line_chart_plotly(data, config)
    elif chart_type == "ts_area":
        return _create_area_chart_plotly(data, config)
    elif chart_type == "ts_candlestick":
        return _create_candlestick_chart_plotly(data, config)
    else:
        raise ValueError(f"Unknown time series chart type: {chart_type}")


def _create_line_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create line chart with plotly."""
    fig = go.Figure()
    kwargs = config.extra_kwargs

    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode='lines+markers',
            name=col,
            marker=dict(size=kwargs.get("markersize", 4))
        ))

    return fig


def _create_area_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create area chart with plotly."""
    fig = go.Figure()

    for col in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[col],
            mode='lines',
            name=col,
            fill='tozeroy',
            opacity=0.5
        ))

    return fig


def _create_candlestick_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create candlestick chart with plotly."""
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in data.columns for col in required_cols):
        raise ValueError(f"Candlestick chart requires columns: {required_cols}")

    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    return fig
