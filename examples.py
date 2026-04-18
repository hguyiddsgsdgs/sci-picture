"""Example usage of the scientific plotter."""

import numpy as np
import pandas as pd
from pathlib import Path

from core.plotter import ScientificPlotter, PlotConfig


def create_sample_data():
    """Create sample datasets for demonstration."""
    output_dir = Path("examples/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Scatter data for regression
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y = 2 * x + 1 + np.random.normal(0, 2, 100)
    df_scatter = pd.DataFrame({"x": x, "y": y})
    df_scatter.to_csv(output_dir / "scatter_data.csv", index=False)

    # 2. Time series data
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    values = np.cumsum(np.random.randn(365)) + 100
    df_ts = pd.DataFrame({"value": values}, index=dates)
    df_ts.to_csv(output_dir / "timeseries_data.csv")

    # 3. Comparison data
    categories = ["A", "B", "C", "D", "E"]
    values1 = np.random.randint(10, 100, 5)
    values2 = np.random.randint(10, 100, 5)
    df_comp = pd.DataFrame({
        "Group1": values1,
        "Group2": values2
    }, index=categories)
    df_comp.to_csv(output_dir / "comparison_data.csv")

    # 4. Distribution data
    data1 = np.random.normal(100, 15, 1000)
    data2 = np.random.normal(110, 20, 1000)
    df_dist = pd.DataFrame({
        "Variable1": data1,
        "Variable2": data2
    })
    df_dist.to_csv(output_dir / "distribution_data.csv", index=False)

    # 5. Correlation data
    n = 100
    df_corr = pd.DataFrame({
        "Feature1": np.random.randn(n),
        "Feature2": np.random.randn(n),
        "Feature3": np.random.randn(n),
        "Feature4": np.random.randn(n),
    })
    df_corr["Feature2"] = df_corr["Feature1"] * 0.8 + np.random.randn(n) * 0.2
    df_corr.to_csv(output_dir / "correlation_data.csv", index=False)

    # 6. ML data - confusion matrix
    y_true = np.random.randint(0, 3, 200)
    y_pred = y_true.copy()
    # Add some errors
    error_idx = np.random.choice(200, 40, replace=False)
    y_pred[error_idx] = np.random.randint(0, 3, 40)
    df_cm = pd.DataFrame({"y_true": y_true, "y_pred": y_pred})
    df_cm.to_csv(output_dir / "confusion_matrix_data.csv", index=False)

    # 7. ML data - ROC curve
    y_true_binary = np.random.randint(0, 2, 200)
    y_score = np.random.rand(200)
    # Make scores somewhat correlated with true labels
    y_score[y_true_binary == 1] += 0.3
    df_roc = pd.DataFrame({"y_true": y_true_binary, "y_score": y_score})
    df_roc.to_csv(output_dir / "roc_data.csv", index=False)

    # 8. Feature importance data
    features = [f"Feature_{i}" for i in range(20)]
    importance = np.random.exponential(0.1, 20)
    df_fi = pd.DataFrame({"feature": features, "importance": importance})
    df_fi.to_csv(output_dir / "feature_importance_data.csv", index=False)

    print(f"Sample data created in {output_dir}")


def example_basic_usage():
    """Example 1: Basic usage."""
    print("\n=== Example 1: Basic Usage ===")

    plotter = ScientificPlotter()

    # Create a scatter plot with regression
    config = PlotConfig(
        chart_type="sci_scatter_regression",
        title="Scatter Plot with Regression",
        xlabel="X Variable",
        ylabel="Y Variable",
        style="nature",
        extra_kwargs={
            "show_regression": True,
            "show_confidence": True,
            "show_equation": True,
            "show_r2": True,
        }
    )

    fig = plotter.create_chart("examples/data/scatter_data.csv", config)
    fig.save("examples/output/scatter_regression.png")
    print("Created: examples/output/scatter_regression.png")


def example_templates():
    """Example 2: Using templates."""
    print("\n=== Example 2: Using Templates ===")

    plotter = ScientificPlotter()

    # Use a predefined template
    fig = plotter.create_from_template(
        "correlation_matrix",
        "examples/data/correlation_data.csv",
        title="Feature Correlations"
    )
    fig.save("examples/output/correlation_matrix.png")
    print("Created: examples/output/correlation_matrix.png")


def example_publication_ready():
    """Example 3: Publication-ready figures."""
    print("\n=== Example 3: Publication-Ready Figures ===")

    plotter = ScientificPlotter()

    # Nature-style figure
    fig = plotter.create_from_template(
        "nature_figure",
        "examples/data/scatter_data.csv",
        title="Nature Style"
    )
    fig.save("examples/output/nature_figure.pdf", format="pdf")
    print("Created: examples/output/nature_figure.pdf")

    # Science-style figure
    fig = plotter.create_from_template(
        "science_figure",
        "examples/data/timeseries_data.csv",
        title="Science Style"
    )
    fig.save("examples/output/science_figure.pdf", format="pdf")
    print("Created: examples/output/science_figure.pdf")


def example_ml_charts():
    """Example 4: ML/AI specific charts."""
    print("\n=== Example 4: ML/AI Charts ===")

    plotter = ScientificPlotter()

    # Confusion matrix
    config = PlotConfig(
        chart_type="ml_confusion_matrix",
        title="Confusion Matrix",
        style="minimal",
        extra_kwargs={"annot": True, "fmt": "d", "cmap": "Blues"}
    )
    fig = plotter.create_chart("examples/data/confusion_matrix_data.csv", config)
    fig.save("examples/output/confusion_matrix.png")
    print("Created: examples/output/confusion_matrix.png")

    # ROC curve
    config = PlotConfig(
        chart_type="ml_roc_curve",
        title="ROC Curve",
        style="nature",
        extra_kwargs={"show_diagonal": True, "show_auc": True}
    )
    fig = plotter.create_chart("examples/data/roc_data.csv", config)
    fig.save("examples/output/roc_curve.png")
    print("Created: examples/output/roc_curve.png")

    # Feature importance
    config = PlotConfig(
        chart_type="ml_feature_importance",
        title="Feature Importance",
        style="nature",
        figsize=(10, 8),
        extra_kwargs={"top_n": 15, "horizontal": True}
    )
    fig = plotter.create_chart("examples/data/feature_importance_data.csv", config)
    fig.save("examples/output/feature_importance.png")
    print("Created: examples/output/feature_importance.png")


def example_interactive():
    """Example 5: Interactive plotly charts."""
    print("\n=== Example 5: Interactive Charts ===")

    plotter = ScientificPlotter()

    # Interactive scatter plot
    config = PlotConfig(
        chart_type="sci_scatter_regression",
        title="Interactive Scatter Plot",
        interactive=True,
        extra_kwargs={"show_regression": True}
    )
    fig = plotter.create_chart("examples/data/scatter_data.csv", config)
    fig.save("examples/output/interactive_scatter.html")
    print("Created: examples/output/interactive_scatter.html")


def example_batch_processing():
    """Example 6: Batch processing."""
    print("\n=== Example 6: Batch Processing ===")

    plotter = ScientificPlotter()

    data_paths = [
        "examples/data/scatter_data.csv",
        "examples/data/distribution_data.csv",
        "examples/data/comparison_data.csv",
    ]

    configs = [
        {"chart_type": "sci_scatter_regression", "style": "nature"},
        {"chart_type": "stat_distribution", "style": "science"},
        {"chart_type": "comp_grouped_bar", "style": "ieee"},
    ]

    output_paths = plotter.batch_create(
        data_paths,
        configs,
        "examples/output/batch",
        format="png"
    )

    print(f"Created {len(output_paths)} charts in batch")


def example_auto_chart():
    """Example 7: Automatic chart selection."""
    print("\n=== Example 7: Auto Chart Selection ===")

    plotter = ScientificPlotter()
    from core.utils import auto_select_chart_type

    # Load data and auto-select chart type
    data = plotter.data_loader.load("examples/data/correlation_data.csv")
    chart_type = auto_select_chart_type(data)
    print(f"Auto-selected chart type: {chart_type}")

    config = PlotConfig(chart_type=chart_type, style="minimal")
    fig = plotter.create_chart(data, config)
    fig.save("examples/output/auto_chart.png")
    print("Created: examples/output/auto_chart.png")


def main():
    """Run all examples."""
    # Create output directory
    Path("examples/output").mkdir(parents=True, exist_ok=True)
    Path("examples/output/batch").mkdir(parents=True, exist_ok=True)

    # Create sample data
    create_sample_data()

    # Run examples
    example_basic_usage()
    example_templates()
    example_publication_ready()
    example_ml_charts()
    example_interactive()
    example_batch_processing()
    example_auto_chart()

    print("\n=== All examples completed! ===")
    print("Check the 'examples/output' directory for generated charts.")


if __name__ == "__main__":
    main()
