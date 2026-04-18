"""ML/AI specific chart creation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from matplotlib.axes import Axes
from sklearn.metrics import auc, confusion_matrix, roc_curve


def create_ml_chart(ax: Axes, data: pd.DataFrame, config):
    """Create ML/AI charts using matplotlib.

    Args:
        ax: Matplotlib axes
        data: Input data
        config: Plot configuration
    """
    chart_type = config.chart_type

    if chart_type == "ml_confusion_matrix":
        _create_confusion_matrix(ax, data, config)
    elif chart_type == "ml_roc_curve":
        _create_roc_curve(ax, data, config)
    elif chart_type == "ml_learning_curve":
        _create_learning_curve(ax, data, config)
    elif chart_type == "ml_feature_importance":
        _create_feature_importance(ax, data, config)
    elif chart_type == "ml_precision_recall":
        _create_precision_recall(ax, data, config)
    else:
        raise ValueError(f"Unknown ML chart type: {chart_type}")


def _create_confusion_matrix(ax: Axes, data: pd.DataFrame, config):
    """Create confusion matrix heatmap."""
    kwargs = config.extra_kwargs
    normalize = kwargs.pop("normalize", False)

    # Expect columns: y_true, y_pred
    if len(data.columns) < 2:
        raise ValueError("Confusion matrix requires 2 columns (y_true, y_pred)")

    y_true = data.iloc[:, 0]
    y_pred = data.iloc[:, 1]

    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Create heatmap
    sns.heatmap(cm, ax=ax, **kwargs)

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")


def _create_roc_curve(ax: Axes, data: pd.DataFrame, config):
    """Create ROC curve."""
    kwargs = config.extra_kwargs
    show_diagonal = kwargs.pop("show_diagonal", True)
    show_auc = kwargs.pop("show_auc", True)

    # Expect columns: y_true, y_score
    if len(data.columns) < 2:
        raise ValueError("ROC curve requires 2 columns (y_true, y_score)")

    y_true = data.iloc[:, 0]
    y_score = data.iloc[:, 1]

    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve
    label = f'ROC curve (AUC = {roc_auc:.2f})' if show_auc else 'ROC curve'
    ax.plot(fpr, tpr, linewidth=2, label=label, **kwargs)

    if show_diagonal:
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')

    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])


def _create_learning_curve(ax: Axes, data: pd.DataFrame, config):
    """Create learning curve."""
    kwargs = config.extra_kwargs
    show_std = kwargs.pop("show_std", True)
    std_alpha = kwargs.pop("std_alpha", 0.2)

    # Expect columns: train_sizes, train_scores, val_scores
    # Optional: train_scores_std, val_scores_std
    if len(data.columns) < 3:
        raise ValueError("Learning curve requires at least 3 columns")

    train_sizes = data.iloc[:, 0]
    train_scores = data.iloc[:, 1]
    val_scores = data.iloc[:, 2]

    # Plot mean scores
    ax.plot(train_sizes, train_scores, 'o-', label='Training score', **kwargs)
    ax.plot(train_sizes, val_scores, 'o-', label='Validation score', **kwargs)

    # Plot std if available
    if show_std and len(data.columns) >= 5:
        train_std = data.iloc[:, 3]
        val_std = data.iloc[:, 4]

        ax.fill_between(train_sizes,
                        train_scores - train_std,
                        train_scores + train_std,
                        alpha=std_alpha)
        ax.fill_between(train_sizes,
                        val_scores - val_std,
                        val_scores + val_std,
                        alpha=std_alpha)

    ax.set_xlabel("Training Size")
    ax.set_ylabel("Score")


def _create_feature_importance(ax: Axes, data: pd.DataFrame, config):
    """Create feature importance plot."""
    kwargs = config.extra_kwargs
    top_n = kwargs.pop("top_n", 20)
    horizontal = kwargs.pop("horizontal", True)

    # Expect columns: feature, importance
    if len(data.columns) < 2:
        raise ValueError("Feature importance requires 2 columns (feature, importance)")

    # Sort by importance and take top N
    data_sorted = data.sort_values(by=data.columns[1], ascending=False).head(top_n)

    if horizontal:
        ax.barh(data_sorted.iloc[:, 0], data_sorted.iloc[:, 1], **kwargs)
        ax.set_xlabel("Importance")
        ax.set_ylabel("Feature")
        ax.invert_yaxis()
    else:
        ax.bar(data_sorted.iloc[:, 0], data_sorted.iloc[:, 1], **kwargs)
        ax.set_xlabel("Feature")
        ax.set_ylabel("Importance")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def _create_precision_recall(ax: Axes, data: pd.DataFrame, config):
    """Create precision-recall curve."""
    from sklearn.metrics import precision_recall_curve, average_precision_score

    kwargs = config.extra_kwargs

    # Expect columns: y_true, y_score
    if len(data.columns) < 2:
        raise ValueError("Precision-recall curve requires 2 columns (y_true, y_score)")

    y_true = data.iloc[:, 0]
    y_score = data.iloc[:, 1]

    # Calculate precision-recall curve
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    # Plot curve
    ax.plot(recall, precision, linewidth=2,
            label=f'AP = {ap:.2f}', **kwargs)

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])


def create_ml_chart_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create ML/AI charts using plotly.

    Args:
        data: Input data
        config: Plot configuration

    Returns:
        Plotly figure
    """
    chart_type = config.chart_type

    if chart_type == "ml_confusion_matrix":
        return _create_confusion_matrix_plotly(data, config)
    elif chart_type == "ml_roc_curve":
        return _create_roc_curve_plotly(data, config)
    elif chart_type == "ml_learning_curve":
        return _create_learning_curve_plotly(data, config)
    elif chart_type == "ml_feature_importance":
        return _create_feature_importance_plotly(data, config)
    else:
        raise ValueError(f"Unknown ML chart type: {chart_type}")


def _create_confusion_matrix_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create confusion matrix with plotly."""
    kwargs = config.extra_kwargs
    normalize = kwargs.get("normalize", False)

    if len(data.columns) < 2:
        raise ValueError("Confusion matrix requires 2 columns (y_true, y_pred)")

    y_true = data.iloc[:, 0]
    y_pred = data.iloc[:, 1]

    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    # Get unique labels
    labels = sorted(set(y_true) | set(y_pred))

    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=[f"Pred {l}" for l in labels],
        y=[f"True {l}" for l in labels],
        colorscale=kwargs.get("cmap", "Blues"),
        text=cm,
        texttemplate='%{text}' if kwargs.get("annot", True) else None,
        textfont={"size": 12}
    ))

    fig.update_layout(
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )

    return fig


def _create_roc_curve_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create ROC curve with plotly."""
    kwargs = config.extra_kwargs

    if len(data.columns) < 2:
        raise ValueError("ROC curve requires 2 columns (y_true, y_score)")

    y_true = data.iloc[:, 0]
    y_score = data.iloc[:, 1]

    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    fig = go.Figure()

    # ROC curve
    fig.add_trace(go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name=f'ROC curve (AUC = {roc_auc:.2f})' if kwargs.get("show_auc", True) else 'ROC curve',
        line=dict(width=2)
    ))

    # Diagonal line
    if kwargs.get("show_diagonal", True):
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random',
            line=dict(dash='dash', color='gray')
        ))

    fig.update_xaxes(title_text="False Positive Rate", range=[0, 1])
    fig.update_yaxes(title_text="True Positive Rate", range=[0, 1.05])

    return fig


def _create_learning_curve_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create learning curve with plotly."""
    kwargs = config.extra_kwargs

    if len(data.columns) < 3:
        raise ValueError("Learning curve requires at least 3 columns")

    train_sizes = data.iloc[:, 0]
    train_scores = data.iloc[:, 1]
    val_scores = data.iloc[:, 2]

    fig = go.Figure()

    # Training scores
    fig.add_trace(go.Scatter(
        x=train_sizes,
        y=train_scores,
        mode='lines+markers',
        name='Training score'
    ))

    # Validation scores
    fig.add_trace(go.Scatter(
        x=train_sizes,
        y=val_scores,
        mode='lines+markers',
        name='Validation score'
    ))

    # Add std if available
    if kwargs.get("show_std", True) and len(data.columns) >= 5:
        train_std = data.iloc[:, 3]
        val_std = data.iloc[:, 4]

        # Training std
        fig.add_trace(go.Scatter(
            x=train_sizes.tolist() + train_sizes.tolist()[::-1],
            y=(train_scores + train_std).tolist() + (train_scores - train_std).tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,100,200,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            name='Training std'
        ))

        # Validation std
        fig.add_trace(go.Scatter(
            x=train_sizes.tolist() + train_sizes.tolist()[::-1],
            y=(val_scores + val_std).tolist() + (val_scores - val_std).tolist()[::-1],
            fill='toself',
            fillcolor='rgba(200,100,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            name='Validation std'
        ))

    fig.update_xaxes(title_text="Training Size")
    fig.update_yaxes(title_text="Score")

    return fig


def _create_feature_importance_plotly(data: pd.DataFrame, config) -> go.Figure:
    """Create feature importance plot with plotly."""
    kwargs = config.extra_kwargs
    top_n = kwargs.get("top_n", 20)
    horizontal = kwargs.get("horizontal", True)

    if len(data.columns) < 2:
        raise ValueError("Feature importance requires 2 columns (feature, importance)")

    # Sort by importance and take top N
    data_sorted = data.sort_values(by=data.columns[1], ascending=False).head(top_n)

    if horizontal:
        fig = go.Figure(go.Bar(
            x=data_sorted.iloc[:, 1],
            y=data_sorted.iloc[:, 0],
            orientation='h'
        ))
        fig.update_xaxes(title_text="Importance")
        fig.update_yaxes(title_text="Feature", autorange="reversed")
    else:
        fig = go.Figure(go.Bar(
            x=data_sorted.iloc[:, 0],
            y=data_sorted.iloc[:, 1]
        ))
        fig.update_xaxes(title_text="Feature")
        fig.update_yaxes(title_text="Importance")

    return fig
