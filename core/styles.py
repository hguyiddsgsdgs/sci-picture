"""Style management for scientific plots."""

from enum import Enum
from typing import Dict, Optional

import matplotlib.pyplot as plt
import seaborn as sns


class PublicationStyle(str, Enum):
    """Publication venue styles."""

    NATURE = "nature"
    SCIENCE = "science"
    IEEE = "ieee"
    ACM = "acm"
    SPRINGER = "springer"
    DEFAULT = "default"
    MINIMAL = "minimal"
    COLORBLIND = "colorblind"


class StyleManager:
    """Manage plotting styles."""

    def __init__(self):
        self._styles = self._initialize_styles()
        self._current_style = None

    def _initialize_styles(self) -> Dict[str, Dict]:
        """Initialize style configurations."""
        return {
            PublicationStyle.NATURE: {
                "font.family": "sans-serif",
                "font.sans-serif": ["Arial", "Helvetica"],
                "font.size": 8,
                "axes.labelsize": 8,
                "axes.titlesize": 9,
                "xtick.labelsize": 7,
                "ytick.labelsize": 7,
                "legend.fontsize": 7,
                "figure.titlesize": 10,
                "axes.linewidth": 0.5,
                "grid.linewidth": 0.5,
                "lines.linewidth": 1.0,
                "patch.linewidth": 0.5,
                "xtick.major.width": 0.5,
                "ytick.major.width": 0.5,
                "figure.dpi": 300,
                "savefig.dpi": 300,
                "axes.spines.top": False,
                "axes.spines.right": False,
            },
            PublicationStyle.SCIENCE: {
                "font.family": "sans-serif",
                "font.sans-serif": ["Helvetica", "Arial"],
                "font.size": 7,
                "axes.labelsize": 7,
                "axes.titlesize": 8,
                "xtick.labelsize": 6,
                "ytick.labelsize": 6,
                "legend.fontsize": 6,
                "figure.titlesize": 9,
                "axes.linewidth": 0.5,
                "grid.linewidth": 0.5,
                "lines.linewidth": 1.0,
                "figure.dpi": 300,
                "savefig.dpi": 300,
                "axes.spines.top": False,
                "axes.spines.right": False,
            },
            PublicationStyle.IEEE: {
                "font.family": "serif",
                "font.serif": ["Times New Roman", "Times"],
                "font.size": 8,
                "axes.labelsize": 8,
                "axes.titlesize": 9,
                "xtick.labelsize": 8,
                "ytick.labelsize": 8,
                "legend.fontsize": 8,
                "figure.titlesize": 10,
                "axes.linewidth": 0.8,
                "grid.linewidth": 0.5,
                "lines.linewidth": 1.5,
                "figure.dpi": 300,
                "savefig.dpi": 300,
            },
            PublicationStyle.ACM: {
                "font.family": "sans-serif",
                "font.sans-serif": ["Helvetica", "Arial"],
                "font.size": 9,
                "axes.labelsize": 9,
                "axes.titlesize": 10,
                "xtick.labelsize": 8,
                "ytick.labelsize": 8,
                "legend.fontsize": 8,
                "figure.titlesize": 11,
                "axes.linewidth": 0.8,
                "grid.linewidth": 0.5,
                "lines.linewidth": 1.5,
                "figure.dpi": 300,
                "savefig.dpi": 300,
            },
            PublicationStyle.SPRINGER: {
                "font.family": "serif",
                "font.serif": ["Times New Roman", "Times"],
                "font.size": 8,
                "axes.labelsize": 8,
                "axes.titlesize": 9,
                "xtick.labelsize": 7,
                "ytick.labelsize": 7,
                "legend.fontsize": 7,
                "figure.titlesize": 10,
                "axes.linewidth": 0.6,
                "grid.linewidth": 0.5,
                "lines.linewidth": 1.2,
                "figure.dpi": 300,
                "savefig.dpi": 300,
            },
            PublicationStyle.DEFAULT: {
                "font.size": 12,
                "axes.labelsize": 12,
                "axes.titlesize": 14,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "figure.titlesize": 16,
                "figure.dpi": 100,
                "savefig.dpi": 300,
            },
            PublicationStyle.MINIMAL: {
                "font.family": "sans-serif",
                "font.sans-serif": ["Arial", "Helvetica"],
                "font.size": 10,
                "axes.labelsize": 10,
                "axes.titlesize": 11,
                "xtick.labelsize": 9,
                "ytick.labelsize": 9,
                "legend.fontsize": 9,
                "figure.titlesize": 12,
                "axes.linewidth": 0.5,
                "grid.linewidth": 0.3,
                "lines.linewidth": 1.5,
                "axes.spines.top": False,
                "axes.spines.right": False,
                "axes.spines.left": False,
                "axes.spines.bottom": False,
                "xtick.major.size": 0,
                "ytick.major.size": 0,
                "figure.dpi": 150,
                "savefig.dpi": 300,
            },
            PublicationStyle.COLORBLIND: {
                "font.size": 12,
                "axes.labelsize": 12,
                "axes.titlesize": 14,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
                "figure.titlesize": 16,
                "axes.prop_cycle": plt.cycler(
                    color=[
                        "#0173B2",  # Blue
                        "#DE8F05",  # Orange
                        "#029E73",  # Green
                        "#CC78BC",  # Purple
                        "#CA9161",  # Brown
                        "#949494",  # Gray
                        "#ECE133",  # Yellow
                        "#56B4E9",  # Sky blue
                    ]
                ),
                "figure.dpi": 100,
                "savefig.dpi": 300,
            },
        }

    def apply_style(self, style_name: str):
        """Apply a style to matplotlib.

        Args:
            style_name: Name of the style to apply
        """
        if style_name not in self._styles:
            raise ValueError(f"Unknown style: {style_name}. Available: {list(self._styles.keys())}")

        style_config = self._styles[style_name]
        plt.rcParams.update(style_config)
        self._current_style = style_name

        # Apply seaborn style for better defaults
        if style_name == PublicationStyle.MINIMAL:
            sns.set_style("white")
        elif style_name == PublicationStyle.COLORBLIND:
            sns.set_palette("colorblind")
        else:
            sns.set_style("ticks")

    def get_color_palette(self, style_name: Optional[str] = None, n_colors: int = 10) -> list:
        """Get color palette for a style.

        Args:
            style_name: Style name. If None, uses current style.
            n_colors: Number of colors to return

        Returns:
            List of color hex codes
        """
        style_name = style_name or self._current_style or PublicationStyle.DEFAULT

        if style_name == PublicationStyle.COLORBLIND:
            return [
                "#0173B2",
                "#DE8F05",
                "#029E73",
                "#CC78BC",
                "#CA9161",
                "#949494",
                "#ECE133",
                "#56B4E9",
            ][:n_colors]
        elif style_name in [PublicationStyle.NATURE, PublicationStyle.SCIENCE]:
            # Nature/Science style colors
            return sns.color_palette("deep", n_colors).as_hex()
        elif style_name == PublicationStyle.IEEE:
            # IEEE style colors
            return sns.color_palette("muted", n_colors).as_hex()
        else:
            # Default palette
            return sns.color_palette("tab10", n_colors).as_hex()

    def list_styles(self) -> list[str]:
        """List all available styles."""
        return list(self._styles.keys())

    def get_current_style(self) -> Optional[str]:
        """Get the currently applied style."""
        return self._current_style

    def reset_style(self):
        """Reset to matplotlib defaults."""
        plt.rcdefaults()
        self._current_style = None

    def create_custom_style(self, name: str, config: Dict):
        """Create a custom style.

        Args:
            name: Name for the custom style
            config: Style configuration dictionary
        """
        self._styles[name] = config

    def get_style_config(self, style_name: str) -> Dict:
        """Get the configuration for a style.

        Args:
            style_name: Name of the style

        Returns:
            Style configuration dictionary
        """
        if style_name not in self._styles:
            raise ValueError(f"Unknown style: {style_name}")
        return self._styles[style_name].copy()
