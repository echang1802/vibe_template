import pytest
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

@pytest.fixture
def sample_sales_data() -> pd.DataFrame:
    foo = pd.DataFrame({
        "date": [datetime(2026, 1, 1) + timedelta(days=i) for i in range(60)],
        "store_id": ["store_001"] * 60,
        "item_id": ["item_001"] * 60,
        "price": np.random.uniform(10.0, 20.0, size=60),
        "sales_units": np.random.randint(10, 15, size=60),
    })
    return foo
