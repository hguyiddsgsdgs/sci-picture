"""Renderer for architecture diagrams with 3D effects."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from typing import List, Tuple, Dict, Any, Optional

try:
    from .arch_parser import ArchitectureSpec, LayerSpec, ConnectionSpec
    from .arch_elements import Box3D, RoundedBox, Arrow2D, Arrow3D, Label, ColorScheme
except ImportError:
    from arch_parser import ArchitectureSpec, LayerSpec, ConnectionSpec
    from arch_elements import Box3D, RoundedBox, Arrow2D, Arrow3D, Label, ColorScheme


class ArchitectureRenderer:
    """Render architecture diagrams with publication-quality styling."""

    def __init__(self, spec: ArchitectureSpec, figsize: Tuple[float, float] = (12, 8)):
        self.spec = spec
        self.figsize = figsize
        self.colors = ColorScheme.get_scheme(spec.style)
        self.layer_positions = {}
        self.use_3d = self._should_use_3d()

    def _should_use_3d(self) -> bool:
        """Determine if 3D rendering is needed."""
        # Use 3D for certain layer types or if explicitly requested
        for layer in self.spec.layers:
            if layer.type in ["input", "conv"] or layer.details.get("3d", False):
                return True
        return False

    def render(self) -> plt.Figure:
        """Render the complete architecture diagram."""
        if self.use_3d:
            return self._render_3d()
        else:
            return self._render_2d()

    def _render_2d(self) -> plt.Figure:
        """Render 2D architecture diagram."""
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Calculate layout
        self._calculate_layout_2d()

        # Draw layers
        for layer in self.spec.layers:
            self._draw_layer_2d(ax, layer)

        # Draw connections
        for conn in self.spec.connections:
            self._draw_connection_2d(ax, conn)

        # Add title
        if self.spec.name:
            fig.suptitle(self.spec.name, fontsize=16, fontweight='bold', y=0.98)

        plt.tight_layout()
        return fig

    def _render_3d(self) -> plt.Figure:
        """Render 3D architecture diagram."""
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')

        # Calculate layout
        self._calculate_layout_3d()

        # Draw layers
        for layer in self.spec.layers:
            if layer.details.get("3d", False) or layer.type in ["input", "conv"]:
                self._draw_layer_3d(ax, layer)
            else:
                # Draw 2D elements in 3D space
                self._draw_layer_2d_in_3d(ax, layer)

        # Draw connections
        for conn in self.spec.connections:
            self._draw_connection_3d(ax, conn)

        # Set view angle
        ax.view_init(elev=20, azim=45)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_zlim(0, 10)
        ax.axis('off')

        # Add title
        if self.spec.name:
            fig.suptitle(self.spec.name, fontsize=16, fontweight='bold')

        return fig

    def _calculate_layout_2d(self):
        """Calculate positions for 2D layout."""
        num_layers = len(self.spec.layers)

        if self.spec.layout == "vertical":
            # Vertical stack
            y_spacing = 8.0 / max(num_layers, 1)
            for i, layer in enumerate(self.spec.layers):
                x = 5.0  # Center
                y = 9.0 - (i * y_spacing)
                self.layer_positions[layer.name] = (x, y)

        elif self.spec.layout == "horizontal":
            # Horizontal flow
            x_spacing = 8.0 / max(num_layers, 1)
            for i, layer in enumerate(self.spec.layers):
                x = 1.0 + (i * x_spacing)
                y = 5.0  # Center
                self.layer_positions[layer.name] = (x, y)

        elif self.spec.layout == "hierarchical":
            # Hierarchical layout (for multi-modal, etc.)
            self._calculate_hierarchical_layout()

    def _calculate_layout_3d(self):
        """Calculate positions for 3D layout."""
        num_layers = len(self.spec.layers)
        z_spacing = 8.0 / max(num_layers, 1)

        for i, layer in enumerate(self.spec.layers):
            x = 5.0
            y = 5.0
            z = 1.0 + (i * z_spacing)
            self.layer_positions[layer.name] = (x, y, z)

    def _calculate_hierarchical_layout(self):
        """Calculate hierarchical layout for multi-modal architectures."""
        # Group layers by type
        input_layers = [l for l in self.spec.layers if l.type == "input"]
        processing_layers = [l for l in self.spec.layers
                           if l.type in ["attention", "ffn", "conv"]]
        output_layers = [l for l in self.spec.layers if l.type == "output"]

        # Position input layers
        if input_layers:
            x_spacing = 6.0 / max(len(input_layers), 1)
            for i, layer in enumerate(input_layers):
                x = 2.0 + (i * x_spacing)
                y = 8.0
                self.layer_positions[layer.name] = (x, y)

        # Position processing layers
        if processing_layers:
            y_spacing = 4.0 / max(len(processing_layers), 1)
            for i, layer in enumerate(processing_layers):
                x = 5.0
                y = 6.5 - (i * y_spacing)
                self.layer_positions[layer.name] = (x, y)

        # Position output layers
        if output_layers:
            for i, layer in enumerate(output_layers):
                x = 5.0
                y = 1.5
                self.layer_positions[layer.name] = (x, y)

    def _draw_layer_2d(self, ax, layer: LayerSpec):
        """Draw a single layer in 2D."""
        if layer.name not in self.layer_positions:
            return

        x, y = self.layer_positions[layer.name]

        # Determine size based on layer type
        if layer.type == "repeat":
            w, h = 2.0, 0.5
        elif layer.type in ["input", "output"]:
            w, h = 2.5, 0.8
        else:
            w, h = 2.0, 0.7

        # Get color
        color = layer.color or self._get_default_color(layer.type)

        # Draw box
        box = RoundedBox(
            position=(x - w/2, y - h/2),
            size=(w, h),
            label=layer.name,
            color=color,
            edge_color=self._darken_color(color),
            corner_radius=0.1
        )
        box.draw(ax)

        # Add shape annotations
        if layer.input_shape or layer.output_shape:
            shape_text = ""
            if layer.input_shape:
                shape_text += f"In: {layer.input_shape}"
            if layer.output_shape:
                if shape_text:
                    shape_text += "\n"
                shape_text += f"Out: {layer.output_shape}"

            ax.text(x + w/2 + 0.3, y, shape_text,
                   fontsize=7, va='center', ha='left',
                   style='italic', color='#666666')

        # Add parameter count
        if layer.params:
            ax.text(x, y - h/2 - 0.15, f"({layer.params})",
                   fontsize=7, ha='center', color='#888888')

    def _draw_layer_3d(self, ax, layer: LayerSpec):
        """Draw a single layer in 3D."""
        if layer.name not in self.layer_positions:
            return

        x, y, z = self.layer_positions[layer.name]

        # Determine size
        if layer.type in ["input", "output"]:
            w, h, d = 2.0, 2.0, 0.3
        else:
            w, h, d = 1.5, 1.5, 0.2

        # Get color and texture
        color = layer.color or self._get_default_color(layer.type)
        texture = layer.details.get("texture", "solid")

        # Draw 3D box
        box = Box3D(
            position=(x - w/2, y - h/2, z - d/2),
            size=(w, h, d),
            color=color,
            texture=texture,
            alpha=0.7
        )
        box.draw(ax)

        # Add label
        ax.text(x, y, z + d/2 + 0.3, layer.name,
               fontsize=9, ha='center', va='bottom',
               fontweight='bold')

    def _draw_layer_2d_in_3d(self, ax, layer: LayerSpec):
        """Draw 2D layer element in 3D space."""
        if layer.name not in self.layer_positions:
            return

        x, y, z = self.layer_positions[layer.name]
        w, h = 2.0, 0.7

        # Get color
        color = layer.color or self._get_default_color(layer.type)

        # Draw as a flat rectangle in 3D
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        vertices = [
            [x - w/2, y - h/2, z],
            [x + w/2, y - h/2, z],
            [x + w/2, y + h/2, z],
            [x - w/2, y + h/2, z]
        ]

        poly = Poly3DCollection([vertices], alpha=0.9,
                               facecolors=color,
                               edgecolors=self._darken_color(color),
                               linewidths=2)
        ax.add_collection3d(poly)

        # Add label
        ax.text(x, y, z, layer.name,
               fontsize=9, ha='center', va='center',
               fontweight='bold', color='#000000')

    def _draw_connection_2d(self, ax, conn: ConnectionSpec):
        """Draw connection between layers in 2D."""
        if conn.from_layer not in self.layer_positions or \
           conn.to_layer not in self.layer_positions:
            return

        start = self.layer_positions[conn.from_layer]
        end = self.layer_positions[conn.to_layer]

        # Determine curve based on style
        curve = 0.3 if conn.style == "curved" else 0.0

        # Draw arrow
        arrow = Arrow2D(
            start=start,
            end=end,
            color=self.colors.get("arrow", "#333333"),
            width=2.0,
            curve=curve
        )
        arrow.draw(ax)

        # Add label if present
        if conn.label:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            ax.text(mid_x, mid_y, conn.label,
                   fontsize=8, ha='center',
                   bbox=dict(boxstyle='round,pad=0.3',
                           facecolor='white', alpha=0.8))

    def _draw_connection_3d(self, ax, conn: ConnectionSpec):
        """Draw connection between layers in 3D."""
        if conn.from_layer not in self.layer_positions or \
           conn.to_layer not in self.layer_positions:
            return

        start = self.layer_positions[conn.from_layer]
        end = self.layer_positions[conn.to_layer]

        # Draw 3D arrow
        arrow = Arrow3D(
            start=start,
            end=end,
            color=self.colors.get("arrow", "#333333"),
            width=2.0
        )
        arrow.draw(ax)

    def _get_default_color(self, layer_type: str) -> str:
        """Get default color for layer type."""
        color_map = {
            "attention": self.colors.get("attention", "#87CEEB"),
            "ffn": self.colors.get("ffn", "#98FB98"),
            "norm": self.colors.get("norm", "#F0E68C"),
            "embedding": self.colors.get("embedding", "#DDA0DD"),
            "input": self.colors.get("primary", "#87CEEB"),
            "output": self.colors.get("output", "#FFB6C1"),
            "conv": self.colors.get("layer1", "#667EEA"),
            "linear": self.colors.get("layer2", "#764BA2"),
            "residual": self.colors.get("layer4", "#4FACFE"),
        }
        return color_map.get(layer_type, "#E0E0E0")

    def _darken_color(self, color: str, factor: float = 0.7) -> str:
        """Darken a color for edges."""
        from matplotlib.colors import to_rgb
        rgb = to_rgb(color)
        darkened = tuple(c * factor for c in rgb)
        return darkened
