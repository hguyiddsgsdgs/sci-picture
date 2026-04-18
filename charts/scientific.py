"""Scientific chart creation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.axes import Axes
from scipy import stats
from scipy.interpolate import griddata


def create_scientific_chart(ax: Axes, data: pd.DataFrame, config):
    """Create scientific charts using matplotlib.

    Args:
        ax: Matplotlib axes
        data: Input data
        config: Plot configuration
    """
    chart_type = config.chart_type

    if chart_type == "sci_scatter_regression":
        _create_scatter_regression(ax, data, config)
    elif chart_type == "sci_contour":
        _create_contour(ax, data, config)
    elif chart_type == "sci_3d_surface":
        _create_3d_surface(data, config)
    elif chart_type == "sci_vector_field":
        _create_vector_field(ax, data, config)
    else:
        raise ValueError(f"Unknown scientific chart type: {chart_type}")


def _create_scatter_regression(ax: Axes, data: pd.DataFrame, config):
    """Create scatter plot with regression line."""
    kwargs = config.extra_kwargs
    show_regression = kwargs.pop("show_regression", True)
    show_confidence = kwargs.pop("show_confidence", True)
    show_equation = kwargs.pop("show_equation", True)
    show_r2 = kwargs.pop("show_r2", True)

    # Expect 2 columns: x and y
    if len(data.columns) < 2:
        raise ValueError("Scatter regression requires at least 2 columns")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values

    # Remove NaN values
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]

    # Scatter plot
    ax.scatter(x, y, alpha=0.6, **kwargs)

    if show_regression:
        # Calculate regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # Regression line
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'r-', linewidth=2, label='Regression')

        # Confidence interval
        if show_confidence:
            predict_y = slope * x + intercept
            residuals = y - predict_y
            std_residuals = np.std(residuals)

            y_upper = y_line + 1.96 * std_residuals
            y_lower = y_line - 1.96 * std_residuals
            ax.fill_between(x_line, y_lower, y_upper, alpha=0.2, color='red')

        # Add equation and R²
        text_items = []
        if show_equation:
            text_items.append(f'y = {slope:.3f}x + {intercept:.3f}')
        if show_r2:
            text_items.append(f'R² = {r_value**2:.3f}')

        if text_items:
            ax.text(0.05, 0.95, '\n'.join(text_items),
                   transform=ax.transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel(data.columns[0])
    ax.set_ylabel(data.columns[1])


def _create_contour(ax: Axes, data: pd.DataFrame, config):
    """Create contour plot."""
    kwargs = config.extra_kwargs
    levels = kwargs.pop("levels", 20)
    cmap = kwargs.pop("cmap", "viridis")

    # Expect 3 columns: x, y, z
    if len(data.columns) < 3:
        raise ValueError("Contour plot requires 3 columns (x, y, z)")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    z = data.iloc[:, 2].values

    # Create grid
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values
    zi = griddata((x, y), z, (xi, yi), method='cubic')

    # Create contour plot
    contour = ax.contourf(xi, yi, zi, levels=levels, cmap=cmap, **kwargs)
    plt.colorbar(contour, ax=ax)

    ax.set_xlabel(data.columns[0])
    ax.set_ylabel(data.columns[1])


def _create_3d_surface(data: pd.DataFrame, config):
    """Create 3D surface plot."""
    from mpl_toolkits.mplot3d import Axes3D

    kwargs = config.extra_kwargs
    cmap = kwargs.pop("cmap", "viridis")

    # Expect 3 columns: x, y, z
    if len(data.columns) < 3:
        raise ValueError("3D surface plot requires 3 columns (x, y, z)")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    z = data.iloc[:, 2].values

    # Create grid
    xi = np.linspace(x.min(), x.max(), 50)
    yi = np.linspace(y.min(), y.max(), 50)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values
    zi = griddata((x, y), z, (xi, yi), method='cubic')

    # Create 3D plot
    fig = plt.figure(figsize=config.figsize)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(xi, yi, zi, cmap=cmap, **kwargs)

    ax.set_xlabel(data.columns[0])
    ax.set_ylabel(data.columns[1])
    ax.set_zlabel(data.columns[2])

    fig.colorbar(surf, ax=ax, shrink=0.5)

    return fig


def _create_vector_field(ax: Axes, data: pd.DataFrame, config):
    """Create vector field plot."""
    kwargs = config.extra_kwargs

    # Expect 4 columns: x, y, u, v
    if len(data.columns) < 4:
        raise ValueError("Vector field requires 4 columns (x, y, u, v)")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    u = data.iloc[:, 2].values
    v = data.iloc[:, 3].values

    # Create quiver plot
    ax.quiver(x, y, u, v, **kwargs)

    ax.set_xlabel(data.columns[0])
    ax.set_ylabel(data.columns[1])
    ax.set_aspect('equal')


def create_scientific_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create scientific charts using plotly.

    Args:
        data: Input data
        config: Plot configuration

    Returns:
        Plotly figure
    """
    chart_type = config.chart_type

    if chart_type == "sci_scatter_regression":
        return _create_scatter_regression_plotly(data, config)
    elif chart_type == "sci_contour":
        return _create_contour_plotly(data, config)
    elif chart_type == "sci_3d_surface":
        return _create_3d_surface_plotly(data, config)
    else:
        raise ValueError(f"Unknown scientific chart type: {chart_type}")


def _create_scatter_regression_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create scatter plot with regression using plotly."""
    kwargs = config.extra_kwargs

    if len(data.columns) < 2:
        raise ValueError("Scatter regression requires at least 2 columns")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values

    # Remove NaN values
    mask = ~(np.isnan(x) | np.isnan(y))
    x = x[mask]
    y = y[mask]

    fig = go.Figure()

    # Scatter plot
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Data',
        marker=dict(size=8, opacity=0.6)
    ))

    # Regression line
    if kwargs.get("show_regression", True):
        slope, intercept, r_value, _, _ = stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        fig.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name='Regression',
            line=dict(color='red', width=2)
        ))

        # Add annotation
        if kwargs.get("show_equation", True) or kwargs.get("show_r2", True):
            text_items = []
            if kwargs.get("show_equation", True):
                text_items.append(f'y = {slope:.3f}x + {intercept:.3f}')
            if kwargs.get("show_r2", True):
                text_items.append(f'R² = {r_value**2:.3f}')

            fig.add_annotation(
                x=0.05,
                y=0.95,
                xref="paper",
                yref="paper",
                text='<br>'.join(text_items),
                showarrow=False,
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )

    fig.update_xaxes(title_text=data.columns[0])
    fig.update_yaxes(title_text=data.columns[1])

    return fig


def _create_contour_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create contour plot with plotly."""
    kwargs = config.extra_kwargs

    if len(data.columns) < 3:
        raise ValueError("Contour plot requires 3 columns (x, y, z)")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    z = data.iloc[:, 2].values

    # Create grid
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values
    zi = griddata((x, y), z, (xi, yi), method='cubic')

    fig = go.Figure(data=go.Contour(
        x=xi[0],
        y=yi[:, 0],
        z=zi,
        colorscale=kwargs.get("colorscale", "Viridis"),
        contours=dict(
            coloring='heatmap',
            showlabels=True
        )
    ))

    fig.update_xaxes(title_text=data.columns[0])
    fig.update_yaxes(title_text=data.columns[1])

    return fig


def _create_3d_surface_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create 3D surface plot with plotly."""
    kwargs = config.extra_kwargs

    if len(data.columns) < 3:
        raise ValueError("3D surface plot requires 3 columns (x, y, z)")

    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    z = data.iloc[:, 2].values

    # Create grid
    xi = np.linspace(x.min(), x.max(), 50)
    yi = np.linspace(y.min(), y.max(), 50)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values
    zi = griddata((x, y), z, (xi, yi), method='cubic')

    fig = go.Figure(data=[go.Surface(
        x=xi,
        y=yi,
        z=zi,
        colorscale=kwargs.get("colorscale", "Viridis")
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title=data.columns[0],
            yaxis_title=data.columns[1],
            zaxis_title=data.columns[2]
        )
    )

    return fig
