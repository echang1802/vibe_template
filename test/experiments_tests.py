import pytest

def get_pipeline():
    from app.experiments.main import Pipeline

    return Pipeline

def get_feature_engineering():
    from app.experiments import feature_engineering

    return feature_engineering 

def get_training():
    from app.experiments import training

    return training

# -----------------------------------------------------
# -------------  Pipeline Unit Tests ------------------
# -----------------------------------------------------

@pytest.mark.unit_test
def test_pipeline_initialization():
    Pipeline = get_pipeline()
    pipeline = Pipeline()
    assert pipeline is not None, "Pipeline instance should not be None"
    assert hasattr(pipeline, "run"), "Pipeline should have a 'run' method"
    assert callable(getattr(pipeline, "run", None)), "'run' should be callable"

@pytest.mark.unit_test
def test_read_experimentation_method():
    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")

    assert pipeline.experiment is not None, "Experiment should not be None"
    assert pipeline.experiment.readed, "Experiment should be read"
    assert type(pipeline.experiment) == dict, "Experiment should be a dictionary"
    assert pipeline.experiment.name == "Sample Forecast Experiment", "Experiment name should match"

@pytest.mark.unit_test
def test_read_unexisting_experimentation_method():
    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")

    assert pipeline.experiment is not None, "Experiment should not be None"
    assert not pipeline.experiment.readed, "Experiment should not be read"

@pytest.mark.unit_test
def test_lag_feature_function_exists():
    feature_engineering = get_feature_engineering()
    assert hasattr(feature_engineering, "create_lag_features"), "feature_engineering should have a 'create_lag_features' method"
    assert callable(feature_engineering.create_lag_features), "'create_lag_features' should be callable"

@pytest.mark.unit_test
def test_lag_feature_function_behavior(sample_sales_data):
    feature_engineering = get_feature_engineering()
    df_with_lags = feature_engineering.create_lag_features(sample_sales_data, date_column="date", target_column="sales_units", lag=1)

    assert type(df_with_lags) == type(sample_sales_data), "Output should be a DataFrame"
    assert all(col in df_with_lags.columns for col in sample_sales_data.columns), "All original columns should be present"
    assert "sales_units_lag_1" in df_with_lags.columns, "Lagged column should be present"

@pytest.mark.unit_test
@pytest.mark.parametrize("lag", [(1), (7), (14), (28)])
def test_lag_feature_function_various_lags(sample_sales_data, lag):
    feature_engineering = get_feature_engineering()
    df_with_lags = feature_engineering.create_lag_features(sample_sales_data, date_column="date", target_column="sales_units", lag=lag)

    assert all(
        df_with_lags.loc[lag:, f"sales_units_lag_{lag}"].values == sample_sales_data.loc[:-lag, "sales_units"].values
    ), f"Lagged values for lag {lag} should match the original values shifted by {lag} days"

@pytest.mark.unit_test
def test_train_function_exists():
    training = get_training()
    assert hasattr(training, "train"), "training should have a 'train' method"
    assert callable(training.train), "'train' should be callable"

@pytest.mark.unit_test
def test_train_algorithms():
    training = get_training()

    feature_matrix = [[1.0], [2.0], [3.0], [4.0], [5.0]]
    target_values = [10, 20, 30, 40, 50]
    dates = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
    algorithm_configs = [
        {
            "name": "Test Algorithm",
            "estimator": "linear_regression",
            "params": {},
        }
    ]

    results = training.train(feature_matrix, target_values, dates, algorithm_configs, test_fraction=0.2)

    assert results is not None, "Results should not be None"
    assert type(results) == dict, "Results should be a dictionary"
    assert "algorithm_name" in results.keys(), "Result should have 'algorithm_name'"
    assert "model_params" in results.keys(), "Result should have 'model_params'"


# -----------------------------------------------------
# ----------  Pipeline integration Tests --------------
# -----------------------------------------------------

@pytest.mark.integration_test
def test_read_input_data():
    from pandas import DataFrame

    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")
    pipeline.read_data("sample_sales_data.csv")

    pipeline.preprocessing()

    assert pipeline.input_data is not None, "Input data should not be None"
    assert type(pipeline.input_data) == DataFrame, "Input data should be a DataFrame"
    assert "sales_units_lag_1" in pipeline.input_data.columns, "Lagged column should be present in input data"
    assert "sales_units_lag_7" in pipeline.input_data.columns, "Lagged column should be present in input data"

@pytest.mark.integration_test
def test_output_model_after_training():
    from pathlib import Path

    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")
    pipeline.read_data("sample_sales_data.csv")

    pipeline.preprocessing()
    pipeline.train()
    pipeline.save_model("integration_model.pkl")

    path = Path("app/experiments/models/integration_model.pkl")

    assert pipeline.model is not None, "Model should not be None after training"
    assert type(pipeline.model) == dict, "Model should be dictionary"
    assert "algorithm_name" in pipeline.model.keys(), "Model should have 'algorithm_name'"
    assert "model_params" in pipeline.model.keys(), "Model should have 'model_params'"
    assert path.exists(), "Model file should be saved as 'integration_model.pkl'"
    assert path.is_file(), "Model file should be a regular file"

# -----------------------------------------------------
# -------------  Pipeline E2E Tests -------------------
# -----------------------------------------------------

@pytest.mark.e2e_test
def test_pipeline_end_to_end():
    from pathlib import Path
    from pandas import DataFrame

    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")
    pipeline.read_data("sample_sales_data.csv")

    pipeline.preprocessing()
    pipeline.train()
    pipeline.save_model("e2e_model.pkl")

    path = Path("app/experiments/models/e2e_model.pkl")

    assert pipeline.input_data is not None, "Input data should not be None"
    assert type(pipeline.input_data) == DataFrame, "Input data should be a DataFrame"
    assert "sales_units_lag_1" in pipeline.input_data.columns, "Lagged column should be present in input data"
    assert "sales_units_lag_7" in pipeline.input_data.columns, "Lagged column should be present in input data"

    assert pipeline.model is not None, "Model should not be None after training"
    assert type(pipeline.model) == dict, "Model should be dictionary"
    assert "algorithm_name" in pipeline.model.keys(), "Model should have 'algorithm_name'"
    assert "model_params" in pipeline.model.keys(), "Model should have 'model_params'"
    assert path.exists(), "Model file should be saved as 'sample_model.pkl'"
    assert path.is_file(), "Model file should be a regular file"
    