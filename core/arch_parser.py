"""Parser for architecture descriptions (natural language and JSON)."""

import json
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field


@dataclass
class LayerSpec:
    """Specification for a single layer/module."""
    name: str
    type: str
    input_shape: Optional[str] = None
    output_shape: Optional[str] = None
    params: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    position: Optional[tuple] = None
    color: Optional[str] = None


@dataclass
class ConnectionSpec:
    """Specification for connections between layers."""
    from_layer: str
    to_layer: str
    label: Optional[str] = None
    style: str = "solid"  # solid, dashed, curved


@dataclass
class ArchitectureSpec:
    """Complete architecture specification."""
    name: str
    layers: List[LayerSpec]
    connections: List[ConnectionSpec]
    style: str = "transformer"
    layout: str = "vertical"  # vertical, horizontal, hierarchical
    annotations: Dict[str, Any] = field(default_factory=dict)


class ArchitectureParser:
    """Parse architecture descriptions into structured specifications."""

    def __init__(self):
        self.layer_keywords = {
            "attention": ["attention", "attn", "self-attention", "cross-attention"],
            "ffn": ["ffn", "feed-forward", "feedforward", "mlp"],
            "conv": ["conv", "convolution", "convolutional"],
            "linear": ["linear", "dense", "fc", "fully-connected"],
            "norm": ["norm", "normalization", "layernorm", "batchnorm"],
            "embedding": ["embedding", "embed"],
            "pooling": ["pool", "pooling", "maxpool", "avgpool"],
            "activation": ["relu", "gelu", "sigmoid", "tanh", "softmax"],
            "dropout": ["dropout"],
            "residual": ["residual", "skip", "shortcut"]
        }

    def parse(self, description: Union[str, Dict]) -> ArchitectureSpec:
        """
        Parse architecture description.

        Args:
            description: Natural language string or JSON dict

        Returns:
            ArchitectureSpec object
        """
        if isinstance(description, dict):
            return self._parse_json(description)
        else:
            return self._parse_natural_language(description)

    def _parse_json(self, data: Dict) -> ArchitectureSpec:
        """Parse JSON/dict description."""
        name = data.get("name", "Model Architecture")
        style = data.get("style", "transformer")
        layout = data.get("layout", "vertical")

        layers = []
        connections = []

        # Parse layers
        for layer_data in data.get("layers", []):
            layer = LayerSpec(
                name=layer_data.get("name", "Layer"),
                type=layer_data.get("type", "unknown"),
                input_shape=layer_data.get("input_shape"),
                output_shape=layer_data.get("output_shape"),
                params=layer_data.get("params"),
                details=layer_data.get("details", {}),
                color=layer_data.get("color")
            )
            layers.append(layer)

        # Parse connections
        for conn_data in data.get("connections", []):
            conn = ConnectionSpec(
                from_layer=conn_data.get("from"),
                to_layer=conn_data.get("to"),
                label=conn_data.get("label"),
                style=conn_data.get("style", "solid")
            )
            connections.append(conn)

        # Auto-generate connections if not specified
        if not connections and len(layers) > 1:
            for i in range(len(layers) - 1):
                connections.append(ConnectionSpec(
                    from_layer=layers[i].name,
                    to_layer=layers[i+1].name
                ))

        return ArchitectureSpec(
            name=name,
            layers=layers,
            connections=connections,
            style=style,
            layout=layout,
            annotations=data.get("annotations", {})
        )

    def _parse_natural_language(self, text: str) -> ArchitectureSpec:
        """Parse natural language description."""
        # Extract model name
        name_match = re.search(r'(?:model|architecture):\s*([^\n]+)', text, re.IGNORECASE)
        name = name_match.group(1).strip() if name_match else "Model Architecture"

        layers = []
        connections = []

        # Split into sentences/lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        layer_counter = 0
        prev_layer_name = None

        for line in lines:
            # Skip lines that are just the model name
            if 'model' in line.lower() and ':' in line:
                continue

            # Detect layer type
            layer_type = self._detect_layer_type(line)
            if not layer_type:
                continue

            # Extract layer details
            layer_name = self._extract_layer_name(line, layer_type, layer_counter)
            input_shape = self._extract_shape(line, "input")
            output_shape = self._extract_shape(line, "output")
            params = self._extract_params(line)
            details = self._extract_details(line)

            layer = LayerSpec(
                name=layer_name,
                type=layer_type,
                input_shape=input_shape,
                output_shape=output_shape,
                params=params,
                details=details
            )
            layers.append(layer)

            # Auto-connect to previous layer
            if prev_layer_name:
                connections.append(ConnectionSpec(
                    from_layer=prev_layer_name,
                    to_layer=layer_name
                ))

            prev_layer_name = layer_name
            layer_counter += 1

        # Determine style based on content
        style = self._infer_style(text)
        layout = self._infer_layout(text)

        return ArchitectureSpec(
            name=name,
            layers=layers,
            connections=connections,
            style=style,
            layout=layout
        )

    def _detect_layer_type(self, text: str) -> Optional[str]:
        """Detect layer type from text."""
        text_lower = text.lower()
        for layer_type, keywords in self.layer_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return layer_type
        return None

    def _extract_layer_name(self, text: str, layer_type: str, counter: int) -> str:
        """Extract or generate layer name."""
        # Try to find explicit name
        name_patterns = [
            r'(?:layer|module|block):\s*([^\n,]+)',
            r'^([A-Z][a-zA-Z\s]+?)(?:\s+layer|\s+module|\s*:)',
        ]

        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # Generate name based on type
        type_names = {
            "attention": "Multi-Head Attention",
            "ffn": "Feed-Forward Network",
            "conv": "Convolution",
            "linear": "Linear",
            "norm": "Layer Normalization",
            "embedding": "Embedding",
            "pooling": "Pooling",
            "activation": "Activation",
            "dropout": "Dropout",
            "residual": "Residual Connection"
        }

        base_name = type_names.get(layer_type, layer_type.capitalize())
        return f"{base_name}"

    def _extract_shape(self, text: str, shape_type: str) -> Optional[str]:
        """Extract input/output shape."""
        patterns = [
            rf'{shape_type}[:\s]+\[([^\]]+)\]',
            rf'{shape_type}[:\s]+\(([^\)]+)\)',
            rf'{shape_type}[:\s]+(\d+[×x]\d+[×x]?\d*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_params(self, text: str) -> Optional[str]:
        """Extract parameter count."""
        patterns = [
            r'(\d+\.?\d*[MKB]?)\s*(?:params?|parameters?)',
            r'(?:params?|parameters?):\s*(\d+\.?\d*[MKB]?)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def _extract_details(self, text: str) -> Dict[str, Any]:
        """Extract additional details."""
        details = {}

        # Extract common parameters
        param_patterns = {
            "heads": r'(\d+)\s*heads?',
            "layers": r'(\d+)\s*layers?',
            "dim": r'd[_-]?model[:\s=]+(\d+)',
            "hidden": r'hidden[:\s=]+(\d+)',
            "kernel": r'kernel[:\s=]+(\d+)',
        }

        for key, pattern in param_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                details[key] = match.group(1)

        return details

    def _infer_style(self, text: str) -> str:
        """Infer visual style from content."""
        text_lower = text.lower()

        if any(word in text_lower for word in ["transformer", "attention", "bert", "gpt"]):
            return "transformer"
        elif any(word in text_lower for word in ["multimodal", "cross-modal", "fusion"]):
            return "multimodal"
        elif any(word in text_lower for word in ["resnet", "cnn", "convolution"]):
            return "modern"
        else:
            return "academic"

    def _infer_layout(self, text: str) -> str:
        """Infer layout from content."""
        text_lower = text.lower()

        if "horizontal" in text_lower:
            return "horizontal"
        elif "hierarchical" in text_lower or "tree" in text_lower:
            return "hierarchical"
        else:
            return "vertical"


def parse_architecture(description: Union[str, Dict]) -> ArchitectureSpec:
    """
    Convenience function to parse architecture description.

    Args:
        description: Natural language string or JSON dict

    Returns:
        ArchitectureSpec object

    Examples:
        # Natural language
        spec = parse_architecture('''
            A Transformer Encoder with:
            - Input: [batch, seq_len, 512]
            - 6 layers of Multi-Head Attention (8 heads)
            - Feed-Forward Network with 2048 hidden units
            - Layer Normalization
            - Output: [batch, seq_len, 512]
        ''')

        # JSON
        spec = parse_architecture({
            "name": "Vision Transformer",
            "layers": [
                {"name": "Patch Embedding", "type": "embedding",
                 "input_shape": "224×224×3", "output_shape": "196×768"},
                {"name": "Transformer Encoder", "type": "attention",
                 "details": {"layers": 12, "heads": 12}}
            ]
        })
    """
    parser = ArchitectureParser()
    return parser.parse(description)
