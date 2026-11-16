"""Model training and competition helpers for forecasting experiments."""

from collections.abc import Sequence
from math import ceil
from typing import Any

from sklearn.base import BaseEstimator
from sklearn.metrics import make_scorer
from sklearn.model_selection import ParameterGrid, RandomizedSearchCV, TimeSeriesSplit
from sklearn.utils import all_estimators

from app.experiments.metrics import wape


def _get_regressor_class(estimator_name: str) -> type[BaseEstimator]:
    """Resolve a configured scikit-learn regressor name."""
    normalized_name = estimator_name.lower().replace("_", "")
    for name, estimator_class in all_estimators(type_filter="regressor"):
        if name.lower().replace("_", "") == normalized_name:
            return estimator_class
    raise ValueError(f"Unknown scikit-learn regressor: {estimator_name}")


def train_model(
    feature_matrix: Sequence[Sequence[float]],
    target_values: Sequence[float],
    dates: Sequence[str],
    algorithm_configs: Sequence[dict[str, Any]],
    test_fraction: float = 0.2,
) -> dict[str, Any]:
    """Train configured regressors, compare holdout WAPE, and return the winner."""
    ordered_indices = sorted(range(len(dates)), key=dates.__getitem__)
    test_size = ceil(len(ordered_indices) * test_fraction)
    split_index = len(ordered_indices) - test_size
    training_indices = ordered_indices[:split_index]
    validation_indices = ordered_indices[split_index:]

    training_features = [feature_matrix[index] for index in training_indices]
    training_targets = [target_values[index] for index in training_indices]
    validation_features = [feature_matrix[index] for index in validation_indices]
    validation_targets = [target_values[index] for index in validation_indices]

    competitors: list[dict[str, Any]] = []
    best_config: dict[str, Any] | None = None
    best_params: dict[str, Any] | None = None
    best_score = float("inf")

    for algorithm_config in algorithm_configs:
        estimator_name = algorithm_config["estimator"]
        estimator_class = _get_regressor_class(estimator_name)
        configured_params = algorithm_config.get("params", {})
        search_method = algorithm_config.get("search_method")

        if search_method == "randomized_search":
            search = RandomizedSearchCV(
                estimator_class(),
                param_distributions=configured_params,
                n_iter=min(10, len(ParameterGrid(configured_params))),
                scoring=make_scorer(wape, greater_is_better=False),
                cv=TimeSeriesSplit(n_splits=3),
                random_state=42,
            )
            search.fit(training_features, training_targets)
            fitted_estimator = search.best_estimator_
            model_params = search.best_params_
        else:
            model_params = configured_params
            fitted_estimator = estimator_class(**model_params)
            fitted_estimator.fit(training_features, training_targets)

        predictions = fitted_estimator.predict(validation_features)
        score = wape(validation_targets, predictions)
        algorithm_name = algorithm_config.get("name", estimator_name)
        competitors.append(
            {
                "algorithm_name": algorithm_name,
                "model_params": model_params,
                "wape": score,
            }
        )
        if score < best_score:
            best_config = algorithm_config
            best_params = model_params
            best_score = score

    best_estimator_class = _get_regressor_class(best_config["estimator"])
    best_model = best_estimator_class(**best_params)
    ordered_features = [feature_matrix[index] for index in ordered_indices]
    ordered_targets = [target_values[index] for index in ordered_indices]
    best_model.fit(ordered_features, ordered_targets)

    return {
        "algorithm_name": best_config.get("name", best_config["estimator"]),
        "model_params": best_params,
        "model": best_model,
        "wape": best_score,
        "competition": competitors,
    }


train = train_model
