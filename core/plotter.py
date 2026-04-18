"""Main scientific plotter class."""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

from .models import PlotConfig
from .styles import StyleManager
from .templates import TemplateManager
from .utils import CacheManager, DataLoader


class Figure:
    """Wrapper for matplotlib or plotly figures."""

    def __init__(self, fig: Union[plt.Figure, go.Figure], backend: str):
        self.fig = fig
        self.backend = backend

    def save(
        self,
        path: Union[str, Path],
        format: Optional[str] = None,
        dpi: int = 300,
        bbox_inches: str = "tight",
        **kwargs,
    ):
        """Save figure to file."""
        path = Path(path)
        if format is None:
            format = path.suffix[1:]  # Remove the dot

        if self.backend == "matplotlib":
            self.fig.savefig(path, format=format, dpi=dpi, bbox_inches=bbox_inches, **kwargs)
        elif self.backend == "plotly":
            if format in ["png", "jpg", "jpeg", "webp", "svg", "pdf", "eps"]:
                self.fig.write_image(str(path), format=format, **kwargs)
            elif format == "html":
                self.fig.write_html(str(path), **kwargs)
            else:
                raise ValueError(f"Unsupported format for plotly: {format}")

    def show(self):
        """Display the figure."""
        if self.backend == "matplotlib":
            plt.show()
        elif self.backend == "plotly":
            self.fig.show()


class ScientificPlotter:
    """Main plotter class for scientific visualizations."""

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        enable_cache: bool = True,
    ):
        """Initialize the plotter.

        Args:
            cache_dir: Directory for caching. If None, uses default.
            enable_cache: Whether to enable caching.
        """
        self.style_manager = StyleManager()
        self.template_manager = TemplateManager()
        self.data_loader = DataLoader()
        self.cache_manager = CacheManager(cache_dir) if enable_cache else None

    def create_chart(
        self,
        data: Union[pd.DataFrame, Dict, str, Path],
        config: Union[PlotConfig, Dict],
        use_cache: bool = True,
    ) -> Figure:
        """Create a chart from data and configuration.

        Args:
            data: Input data (DataFrame, dict, or path to file)
            config: Plot configuration
            use_cache: Whether to use cache

        Returns:
            Figure object
        """
        # Load data if needed
        if isinstance(data, (str, Path)):
            data = self.data_loader.load(data)
        elif isinstance(data, dict):
            data = pd.DataFrame(data)

        # Parse config
        if isinstance(config, dict):
            config = PlotConfig(**config)

        # Check cache
        if use_cache and self.cache_manager:
            cache_key = self._generate_cache_key(data, config)
            cached_fig = self.cache_manager.get(cache_key)
            if cached_fig is not None:
                return cached_fig

        # Apply style
        self.style_manager.apply_style(config.style)

        # Create chart based on type
        if config.interactive:
            fig = self._create_plotly_chart(data, config)
            result = Figure(fig, "plotly")
        else:
            fig = self._create_matplotlib_chart(data, config)
            result = Figure(fig, "matplotlib")

        # Cache result
        if use_cache and self.cache_manager:
            self.cache_manager.set(cache_key, result)

        return result

    def _create_matplotlib_chart(self, data: pd.DataFrame, config: PlotConfig) -> plt.Figure:
        """Create a matplotlib chart."""
        from charts import (
            create_comparison_chart,
            create_ml_chart,
            create_scientific_chart,
            create_statistical_chart,
            create_timeseries_chart,
        )

        fig, ax = plt.subplots(figsize=config.figsize, dpi=config.dpi)

        # Route to appropriate chart creator
        if config.chart_type.startswith("stat_"):
            create_statistical_chart(ax, data, config)
        elif config.chart_type.startswith("ts_"):
            create_timeseries_chart(ax, data, config)
        elif config.chart_type.startswith("comp_"):
            create_comparison_chart(ax, data, config)
        elif config.chart_type.startswith("sci_"):
            create_scientific_chart(ax, data, config)
        elif config.chart_type.startswith("ml_"):
            create_ml_chart(ax, data, config)
        else:
            raise ValueError(f"Unknown chart type: {config.chart_type}")

        # Apply common settings
        if config.title:
            ax.set_title(config.title, fontsize=config.font_size + 2)
        if config.xlabel:
            ax.set_xlabel(config.xlabel, fontsize=config.font_size)
        if config.ylabel:
            ax.set_ylabel(config.ylabel, fontsize=config.font_size)
        if config.show_grid:
            ax.grid(True, alpha=0.3)
        if config.show_legend:
            ax.legend(fontsize=config.font_size - 2)

        plt.tight_layout()
        return fig

    def _create_plotly_chart(self, data: pd.DataFrame, config: PlotConfig) -> go.Figure:
        """Create a plotly chart."""
        from charts import (
            create_comparison_chart_plotly,
            create_ml_chart_plotly,
            create_scientific_chart_plotly,
            create_statistical_chart_plotly,
            create_timeseries_chart_plotly,
        )

        # Route to appropriate chart creator
        if config.chart_type.startswith("stat_"):
            fig = create_statistical_chart_plotly(data, config)
        elif config.chart_type.startswith("ts_"):
            fig = create_timeseries_chart_plotly(data, config)
        elif config.chart_type.startswith("comp_"):
            fig = create_comparison_chart_plotly(data, config)
        elif config.chart_type.startswith("sci_"):
            fig = create_scientific_chart_plotly(data, config)
        elif config.chart_type.startswith("ml_"):
            fig = create_ml_chart_plotly(data, config)
        else:
            raise ValueError(f"Unknown chart type: {config.chart_type}")

        # Apply common settings
        fig.update_layout(
            title=config.title,
            xaxis_title=config.xlabel,
            yaxis_title=config.ylabel,
            showlegend=config.show_legend,
            template="plotly_white",
            font=dict(size=config.font_size),
        )

        if config.show_grid:
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(128,128,128,0.2)")

        return fig

    def _generate_cache_key(self, data: pd.DataFrame, config: PlotConfig) -> str:
        """Generate a cache key from data and config."""
        # Hash data
        data_hash = hashlib.md5(pd.util.hash_pandas_object(data).values).hexdigest()

        # Hash config
        config_str = json.dumps(config.model_dump(), sort_keys=True)
        config_hash = hashlib.md5(config_str.encode()).hexdigest()

        return f"{data_hash}_{config_hash}"

    def batch_create(
        self,
        data_list: List[Union[pd.DataFrame, Dict, str, Path]],
        config_list: List[Union[PlotConfig, Dict]],
        output_dir: Union[str, Path],
        format: str = "png",
        parallel: bool = False,
    ) -> List[Path]:
        """Create multiple charts in batch.

        Args:
            data_list: List of data sources
            config_list: List of configurations
            output_dir: Output directory
            format: Output format
            parallel: Whether to use parallel processing

        Returns:
            List of output file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        output_paths = []

        if parallel:
            # TODO: Implement parallel processing
            pass

        for i, (data, config) in enumerate(zip(data_list, config_list)):
            fig = self.create_chart(data, config)
            output_path = output_dir / f"chart_{i:03d}.{format}"
            fig.save(output_path, format=format)
            output_paths.append(output_path)

        return output_paths

    def create_from_template(
        self,
        template_name: str,
        data: Union[pd.DataFrame, Dict, str, Path],
        **kwargs,
    ) -> Figure:
        """Create a chart from a template.

        Args:
            template_name: Name of the template
            data: Input data
            **kwargs: Additional parameters to override template

        Returns:
            Figure object
        """
        config = self.template_manager.get_template(template_name)

        # Override with kwargs
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return self.create_chart(data, config)

    def list_chart_types(self) -> List[str]:
        """List all available chart types."""
        return [
            # Statistical
            "stat_boxplot",
            "stat_violin",
            "stat_distribution",
            "stat_correlation_heatmap",
            "stat_pairplot",
            # Time series
            "ts_line",
            "ts_area",
            "ts_candlestick",
            "ts_decomposition",
            # Comparison
            "comp_bar",
            "comp_grouped_bar",
            "comp_stacked_bar",
            "comp_radar",
            # Scientific
            "sci_scatter_regression",
            "sci_contour",
            "sci_3d_surface",
            "sci_vector_field",
            # ML/AI
            "ml_confusion_matrix",
            "ml_roc_curve",
            "ml_learning_curve",
            "ml_feature_importance",
            "ml_precision_recall",
        ]

    def list_styles(self) -> List[str]:
        """List all available styles."""
        return self.style_manager.list_styles()

    def list_templates(self) -> List[str]:
        """List all available templates."""
        return self.template_manager.list_templates()
