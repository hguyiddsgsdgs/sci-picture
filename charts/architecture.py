"""Architecture diagram creation functions."""

import matplotlib.pyplot as plt
from typing import Union, Dict, Any, Optional
from pathlib import Path

try:
    from ..core.arch_parser import parse_architecture, ArchitectureSpec
    from ..core.arch_templates import ArchitectureTemplates
    from ..core.arch_renderer import ArchitectureRenderer
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.arch_parser import parse_architecture, ArchitectureSpec
    from core.arch_templates import ArchitectureTemplates
    from core.arch_renderer import ArchitectureRenderer


def create_architecture_diagram(
    description: Union[str, Dict, ArchitectureSpec],
    figsize: tuple = (12, 8),
    style: Optional[str] = None,
    output_path: Optional[Union[str, Path]] = None,
    dpi: int = 300,
    format: str = "pdf"
) -> plt.Figure:
    """
    Create architecture diagram from description.

    Args:
        description: Natural language, JSON dict, or ArchitectureSpec
        figsize: Figure size (width, height)
        style: Visual style override ('transformer', 'multimodal', 'modern', 'academic')
        output_path: Path to save figure (optional)
        dpi: DPI for output
        format: Output format ('pdf', 'png', 'svg')

    Returns:
        Matplotlib figure

    Examples:
        # Natural language
        fig = create_architecture_diagram('''
            A Transformer Encoder with 6 layers.
            Input: [batch, seq_len, 512]
            Each layer has Multi-Head Attention with 8 heads
            and Feed-Forward Network with 2048 hidden units.
        ''')

        # JSON
        fig = create_architecture_diagram({
            "name": "My Model",
            "layers": [
                {"name": "Input", "type": "input", "input_shape": "[B, 512]"},
                {"name": "Attention", "type": "attention"},
                {"name": "Output", "type": "output"}
            ]
        })

        # Template
        fig = create_architecture_diagram_from_template(
            "transformer_encoder",
            num_layers=6,
            d_model=512
        )
    """
    # Parse description
    if isinstance(description, ArchitectureSpec):
        spec = description
    else:
        spec = parse_architecture(description)

    # Override style if specified
    if style:
        spec.style = style

    # Render diagram
    renderer = ArchitectureRenderer(spec, figsize=figsize)
    fig = renderer.render()

    # Save if output path specified
    if output_path:
        fig.savefig(output_path, dpi=dpi, format=format, bbox_inches='tight')

    return fig


def create_architecture_diagram_from_template(
    template_name: str,
    figsize: tuple = (12, 8),
    output_path: Optional[Union[str, Path]] = None,
    dpi: int = 300,
    format: str = "pdf",
    **template_params
) -> plt.Figure:
    """
    Create architecture diagram from pre-defined template.

    Args:
        template_name: Template name (see ArchitectureTemplates.list_templates())
        figsize: Figure size
        output_path: Path to save figure
        dpi: DPI for output
        format: Output format
        **template_params: Template-specific parameters

    Returns:
        Matplotlib figure

    Examples:
        # Transformer Encoder
        fig = create_architecture_diagram_from_template(
            "transformer_encoder",
            num_layers=6,
            d_model=512,
            num_heads=8
        )

        # Vision Transformer
        fig = create_architecture_diagram_from_template(
            "vit",
            patch_size=16,
            d_model=768,
            num_layers=12
        )

        # Cross-Attention (multi-modal)
        fig = create_architecture_diagram_from_template(
            "cross_attention",
            d_model=512,
            num_heads=8
        )
    """
    # Get template
    template_dict = ArchitectureTemplates.get_template(template_name, **template_params)

    # Create diagram
    return create_architecture_diagram(
        template_dict,
        figsize=figsize,
        output_path=output_path,
        dpi=dpi,
        format=format
    )


def list_architecture_templates() -> list:
    """
    List all available architecture templates.

    Returns:
        List of template names
    """
    return ArchitectureTemplates.list_templates()


# Convenience functions for common architectures

def create_transformer_diagram(
    num_layers: int = 6,
    d_model: int = 512,
    num_heads: int = 8,
    d_ff: int = 2048,
    encoder: bool = True,
    **kwargs
) -> plt.Figure:
    """Create Transformer architecture diagram."""
    template = "transformer_encoder" if encoder else "transformer_decoder"
    return create_architecture_diagram_from_template(
        template,
        num_layers=num_layers,
        d_model=d_model,
        num_heads=num_heads,
        d_ff=d_ff,
        **kwargs
    )


def create_vit_diagram(
    patch_size: int = 16,
    d_model: int = 768,
    num_layers: int = 12,
    num_heads: int = 12,
    **kwargs
) -> plt.Figure:
    """Create Vision Transformer diagram."""
    return create_architecture_diagram_from_template(
        "vit",
        patch_size=patch_size,
        d_model=d_model,
        num_layers=num_layers,
        num_heads=num_heads,
        **kwargs
    )


def create_multimodal_diagram(
    d_text: int = 512,
    d_image: int = 2048,
    d_fusion: int = 768,
    **kwargs
) -> plt.Figure:
    """Create multi-modal fusion diagram."""
    return create_architecture_diagram_from_template(
        "multimodal_fusion",
        d_text=d_text,
        d_image=d_image,
        d_fusion=d_fusion,
        **kwargs
    )


def create_resnet_diagram(
    channels: int = 64,
    **kwargs
) -> plt.Figure:
    """Create ResNet block diagram."""
    return create_architecture_diagram_from_template(
        "resnet_block",
        channels=channels,
        **kwargs
    )
