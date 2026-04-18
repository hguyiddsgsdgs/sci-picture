"""Utility functions for data loading and caching."""

import hashlib
import pickle
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd


class DataLoader:
    """Load data from various formats."""

    def load(self, path: Union[str, Path]) -> pd.DataFrame:
        """Load data from file.

        Args:
            path: Path to data file

        Returns:
            DataFrame

        Raises:
            ValueError: If file format not supported
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()

        if suffix == ".csv":
            return pd.read_csv(path)
        elif suffix in [".xls", ".xlsx"]:
            return pd.read_excel(path)
        elif suffix == ".json":
            return pd.read_json(path)
        elif suffix == ".parquet":
            return pd.read_parquet(path)
        elif suffix in [".h5", ".hdf5"]:
            return pd.read_hdf(path)
        elif suffix == ".pkl":
            return pd.read_pickle(path)
        elif suffix == ".feather":
            return pd.read_feather(path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def save(self, df: pd.DataFrame, path: Union[str, Path], format: Optional[str] = None):
        """Save DataFrame to file.

        Args:
            df: DataFrame to save
            path: Output path
            format: Output format (inferred from path if None)
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format is None:
            format = path.suffix.lower()[1:]  # Remove dot

        if format == "csv":
            df.to_csv(path, index=False)
        elif format in ["xls", "xlsx"]:
            df.to_excel(path, index=False)
        elif format == "json":
            df.to_json(path, orient="records", indent=2)
        elif format == "parquet":
            df.to_parquet(path, index=False)
        elif format in ["h5", "hdf5"]:
            df.to_hdf(path, key="data", mode="w")
        elif format == "pkl":
            df.to_pickle(path)
        elif format == "feather":
            df.to_feather(path)
        else:
            raise ValueError(f"Unsupported format: {format}")


class CacheManager:
    """Manage caching of plot results."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize cache manager.

        Args:
            cache_dir: Directory for cache files. If None, uses default.
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "scientific_plotter"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            try:
                with cache_file.open("rb") as f:
                    return pickle.load(f)
            except Exception:
                # Cache corrupted, remove it
                cache_file.unlink()
        return None

    def set(self, key: str, value: Any):
        """Set cached value.

        Args:
            key: Cache key
            value: Value to cache
        """
        cache_file = self.cache_dir / f"{key}.pkl"
        try:
            with cache_file.open("wb") as f:
                pickle.dump(value, f)
        except Exception:
            # Failed to cache, ignore
            pass

    def clear(self):
        """Clear all cached values."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()

    def get_cache_size(self) -> int:
        """Get total cache size in bytes."""
        return sum(f.stat().st_size for f in self.cache_dir.glob("*.pkl"))


def generate_hash(data: Any) -> str:
    """Generate MD5 hash for data.

    Args:
        data: Data to hash

    Returns:
        MD5 hash string
    """
    if isinstance(data, pd.DataFrame):
        data_bytes = pd.util.hash_pandas_object(data).values.tobytes()
    elif isinstance(data, (str, bytes)):
        data_bytes = data.encode() if isinstance(data, str) else data
    else:
        data_bytes = str(data).encode()

    return hashlib.md5(data_bytes).hexdigest()


def validate_dataframe(df: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """Validate DataFrame structure.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Returns:
        True if valid

    Raises:
        ValueError: If validation fails
    """
    if df.empty:
        raise ValueError("DataFrame is empty")

    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    return True


def infer_column_types(df: pd.DataFrame) -> dict:
    """Infer semantic types of DataFrame columns.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary mapping column names to types
    """
    column_types = {}

    for col in df.columns:
        dtype = df[col].dtype

        if pd.api.types.is_numeric_dtype(dtype):
            # Check if it's actually categorical (few unique values)
            if df[col].nunique() < 10:
                column_types[col] = "categorical_numeric"
            else:
                column_types[col] = "continuous"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            column_types[col] = "datetime"
        elif pd.api.types.is_categorical_dtype(dtype) or pd.api.types.is_object_dtype(dtype):
            column_types[col] = "categorical"
        elif pd.api.types.is_bool_dtype(dtype):
            column_types[col] = "boolean"
        else:
            column_types[col] = "unknown"

    return column_types


def auto_select_chart_type(df: pd.DataFrame) -> str:
    """Automatically suggest a chart type based on data.

    Args:
        df: DataFrame to analyze

    Returns:
        Suggested chart type
    """
    column_types = infer_column_types(df)
    n_cols = len(df.columns)
    n_rows = len(df)

    # Count column types
    n_continuous = sum(1 for t in column_types.values() if t == "continuous")
    n_categorical = sum(1 for t in column_types.values() if t in ["categorical", "categorical_numeric"])
    n_datetime = sum(1 for t in column_types.values() if t == "datetime")

    # Also treat a datetime index as a datetime dimension
    has_datetime_index = pd.api.types.is_datetime64_any_dtype(df.index)
    if has_datetime_index:
        n_datetime += 1

    # Decision logic
    if n_datetime >= 1 and n_continuous >= 1:
        return "ts_line"
    elif n_continuous >= 2:
        if n_continuous == 2:
            return "sci_scatter_regression"
        else:
            return "stat_correlation_heatmap"
    elif n_categorical >= 1 and n_continuous >= 1:
        if n_categorical == 1:
            return "comp_bar"
        else:
            return "comp_grouped_bar"
    elif n_continuous >= 1:
        return "stat_distribution"
    else:
        return "comp_bar"  # Default fallback
