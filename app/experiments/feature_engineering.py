"""Feature engineering helpers for demand forecasting."""

import pandas as pd


def create_lag_features(
    input_data: pd.DataFrame,
    date_column: str,
    group_columns : list[str],
    target_column: str,
    lag: int,
) -> pd.DataFrame:
    """Return a copy of the input with a target lag calculated per group."""
    output_data = input_data.copy()
    row_positions = pd.Series(range(len(input_data)), index=input_data.index)
    ordered_data = input_data.assign(_row_position=row_positions.to_numpy())
    ordered_data = ordered_data.sort_values(
        [*group_columns, date_column, "_row_position"],
        kind="stable",
    )
    if group_columns:
        lagged_values = ordered_data.groupby(
            group_columns, sort=False, dropna=False
        )[target_column].shift(lag)
    else:
        lagged_values = ordered_data[target_column].shift(lag)

    lagged_by_position = pd.Series(
        lagged_values.to_numpy(),
        index=ordered_data["_row_position"].to_numpy(),
    )
    output_data[f"{target_column}_lag_{lag}"] = [
        lagged_by_position[position] for position in range(len(input_data))
    ]
    return output_data
