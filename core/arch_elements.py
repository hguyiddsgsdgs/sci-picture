"""Visual elements for architecture diagrams."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Tuple, List, Optional, Dict, Any


class ArchElement:
    """Base class for architecture diagram elements."""

    def __init__(self, position: Tuple[float, float], size: Tuple[float, float]):
        self.position = position
        self.size = size
        self.color = "#4A90E2"
        self.label = ""

    def draw(self, ax):
        """Draw the element on the given axes."""
        raise NotImplementedError


class Box3D(ArchElement):
    """3D box element for feature maps and tensors."""

    def __init__(self, position: Tuple[float, float, float],
                 size: Tuple[float, float, float],
                 color: str = "#4A90E2",
                 alpha: float = 0.7,
                 edge_color: str = "#2E5C8A",
                 texture: str = "solid"):
        """
        Args:
            position: (x, y, z) position
            size: (width, height, depth)
            color: Fill color
            alpha: Transparency
            edge_color: Edge color
            texture: 'solid', 'grid', 'diagonal', 'gradient'
        """
        self.position = position
        self.size = size
        self.color = color
        self.alpha = alpha
        self.edge_color = edge_color
        self.texture = texture

    def draw(self, ax):
        """Draw 3D box on 3D axes."""
        x, y, z = self.position
        w, h, d = self.size

        # Define vertices
        vertices = [
            [x, y, z], [x+w, y, z], [x+w, y+h, z], [x, y+h, z],  # Front
            [x, y, z+d], [x+w, y, z+d], [x+w, y+h, z+d], [x, y+h, z+d]  # Back
        ]

        # Define faces
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Bottom
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Top
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Front
            [vertices[4], vertices[5], vertices[6], vertices[7]]   # Back
        ]

        # Apply texture
        if self.texture == "gradient":
            colors = self._create_gradient_colors()
        else:
            colors = [self.color] * 6

        # Create collection
        collection = Poly3DCollection(faces, alpha=self.alpha,
                                     facecolors=colors,
                                     edgecolors=self.edge_color,
                                     linewidths=1.5)
        ax.add_collection3d(collection)

        # Add texture patterns
        if self.texture == "grid":
            self._add_grid_texture(ax, vertices)
        elif self.texture == "diagonal":
            self._add_diagonal_texture(ax, vertices)

    def _create_gradient_colors(self) -> List[str]:
        """Create gradient colors for faces."""
        from matplotlib.colors import to_rgb
        base_rgb = to_rgb(self.color)
        colors = []
        for i, factor in enumerate([0.6, 1.0, 0.7, 0.9, 0.8, 0.5]):
            rgb = tuple(c * factor for c in base_rgb)
            colors.append(rgb)
        return colors

    def _add_grid_texture(self, ax, vertices):
        """Add grid texture to front face."""
        x, y, z = self.position
        w, h, d = self.size

        # Draw grid lines
        grid_lines = 5
        for i in range(grid_lines + 1):
            # Vertical lines
            xi = x + (w * i / grid_lines)
            ax.plot([xi, xi], [y, y+h], [z, z],
                   color=self.edge_color, alpha=0.3, linewidth=0.5)
            # Horizontal lines
            yi = y + (h * i / grid_lines)
            ax.plot([x, x+w], [yi, yi], [z, z],
                   color=self.edge_color, alpha=0.3, linewidth=0.5)

    def _add_diagonal_texture(self, ax, vertices):
        """Add diagonal stripe texture."""
        x, y, z = self.position
        w, h, d = self.size

        # Draw diagonal lines
        num_lines = 8
        for i in range(num_lines):
            offset = (w + h) * i / num_lines
            # Calculate line endpoints
            if offset < w:
                x1, y1 = x + offset, y
                x2, y2 = x, y + offset
            else:
                x1, y1 = x + w, y + (offset - w)
                x2, y2 = x + (offset - h), y + h

            if y2 <= y + h and x2 >= x:
                ax.plot([x1, x2], [y1, y2], [z, z],
                       color=self.edge_color, alpha=0.2, linewidth=0.8)


class RoundedBox(ArchElement):
    """Rounded rectangle for operations/layers."""

    def __init__(self, position: Tuple[float, float],
                 size: Tuple[float, float],
                 label: str = "",
                 color: str = "#FFD700",
                 edge_color: str = "#DAA520",
                 text_color: str = "#000000",
                 alpha: float = 0.9,
                 corner_radius: float = 0.1):
        self.position = position
        self.size = size
        self.label = label
        self.color = color
        self.edge_color = edge_color
        self.text_color = text_color
        self.alpha = alpha
        self.corner_radius = corner_radius

    def draw(self, ax):
        """Draw rounded box on 2D axes."""
        x, y = self.position
        w, h = self.size

        # Create rounded box
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad={self.corner_radius}",
            facecolor=self.color,
            edgecolor=self.edge_color,
            alpha=self.alpha,
            linewidth=2
        )
        ax.add_patch(box)

        # Add label
        if self.label:
            ax.text(x + w/2, y + h/2, self.label,
                   ha='center', va='center',
                   fontsize=10, fontweight='bold',
                   color=self.text_color)


class Arrow3D(ArchElement):
    """3D arrow for data flow."""

    def __init__(self, start: Tuple[float, float, float],
                 end: Tuple[float, float, float],
                 color: str = "#333333",
                 width: float = 2.0,
                 arrow_style: str = "->"):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.arrow_style = arrow_style

    def draw(self, ax):
        """Draw 3D arrow."""
        from matplotlib.patches import FancyArrowPatch
        from mpl_toolkits.mplot3d import proj3d

        class Arrow3D(FancyArrowPatch):
            def __init__(self, xs, ys, zs, *args, **kwargs):
                FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
                self._verts3d = xs, ys, zs

            def do_3d_projection(self, renderer=None):
                xs3d, ys3d, zs3d = self._verts3d
                xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
                self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
                return np.min(zs)

        arrow = Arrow3D(
            [self.start[0], self.end[0]],
            [self.start[1], self.end[1]],
            [self.start[2], self.end[2]],
            mutation_scale=20,
            lw=self.width,
            arrowstyle=self.arrow_style,
            color=self.color
        )
        ax.add_artist(arrow)


class Arrow2D(ArchElement):
    """2D arrow for data flow."""

    def __init__(self, start: Tuple[float, float],
                 end: Tuple[float, float],
                 color: str = "#333333",
                 width: float = 2.0,
                 arrow_style: str = "->",
                 curve: float = 0.0):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.arrow_style = arrow_style
        self.curve = curve

    def draw(self, ax):
        """Draw 2D arrow."""
        if self.curve == 0:
            # Straight arrow
            arrow = FancyArrowPatch(
                self.start, self.end,
                arrowstyle=self.arrow_style,
                color=self.color,
                linewidth=self.width,
                mutation_scale=20
            )
        else:
            # Curved arrow
            arrow = FancyArrowPatch(
                self.start, self.end,
                arrowstyle=self.arrow_style,
                color=self.color,
                linewidth=self.width,
                mutation_scale=20,
                connectionstyle=f"arc3,rad={self.curve}"
            )
        ax.add_patch(arrow)


class Label:
    """Text label for annotations."""

    def __init__(self, position: Tuple[float, float],
                 text: str,
                 fontsize: int = 10,
                 color: str = "#000000",
                 fontweight: str = "normal",
                 ha: str = "center",
                 va: str = "center",
                 bbox: Optional[Dict] = None):
        self.position = position
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.fontweight = fontweight
        self.ha = ha
        self.va = va
        self.bbox = bbox

    def draw(self, ax):
        """Draw label."""
        ax.text(self.position[0], self.position[1], self.text,
               fontsize=self.fontsize,
               color=self.color,
               fontweight=self.fontweight,
               ha=self.ha,
               va=self.va,
               bbox=self.bbox)


class ColorScheme:
    """Color schemes for architecture diagrams."""

    # Transformer style (blue-green gradient)
    TRANSFORMER = {
        "attention": "#87CEEB",  # Sky blue
        "ffn": "#98FB98",        # Pale green
        "norm": "#F0E68C",       # Khaki
        "embedding": "#DDA0DD",  # Plum
        "output": "#FFB6C1",     # Light pink
        "arrow": "#333333"       # Dark gray
    }

    # Multi-modal style (from reference image 1)
    MULTIMODAL = {
        "text": "#FFD700",       # Gold
        "image": "#87CEEB",      # Sky blue
        "fusion": "#98FB98",     # Pale green
        "attention": "#F0E68C",  # Khaki
        "output": "#FFB6C1",     # Light pink
        "arrow": "#333333"
    }

    # Modern gradient style
    MODERN = {
        "layer1": "#667EEA",     # Purple-blue
        "layer2": "#764BA2",     # Purple
        "layer3": "#F093FB",     # Pink
        "layer4": "#4FACFE",     # Blue
        "layer5": "#00F2FE",     # Cyan
        "arrow": "#2D3748"
    }

    # Academic style (Nature/Science)
    ACADEMIC = {
        "primary": "#0C4B8E",    # Deep blue
        "secondary": "#2E86AB",  # Medium blue
        "accent": "#A23B72",     # Purple
        "highlight": "#F18F01",  # Orange
        "neutral": "#C73E1D",    # Red
        "arrow": "#1A1A1A"
    }

    @staticmethod
    def get_scheme(name: str) -> Dict[str, str]:
        """Get color scheme by name."""
        schemes = {
            "transformer": ColorScheme.TRANSFORMER,
            "multimodal": ColorScheme.MULTIMODAL,
            "modern": ColorScheme.MODERN,
            "academic": ColorScheme.ACADEMIC
        }
        return schemes.get(name.lower(), ColorScheme.TRANSFORMER)
