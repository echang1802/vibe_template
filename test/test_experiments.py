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
    assert callable(getattr(pipeline, "train", None)), "'train' should be callable"

@pytest.mark.unit_test
def test_read_experimentation_method():
    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")

    assert pipeline.experiment is not None, "Experiment should not be None"
    assert pipeline.experiment["readed"], "Experiment should be read"
    assert type(pipeline.experiment) == dict, "Experiment should be a dictionary"
    assert pipeline.experiment["name"] == "Sample Forecast Experiment", "Experiment name should match"

@pytest.mark.unit_test
def test_read_unexisting_experimentation_method():
    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("missing_forecast.yml")

    assert pipeline.experiment is not None, "Experiment should not be None"
    assert not pipeline.experiment["readed"], "Experiment should not be read"

@pytest.mark.unit_test
def test_lag_feature_function_exists():
    feature_engineering = get_feature_engineering()
    assert hasattr(feature_engineering, "create_lag_features"), "feature_engineering should have a 'create_lag_features' method"
    assert callable(feature_engineering.create_lag_features), "'create_lag_features' should be callable"

@pytest.mark.unit_test
def test_lag_feature_function_behavior(sample_sales_data):
    feature_engineering = get_feature_engineering()
    df_with_lags = feature_engineering.create_lag_features(sample_sales_data, date_column="date", group_columns=[], target_column="sales_units", lag=1)

    assert type(df_with_lags) == type(sample_sales_data), "Output should be a DataFrame"
    assert all(col in df_with_lags.columns for col in sample_sales_data.columns), "All original columns should be present"
    assert "sales_units_lag_1" in df_with_lags.columns, "Lagged column should be present"

@pytest.mark.unit_test
@pytest.mark.parametrize("lag", [(1), (7), (14), (28)])
def test_lag_feature_function_various_lags(sample_sales_data, lag):
    feature_engineering = get_feature_engineering()
    df_with_lags = feature_engineering.create_lag_features(sample_sales_data, date_column="date", group_columns=[], target_column="sales_units", lag=lag)

    assert (
        df_with_lags.iloc[lag:][f"sales_units_lag_{lag}"].tolist()
        == sample_sales_data.iloc[:-lag]["sales_units"].tolist()
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

@pytest.mark.unit_test
def test_wape_calculates_weighted_absolute_percentage_error():
    from app.experiments.metrics import wape

    score = wape([100, 200], [90, 180])

    assert score == pytest.approx(0.1)

@pytest.mark.unit_test
def test_train_model_selects_algorithm_with_lowest_wape():
    training = get_training()

    target_by_value = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 40.0, 41.0, 42.0]
    input_order = [9, 1, 7, 2, 10, 5, 4, 8, 3, 6]
    feature_matrix = [[float(value)] for value in input_order]
    target_values = [target_by_value[value - 1] for value in input_order]
    dates = [f"2026-01-{value:02d}" for value in input_order]
    algorithm_configs = [
        {
            "name": "Linear Regression",
            "estimator": "LinearRegression",
            "params": {},
        },
        {
            "name": "Decision Tree",
            "estimator": "DecisionTreeRegressor",
            "params": {},
        },
    ]

    result = training.train_model(
        feature_matrix,
        target_values,
        dates,
        algorithm_configs,
        test_fraction=0.3,
    )

    best_competitor = min(result["competition"], key=lambda competitor: competitor["wape"])
    assert result["algorithm_name"] == best_competitor["algorithm_name"]
    assert result["wape"] == best_competitor["wape"]
    assert result["algorithm_name"] == "Linear Regression"
    assert result["wape"] == pytest.approx(69 / 123)

@pytest.mark.unit_test
def test_train_model_supports_randomized_parameter_search():
    training = get_training()
    feature_matrix = [[float(value)] for value in range(1, 11)]
    target_values = [float(value) for value in range(1, 11)]
    dates = [f"2026-01-{value:02d}" for value in range(1, 11)]

    result = training.train_model(
        feature_matrix,
        target_values,
        dates,
        [
            {
                "name": "Tuned Linear Regression",
                "estimator": "LinearRegression",
                "search_method": "randomized_search",
                "params": {"fit_intercept": [True, False]},
            }
        ],
        test_fraction=0.3,
    )

    assert result["model_params"]["fit_intercept"] in [True, False]
    assert result["competition"][0]["wape"] == result["wape"]


# -----------------------------------------------------
# ----------  Pipeline integration Tests --------------
# -----------------------------------------------------

@pytest.mark.integration_test
def test_read_input_data(pipeline_test_directory):
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
def test_output_model_after_training(pipeline_test_directory):
    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")
    pipeline.experiment["algorithms"] = [
        {
            "name": "Test Linear Regression",
            "estimator": "LinearRegression",
            "params": {},
        }
    ]
    pipeline.read_data("sample_sales_data.csv")

    pipeline.preprocessing()
    pipeline.train()
    path = pipeline.save_model("integration_model.pkl")

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
def test_pipeline_end_to_end(pipeline_test_directory):
    from pandas import DataFrame

    Pipeline = get_pipeline()
    pipeline = Pipeline()

    pipeline.get_experiment("sample_forecast.yml")
    pipeline.experiment["algorithms"] = [
        {
            "name": "Test Linear Regression",
            "estimator": "LinearRegression",
            "params": {},
        }
    ]
    pipeline.read_data("sample_sales_data.csv")

    pipeline.preprocessing()
    pipeline.train()
    path = pipeline.save_model("e2e_model.pkl")

    assert pipeline.input_data is not None, "Input data should not be None"
    assert type(pipeline.input_data) == DataFrame, "Input data should be a DataFrame"
    assert "sales_units_lag_1" in pipeline.input_data.columns, "Lagged column should be present in input data"
    assert "sales_units_lag_7" in pipeline.input_data.columns, "Lagged column should be present in input data"

    assert pipeline.model is not None, "Model should not be None after training"
    assert type(pipeline.model) == dict, "Model should be dictionary"
    assert "algorithm_name" in pipeline.model.keys(), "Model should have 'algorithm_name'"
    assert "model_params" in pipeline.model.keys(), "Model should have 'model_params'"
    assert path.exists(), "Model file should be saved as 'e2e_model.pkl'"
    assert path.is_file(), "Model file should be a regular file"
    