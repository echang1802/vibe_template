from pathlib import Path

import pytest
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

@pytest.fixture
def sample_sales_data() -> pd.DataFrame:
    random_generator = np.random.default_rng(42)
    foo = pd.DataFrame({
        "date": [datetime(2026, 1, 1) + timedelta(days=i) for i in range(60)],
        "store_id": ["store_001"] * 60,
        "item_id": ["item_001"] * 60,
        "price": random_generator.uniform(10.0, 20.0, size=60),
        "sales_units": random_generator.integers(10, 15, size=60),
    })
    return foo


@pytest.fixture
def pipeline_test_directory(
    tmp_path: Path,
    sample_sales_data: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    from app.experiments import main

    monkeypatch.setattr(main, "DATA_DIRECTORY", tmp_path)
    monkeypatch.setattr(main, "MODELS_DIRECTORY", tmp_path / "models")
    sample_sales_data.to_csv(tmp_path / "sample_sales_data.csv", index=False)
    return tmp_path
