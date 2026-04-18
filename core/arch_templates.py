"""Pre-defined templates for common architectures."""

from typing import Dict, Any


class ArchitectureTemplates:
    """Library of pre-defined architecture templates."""

    @staticmethod
    def get_template(name: str, **kwargs) -> Dict[str, Any]:
        """
        Get architecture template by name.

        Args:
            name: Template name
            **kwargs: Template parameters

        Returns:
            Architecture specification dict
        """
        templates = {
            "transformer_encoder": ArchitectureTemplates.transformer_encoder,
            "transformer_decoder": ArchitectureTemplates.transformer_decoder,
            "cross_attention": ArchitectureTemplates.cross_attention,
            "self_attention": ArchitectureTemplates.self_attention,
            "resnet_block": ArchitectureTemplates.resnet_block,
            "vit": ArchitectureTemplates.vision_transformer,
            "bert_layer": ArchitectureTemplates.bert_layer,
            "gpt_decoder": ArchitectureTemplates.gpt_decoder,
            "multimodal_fusion": ArchitectureTemplates.multimodal_fusion,
            "deformable_conv": ArchitectureTemplates.deformable_conv,
        }

        template_func = templates.get(name.lower())
        if not template_func:
            raise ValueError(f"Unknown template: {name}")

        return template_func(**kwargs)

    @staticmethod
    def transformer_encoder(num_layers: int = 6, d_model: int = 512,
                           num_heads: int = 8, d_ff: int = 2048) -> Dict:
        """Standard Transformer Encoder."""
        return {
            "name": "Transformer Encoder",
            "style": "transformer",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Input Embedding",
                    "type": "embedding",
                    "input_shape": f"[seq_len, {d_model}]",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#DDA0DD"
                },
                {
                    "name": f"Multi-Head Attention\n({num_heads} heads)",
                    "type": "attention",
                    "output_shape": f"[seq_len, {d_model}]",
                    "details": {"heads": num_heads, "d_model": d_model},
                    "color": "#87CEEB"
                },
                {
                    "name": "Add & Norm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"Feed-Forward\n(d_ff={d_ff})",
                    "type": "ffn",
                    "details": {"d_ff": d_ff},
                    "color": "#98FB98"
                },
                {
                    "name": "Add & Norm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"× {num_layers} layers",
                    "type": "repeat",
                    "color": "#E0E0E0"
                },
                {
                    "name": "Output",
                    "type": "output",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#FFB6C1"
                }
            ],
            "annotations": {
                "note": f"Standard Transformer Encoder with {num_layers} layers"
            }
        }

    @staticmethod
    def transformer_decoder(num_layers: int = 6, d_model: int = 512,
                           num_heads: int = 8, d_ff: int = 2048) -> Dict:
        """Standard Transformer Decoder."""
        return {
            "name": "Transformer Decoder",
            "style": "transformer",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Output Embedding",
                    "type": "embedding",
                    "input_shape": f"[tgt_len, {d_model}]",
                    "color": "#DDA0DD"
                },
                {
                    "name": "Masked Self-Attention",
                    "type": "attention",
                    "details": {"heads": num_heads, "masked": True},
                    "color": "#87CEEB"
                },
                {
                    "name": "Add & Norm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": "Cross-Attention",
                    "type": "attention",
                    "details": {"heads": num_heads, "cross": True},
                    "color": "#B0C4DE"
                },
                {
                    "name": "Add & Norm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"Feed-Forward\n(d_ff={d_ff})",
                    "type": "ffn",
                    "color": "#98FB98"
                },
                {
                    "name": "Add & Norm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"× {num_layers} layers",
                    "type": "repeat",
                    "color": "#E0E0E0"
                },
                {
                    "name": "Linear + Softmax",
                    "type": "output",
                    "color": "#FFB6C1"
                }
            ]
        }

    @staticmethod
    def cross_attention(d_model: int = 512, num_heads: int = 8) -> Dict:
        """Cross-Attention module (similar to reference image 1)."""
        return {
            "name": "Cross-Modality Decoder Layer",
            "style": "multimodal",
            "layout": "hierarchical",
            "layers": [
                {
                    "name": "Text Features",
                    "type": "input",
                    "input_shape": "[seq_len, d_text]",
                    "color": "#FFD700",
                    "details": {"modality": "text", "texture": "diagonal"}
                },
                {
                    "name": "Image Features",
                    "type": "input",
                    "input_shape": "[H×W, d_img]",
                    "color": "#87CEEB",
                    "details": {"modality": "image", "texture": "grid"}
                },
                {
                    "name": "Self-Attention",
                    "type": "attention",
                    "details": {"heads": num_heads, "qkv": "Q,K,V"},
                    "color": "#FFFFFF"
                },
                {
                    "name": "Image Cross-Attention",
                    "type": "attention",
                    "details": {"heads": num_heads, "kv_source": "image"},
                    "color": "#B0E0E6"
                },
                {
                    "name": "Text Cross-Attention",
                    "type": "attention",
                    "details": {"heads": num_heads, "kv_source": "text"},
                    "color": "#FFFACD"
                },
                {
                    "name": "FFN",
                    "type": "ffn",
                    "color": "#FFFFFF"
                },
                {
                    "name": "Updated Query",
                    "type": "output",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#FFB6C1"
                }
            ],
            "connections": [
                {"from": "Text Features", "to": "Text Cross-Attention", "label": "K,V"},
                {"from": "Image Features", "to": "Image Cross-Attention", "label": "K,V"},
                {"from": "Self-Attention", "to": "Image Cross-Attention", "label": "Q"},
                {"from": "Image Cross-Attention", "to": "Text Cross-Attention", "label": "Q"},
                {"from": "Text Cross-Attention", "to": "FFN"},
                {"from": "FFN", "to": "Updated Query"}
            ]
        }

    @staticmethod
    def self_attention(d_model: int = 512, num_heads: int = 8) -> Dict:
        """Self-Attention mechanism."""
        return {
            "name": "Multi-Head Self-Attention",
            "style": "transformer",
            "layout": "horizontal",
            "layers": [
                {
                    "name": "Input",
                    "type": "input",
                    "input_shape": f"[seq_len, {d_model}]",
                    "color": "#DDA0DD"
                },
                {
                    "name": "Linear Q",
                    "type": "linear",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#FFB6C1"
                },
                {
                    "name": "Linear K",
                    "type": "linear",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#98FB98"
                },
                {
                    "name": "Linear V",
                    "type": "linear",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#87CEEB"
                },
                {
                    "name": f"Attention\n({num_heads} heads)",
                    "type": "attention",
                    "details": {"heads": num_heads},
                    "color": "#F0E68C"
                },
                {
                    "name": "Concat & Linear",
                    "type": "linear",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#DDA0DD"
                }
            ]
        }

    @staticmethod
    def resnet_block(channels: int = 64) -> Dict:
        """ResNet residual block."""
        return {
            "name": "ResNet Block",
            "style": "modern",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Input",
                    "type": "input",
                    "input_shape": f"[H, W, {channels}]",
                    "color": "#667EEA"
                },
                {
                    "name": "Conv 3×3",
                    "type": "conv",
                    "details": {"kernel": 3, "stride": 1},
                    "color": "#764BA2"
                },
                {
                    "name": "BatchNorm + ReLU",
                    "type": "norm",
                    "color": "#F093FB"
                },
                {
                    "name": "Conv 3×3",
                    "type": "conv",
                    "details": {"kernel": 3, "stride": 1},
                    "color": "#764BA2"
                },
                {
                    "name": "BatchNorm",
                    "type": "norm",
                    "color": "#F093FB"
                },
                {
                    "name": "Add (Residual)",
                    "type": "residual",
                    "color": "#4FACFE"
                },
                {
                    "name": "ReLU",
                    "type": "activation",
                    "color": "#00F2FE"
                }
            ],
            "connections": [
                {"from": "Input", "to": "Conv 3×3"},
                {"from": "Conv 3×3", "to": "BatchNorm + ReLU"},
                {"from": "BatchNorm + ReLU", "to": "Conv 3×3"},
                {"from": "Conv 3×3", "to": "BatchNorm"},
                {"from": "BatchNorm", "to": "Add (Residual)"},
                {"from": "Input", "to": "Add (Residual)", "style": "curved", "label": "skip"},
                {"from": "Add (Residual)", "to": "ReLU"}
            ]
        }

    @staticmethod
    def vision_transformer(patch_size: int = 16, d_model: int = 768,
                          num_layers: int = 12, num_heads: int = 12) -> Dict:
        """Vision Transformer (ViT)."""
        return {
            "name": "Vision Transformer",
            "style": "transformer",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Image Input",
                    "type": "input",
                    "input_shape": "224×224×3",
                    "color": "#DDA0DD",
                    "details": {"texture": "grid"}
                },
                {
                    "name": f"Patch Embedding\n({patch_size}×{patch_size} patches)",
                    "type": "embedding",
                    "output_shape": f"196×{d_model}",
                    "color": "#FFB6C1"
                },
                {
                    "name": "Position Embedding",
                    "type": "embedding",
                    "color": "#F0E68C"
                },
                {
                    "name": f"Transformer Encoder\n({num_layers} layers, {num_heads} heads)",
                    "type": "attention",
                    "details": {"layers": num_layers, "heads": num_heads},
                    "color": "#87CEEB"
                },
                {
                    "name": "Classification Head",
                    "type": "linear",
                    "output_shape": "num_classes",
                    "color": "#98FB98"
                }
            ]
        }

    @staticmethod
    def bert_layer(d_model: int = 768, num_heads: int = 12, d_ff: int = 3072) -> Dict:
        """BERT encoder layer."""
        return {
            "name": "BERT Layer",
            "style": "academic",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Input",
                    "type": "input",
                    "input_shape": f"[seq_len, {d_model}]",
                    "color": "#0C4B8E"
                },
                {
                    "name": f"Multi-Head Attention\n({num_heads} heads)",
                    "type": "attention",
                    "color": "#2E86AB"
                },
                {
                    "name": "Add & LayerNorm",
                    "type": "norm",
                    "color": "#A23B72"
                },
                {
                    "name": f"Feed-Forward\n({d_ff} hidden)",
                    "type": "ffn",
                    "color": "#F18F01"
                },
                {
                    "name": "Add & LayerNorm",
                    "type": "norm",
                    "color": "#A23B72"
                }
            ]
        }

    @staticmethod
    def gpt_decoder(num_layers: int = 12, d_model: int = 768,
                   num_heads: int = 12, d_ff: int = 3072) -> Dict:
        """GPT decoder architecture."""
        return {
            "name": "GPT Decoder",
            "style": "transformer",
            "layout": "vertical",
            "layers": [
                {
                    "name": "Token Embedding",
                    "type": "embedding",
                    "output_shape": f"[seq_len, {d_model}]",
                    "color": "#DDA0DD"
                },
                {
                    "name": "Position Embedding",
                    "type": "embedding",
                    "color": "#F0E68C"
                },
                {
                    "name": f"Masked Self-Attention\n({num_heads} heads)",
                    "type": "attention",
                    "details": {"masked": True},
                    "color": "#87CEEB"
                },
                {
                    "name": "Add & LayerNorm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"Feed-Forward\n({d_ff} hidden)",
                    "type": "ffn",
                    "color": "#98FB98"
                },
                {
                    "name": "Add & LayerNorm",
                    "type": "norm",
                    "color": "#F0E68C"
                },
                {
                    "name": f"× {num_layers} layers",
                    "type": "repeat",
                    "color": "#E0E0E0"
                },
                {
                    "name": "Language Model Head",
                    "type": "linear",
                    "output_shape": "vocab_size",
                    "color": "#FFB6C1"
                }
            ]
        }

    @staticmethod
    def multimodal_fusion(d_text: int = 512, d_image: int = 2048,
                         d_fusion: int = 768) -> Dict:
        """Multi-modal fusion module."""
        return {
            "name": "Multi-Modal Fusion",
            "style": "multimodal",
            "layout": "hierarchical",
            "layers": [
                {
                    "name": "Text Encoder",
                    "type": "input",
                    "output_shape": f"[seq_len, {d_text}]",
                    "color": "#FFD700",
                    "details": {"texture": "diagonal"}
                },
                {
                    "name": "Image Encoder",
                    "type": "input",
                    "output_shape": f"[H×W, {d_image}]",
                    "color": "#87CEEB",
                    "details": {"texture": "grid"}
                },
                {
                    "name": "Text Projection",
                    "type": "linear",
                    "output_shape": f"[seq_len, {d_fusion}]",
                    "color": "#FFFACD"
                },
                {
                    "name": "Image Projection",
                    "type": "linear",
                    "output_shape": f"[H×W, {d_fusion}]",
                    "color": "#B0E0E6"
                },
                {
                    "name": "Cross-Modal Attention",
                    "type": "attention",
                    "color": "#98FB98"
                },
                {
                    "name": "Fusion Output",
                    "type": "output",
                    "output_shape": f"[seq_len, {d_fusion}]",
                    "color": "#FFB6C1"
                }
            ]
        }

    @staticmethod
    def deformable_conv(in_channels: int = 64, out_channels: int = 64) -> Dict:
        """Deformable convolution (similar to reference image 2)."""
        return {
            "name": "Deformable Convolution",
            "style": "modern",
            "layout": "horizontal",
            "layers": [
                {
                    "name": "Input Feature Map",
                    "type": "input",
                    "input_shape": f"[H, W, {in_channels}]",
                    "color": "#C0C0C0",
                    "details": {"texture": "grid", "3d": True}
                },
                {
                    "name": "Conv\n(offset field)",
                    "type": "conv",
                    "output_shape": "[H, W, 2N]",
                    "color": "#98FB98",
                    "details": {"3d": True}
                },
                {
                    "name": "Offsets",
                    "type": "output",
                    "output_shape": "[H, W, 2N]",
                    "color": "#F0E68C",
                    "details": {"show_grid": True}
                },
                {
                    "name": "Deformable Convolution",
                    "type": "conv",
                    "details": {"deformable": True},
                    "color": "#87CEEB"
                },
                {
                    "name": "Output Feature Map",
                    "type": "output",
                    "input_shape": f"[H, W, {out_channels}]",
                    "color": "#C0C0C0",
                    "details": {"texture": "grid", "3d": True}
                }
            ],
            "annotations": {
                "sampling_points": True,
                "show_deformation": True
            }
        }

    @staticmethod
    def list_templates() -> list:
        """List all available templates."""
        return [
            "transformer_encoder",
            "transformer_decoder",
            "cross_attention",
            "self_attention",
            "resnet_block",
            "vit",
            "bert_layer",
            "gpt_decoder",
            "multimodal_fusion",
            "deformable_conv"
        ]
