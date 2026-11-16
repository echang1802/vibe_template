"""Evaluation metrics for forecasting experiments."""

from collections.abc import Sequence


def wape(actual_values: Sequence[float], predicted_values: Sequence[float]) -> float:
    """Calculate weighted absolute percentage error as a fraction."""
    absolute_errors = (
        abs(actual - predicted)
        for actual, predicted in zip(actual_values, predicted_values, strict=True)
    )
    return float(sum(absolute_errors) / sum(abs(actual) for actual in actual_values))
