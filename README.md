# Demand Forecasting Template

This repository separates analyst-led model experiments from the application that
will eventually consume the selected model. The forecasting experiment pipeline
is implemented; the backend and frontend are currently scaffolds for future
model-serving and user-interface code.

## Repository guide

| Path | Purpose |
| --- | --- |
| `app/experiments/` | Analyst-facing feature preparation, model training, WAPE evaluation, and experiment configuration. |
| `app/experiments/experiments/sample_forecast.yml` | Example configuration for a sales forecast experiment. |
| `app/experiments/models/` | Destination for serialized model results created by the pipeline. |
| `app/backend/` | Intended home for application/API code that loads and uses a trained model. It is currently a placeholder. |
| `app/frontend/` | Intended home for the UI that will use the backend. It is currently a placeholder. |
| `test/experiments/test_experiments.py` | Unit, integration, and end-to-end tests for the experiment workflow. |
| `test/conftest.py` | Shared deterministic synthetic sales-data fixtures. |
| `test/backend/`, `test/frontend/` | Reserved test areas for the future application layers. |
| `requirements.txt` | Python packages used by the project and its tests. |
| `pyproject.toml` | Pytest import path, coverage options, and test markers. |
| `.github/workflows/ci.yml` | GitHub Actions workflow for linting, formatting, and tests. |

There is no production sales CSV in the repository. The test suite generates its
own small synthetic dataset; analysts should provide their own CSV under
`app/data/`.

## Agent instructions and development methodology

The `AGENTS.md` files provide scoped guidance for AI-assisted changes:

- [`AGENTS.md`](AGENTS.md) describes the overall workflow and links to the
  specialized instructions and user-story template.
- [`.github/AGENTS.md`](.github/AGENTS.md) defines the shared coding-agent and
  Git workflow, including branch and commit expectations.
- [`app/AGENTS.md`](app/AGENTS.md) contains application architecture, Python
  style, and implementation guidance.
- [`test/AGENTS.md`](test/AGENTS.md) defines pytest conventions, test markers,
  fixture expectations, and coverage practices.

In short, changes should start with a clear requirement and acceptance criteria,
then a proposed test plan. After review, tests are written before implementation,
the narrowest relevant tests are run, and documentation is updated when needed.
Commits require passing required tests and explicit approval. The repository
also has a [user-story template](templates/user-story-template.md).

## Technology

- **Python** is the implementation language; CI currently uses Python 3.12.
- **pandas** handles tabular input and feature preparation.
- **scikit-learn** provides regression estimators, randomized parameter search,
  and time-series cross-validation.
- **PyYAML** reads experiment configuration files.
- **pytest** and **pytest-cov** run tests and collect coverage.
- **Ruff** is referenced by CI for linting and formatting checks, but is not
  currently listed in `requirements.txt`.

No backend web framework or frontend framework has been selected or implemented
yet. The backend and frontend directories are placeholders, not runnable
applications.

## Forecast experiment workflow

`Pipeline` in `app/experiments/main.py` coordinates the experiment:

1. Load a YAML configuration from `app/experiments/experiments/`.
2. Read the configured sales CSV from `app/data/`.
3. Generate target lag features, within each configured group when applicable,
   and remove rows without the required lag history.
4. Train each configured regression estimator and score its predictions on a
   chronological holdout.
5. Select the candidate with the lowest WAPE and return its estimator,
   parameters, score, and competition results.
6. Optionally serialize the result to `app/experiments/models/`.

The training API also supports the configuration's `randomized_search` option.
Its parameter search uses time-series cross-validation. The selected estimator
is refit on the complete dataset after holdout scoring.

### Experiment modules

- `feature_engineering.py` creates lagged target columns without changing the
  input data's row order.
- `training.py` resolves configured scikit-learn regressors, compares their
  holdout WAPE scores, and returns the winning fitted model.
- `metrics.py` contains WAPE, calculated as the sum of absolute errors divided
  by the sum of absolute actual values. Lower scores are better; WAPE is
  undefined when all actual values are zero.
- `main.py` handles configuration, CSV loading, preprocessing, training, and
  saving the model result.

### Example configuration

[`sample_forecast.yml`](app/experiments/experiments/sample_forecast.yml) shows
the expected configuration shape. It names the date, target, grouping columns,
lags, and feature columns, sets a holdout fraction, and compares a
`LinearRegression` with a `RandomForestRegressor` using randomized search.

The input CSV must contain the columns referenced by the YAML file. For the
sample configuration these include `date`, `store_id`, `item_id`, `price`, and
`sales_units`. Use consistently formatted dates (for example, `YYYY-MM-DD`) so
the chronological split follows time order.

### Run an experiment

Create `app/data/` if it does not exist and put a compatible CSV there. Then,
from the repository root:

```python
from app.experiments.main import Pipeline

pipeline = Pipeline()
pipeline.get_experiment("sample_forecast.yml")
pipeline.read_data("sample_sales_data.csv")
pipeline.preprocessing()
result = pipeline.train()

print(result["algorithm_name"])
print(result["wape"])
pipeline.save_model("sales_forecast.pkl")
```

For a different dataset, place its CSV under `app/data/` and pass that filename
to `read_data`.

`save_model` writes the serialized result to
`app/experiments/models/sales_forecast.pkl`. The repository does not currently
provide a command-line runner or a web endpoint for executing experiments.

## Setup and tests

Create and activate a virtual environment, then install the declared
dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run all tests from the repository root:

```powershell
python -m pytest
```

Tests are marked by scope; run one group at a time with:

```powershell
python -m pytest -m unit_test
python -m pytest -m integration_test
python -m pytest -m e2e_test
```

The experiment tests are in
[`test/experiments/test_experiments.py`](test/experiments/test_experiments.py).
Their shared fixture creates deterministic sales data, and integration tests
use temporary directories for CSVs and serialized models.

CI additionally runs Ruff checks and formatting validation before tests, and
requires at least 80% test coverage. Install Ruff separately if you want to run
those lint and format commands locally.
