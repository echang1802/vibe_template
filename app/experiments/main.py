"""Demand forecasting pipeline orchestration."""

import pickle
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from app.experiments.feature_engineering import create_lag_features
from app.experiments.training import train as train_model


PROJECT_DIRECTORY = Path(__file__).resolve().parents[2]
EXPERIMENTS_DIRECTORY = Path(__file__).resolve().parent / "experiments"
DATA_DIRECTORY = PROJECT_DIRECTORY / "app" / "data"
MODELS_DIRECTORY = PROJECT_DIRECTORY / "app" / "experiments" / "models"


class Pipeline:
    """Load an experiment, prepare data, train a model, and save its artifact."""

    def __init__(self) -> None:
        self.experiment: dict[str, Any] = {"readed": False}
        self.raw_data: pd.DataFrame | None = None
        self.input_data: pd.DataFrame | None = None
        self.model: dict[str, Any] | None = None

    def get_experiment(self, experiment_filename: str) -> dict[str, Any]:
        """Load a YAML experiment by filename from the experiments directory."""
        self.experiment = {"readed": False}

        experiment_path = (EXPERIMENTS_DIRECTORY / experiment_filename).resolve()        
        if not experiment_path.is_file():
            return self.experiment

        with experiment_path.open(encoding="utf-8") as experiment_file:
            experiment = yaml.safe_load(experiment_file)

        experiment["readed"] = True
        self.experiment = experiment
        return self.experiment

    def read_data(self, data_filename: str) -> pd.DataFrame:
        """Read a CSV file from app/data for the loaded experiment."""
        data_path = (DATA_DIRECTORY / data_filename).resolve()
        self.raw_data = pd.read_csv(data_path)
        self.input_data = None
        self.model = None
        return self.raw_data

    def preprocessing(self) -> pd.DataFrame:
        """Create configured lag features and remove rows without lag history."""

        date_column = self.experiment.get("date_column", "date")
        group_columns = self.experiment.get("group_columns", [])
        target_column = self.experiment.get("target_column", "sales_units")
        
        lag_periods = self.experiment.get("lags", [1, 7])

        prepared_data = self.raw_data.copy()
        for lag_period in lag_periods:
            prepared_data = create_lag_features(
                prepared_data,
                date_column=date_column, 
                group_columns = group_columns,
                target_column=target_column,
                lag=lag_period,
            )
        lag_columns = [f"{target_column}_lag_{lag}" for lag in lag_periods]
        prepared_data = prepared_data.dropna(subset=lag_columns).reset_index(drop=True)
        self.input_data = prepared_data
        return prepared_data

    def train(self) -> dict[str, Any]:
        """Train configured algorithms and retain the best fitted model."""

        target_column = self.experiment.get("target_column", "sales_units")
        date_column = self.experiment.get("date_column", "date")
        configured_features = self.experiment.get("features")
        missing_features = [
            feature
            for feature in configured_features
            if feature not in self.input_data.columns
        ]
        if missing_features:
            raise ValueError(f"Configured features were not found: {missing_features}")

        algorithms = self.experiment.get("algorithms")
        feature_matrix = self.input_data[configured_features].astype(float).values.tolist()
        target_values = self.input_data[target_column].astype(float).tolist()
        dates = self.input_data[date_column].astype(str).tolist()
        self.model = train_model(
            feature_matrix,
            target_values,
            dates,
            algorithms,
            test_fraction=self.experiment.get("test_fraction", 0.2),
        )
        return self.model

    def save_model(self, model_filename: str) -> Path:
        """Serialize the fitted model under app/experiments/models."""
        MODELS_DIRECTORY.mkdir(parents=True, exist_ok=True)
        model_path = MODELS_DIRECTORY / model_filename
        with model_path.open("wb") as model_file:
            pickle.dump(self.model, model_file)
        return model_path