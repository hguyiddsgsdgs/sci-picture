"""Chart creation functions."""

from .statistical import (
    create_statistical_chart,
    create_statistical_chart_plotly,
)
from .timeseries import (
    create_timeseries_chart,
    create_timeseries_chart_plotly,
)
from .comparison import (
    create_comparison_chart,
    create_comparison_chart_plotly,
)
from .scientific import (
    create_scientific_chart,
    create_scientific_chart_plotly,
)
from .ml import (
    create_ml_chart,
    create_ml_chart_plotly,
)
from .architecture import (
    create_architecture_diagram,
    create_architecture_diagram_from_template,
    list_architecture_templates,
    create_transformer_diagram,
    create_vit_diagram,
    create_multimodal_diagram,
    create_resnet_diagram,
)

__all__ = [
    # Data visualization charts
    "create_statistical_chart",
    "create_statistical_chart_plotly",
    "create_timeseries_chart",
    "create_timeseries_chart_plotly",
    "create_comparison_chart",
    "create_comparison_chart_plotly",
    "create_scientific_chart",
    "create_scientific_chart_plotly",
    "create_ml_chart",
    "create_ml_chart_plotly",
    # Architecture diagrams
    "create_architecture_diagram",
    "create_architecture_diagram_from_template",
    "list_architecture_templates",
    "create_transformer_diagram",
    "create_vit_diagram",
    "create_multimodal_diagram",
    "create_resnet_diagram",
]
