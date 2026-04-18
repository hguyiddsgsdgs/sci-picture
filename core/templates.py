"""Template management for common chart configurations."""

from typing import Dict, List

from .models import PlotConfig


class TemplateManager:
    """Manage chart templates."""

    def __init__(self):
        self._templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict[str, PlotConfig]:
        """Initialize built-in templates."""
        return {
            # Statistical templates
            "boxplot_comparison": PlotConfig(
                chart_type="stat_boxplot",
                style="nature",
                figsize=(8, 6),
                show_grid=True,
                extra_kwargs={"showfliers": True, "notch": False},
            ),
            "distribution_analysis": PlotConfig(
                chart_type="stat_distribution",
                style="science",
                figsize=(10, 6),
                show_grid=False,
                extra_kwargs={"kde": True, "bins": 30},
            ),
            "correlation_matrix": PlotConfig(
                chart_type="stat_correlation_heatmap",
                style="minimal",
                figsize=(10, 8),
                show_grid=False,
                extra_kwargs={"annot": True, "cmap": "coolwarm", "center": 0},
            ),
            # Time series templates
            "timeseries_basic": PlotConfig(
                chart_type="ts_line",
                style="ieee",
                figsize=(12, 6),
                show_grid=True,
                extra_kwargs={"marker": "o", "markersize": 4},
            ),
            "timeseries_forecast": PlotConfig(
                chart_type="ts_line",
                style="nature",
                figsize=(14, 6),
                show_grid=True,
                extra_kwargs={
                    "show_confidence": True,
                    "confidence_alpha": 0.2,
                },
            ),
            # Comparison templates
            "bar_comparison": PlotConfig(
                chart_type="comp_bar",
                style="acm",
                figsize=(10, 6),
                show_grid=True,
                extra_kwargs={"error_bars": True},
            ),
            "grouped_comparison": PlotConfig(
                chart_type="comp_grouped_bar",
                style="nature",
                figsize=(12, 6),
                show_grid=True,
                extra_kwargs={"bar_width": 0.35},
            ),
            "radar_comparison": PlotConfig(
                chart_type="comp_radar",
                style="minimal",
                figsize=(8, 8),
                show_grid=True,
                extra_kwargs={"fill": True, "alpha": 0.25},
            ),
            # Scientific templates
            "scatter_regression": PlotConfig(
                chart_type="sci_scatter_regression",
                style="nature",
                figsize=(8, 8),
                show_grid=True,
                extra_kwargs={
                    "show_regression": True,
                    "show_confidence": True,
                    "show_equation": True,
                    "show_r2": True,
                },
            ),
            "contour_plot": PlotConfig(
                chart_type="sci_contour",
                style="science",
                figsize=(10, 8),
                show_grid=False,
                extra_kwargs={"levels": 20, "cmap": "viridis"},
            ),
            "surface_3d": PlotConfig(
                chart_type="sci_3d_surface",
                style="default",
                figsize=(10, 8),
                interactive=True,
                extra_kwargs={"colorscale": "Viridis"},
            ),
            # ML/AI templates
            "confusion_matrix": PlotConfig(
                chart_type="ml_confusion_matrix",
                style="minimal",
                figsize=(8, 8),
                show_grid=False,
                extra_kwargs={
                    "annot": True,
                    "fmt": "d",
                    "cmap": "Blues",
                    "normalize": False,
                },
            ),
            "roc_curve": PlotConfig(
                chart_type="ml_roc_curve",
                style="nature",
                figsize=(8, 8),
                show_grid=True,
                extra_kwargs={
                    "show_diagonal": True,
                    "show_auc": True,
                },
            ),
            "learning_curve": PlotConfig(
                chart_type="ml_learning_curve",
                style="ieee",
                figsize=(10, 6),
                show_grid=True,
                extra_kwargs={
                    "show_std": True,
                    "std_alpha": 0.2,
                },
            ),
            "feature_importance": PlotConfig(
                chart_type="ml_feature_importance",
                style="nature",
                figsize=(10, 8),
                show_grid=True,
                extra_kwargs={
                    "top_n": 20,
                    "horizontal": True,
                },
            ),
            # Publication-ready templates
            "nature_figure": PlotConfig(
                chart_type="sci_scatter_regression",
                style="nature",
                figsize=(3.5, 3.5),  # Nature single column width
                dpi=300,
                font_size=8,
                show_grid=False,
                extra_kwargs={"marker_size": 3},
            ),
            "science_figure": PlotConfig(
                chart_type="ts_line",
                style="science",
                figsize=(3.3, 2.5),  # Science single column width
                dpi=300,
                font_size=7,
                show_grid=False,
            ),
            "ieee_figure": PlotConfig(
                chart_type="comp_bar",
                style="ieee",
                figsize=(3.5, 2.5),  # IEEE single column width
                dpi=300,
                font_size=8,
                show_grid=True,
            ),
        }

    def get_template(self, name: str) -> PlotConfig:
        """Get a template by name.

        Args:
            name: Template name

        Returns:
            PlotConfig object

        Raises:
            ValueError: If template not found
        """
        if name not in self._templates:
            raise ValueError(f"Unknown template: {name}. Available: {self.list_templates()}")
        return self._templates[name].model_copy(deep=True)

    def list_templates(self) -> List[str]:
        """List all available templates."""
        return list(self._templates.keys())

    def add_template(self, name: str, config: PlotConfig):
        """Add a custom template.

        Args:
            name: Template name
            config: PlotConfig object
        """
        self._templates[name] = config

    def remove_template(self, name: str):
        """Remove a template.

        Args:
            name: Template name
        """
        if name in self._templates:
            del self._templates[name]

    def get_templates_by_category(self) -> Dict[str, List[str]]:
        """Get templates grouped by category.

        Returns:
            Dictionary mapping category to list of template names
        """
        categories = {
            "Statistical": [],
            "Time Series": [],
            "Comparison": [],
            "Scientific": [],
            "ML/AI": [],
            "Publication": [],
        }

        for name in self._templates:
            if name.startswith("boxplot") or name.startswith("distribution") or name.startswith("correlation"):
                categories["Statistical"].append(name)
            elif name.startswith("timeseries"):
                categories["Time Series"].append(name)
            elif name.startswith("bar") or name.startswith("grouped") or name.startswith("radar"):
                categories["Comparison"].append(name)
            elif name.startswith("scatter") or name.startswith("contour") or name.startswith("surface"):
                categories["Scientific"].append(name)
            elif name.startswith("confusion") or name.startswith("roc") or name.startswith("learning") or name.startswith("feature"):
                categories["ML/AI"].append(name)
            elif name.endswith("_figure"):
                categories["Publication"].append(name)

        return {k: v for k, v in categories.items() if v}  # Remove empty categories
