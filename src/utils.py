"""
Pure functions for dashboard filtering and aggregation logic.
Extracted for testability.
"""
import pandas as pd
import ibis


def apply_filters(
    t: ibis.Table,
    *,
    house_val_range: tuple[float, float],
    income_range: tuple[float, float],
    age_range: tuple[float, float],
    rooms_range: tuple[float, float],
    beds_range: tuple[float, float],
    pop_range: tuple[float, float],
    households_range: tuple[float, float],
    ocean_proximity: list[str],
    county_select: list[str],
):
    """
    Filter the housing dataframe by the given ranges and selections.
    Returns rows where all conditions are satisfied (AND logic).
    Empty county_select means include all counties.
    """

    conditions = [
        t.median_house_value.between(house_val_range[0], house_val_range[1]),
        t.median_income_usd.between(income_range[0], income_range[1]),
        t.housing_median_age.between(age_range[0], age_range[1]),
        t.total_rooms.between(rooms_range[0], rooms_range[1]),
        t.total_bedrooms.between(beds_range[0], beds_range[1]),
        t.population.between(pop_range[0], pop_range[1]),
        t.households.between(households_range[0], households_range[1]),
        t.ocean_proximity.isin(ocean_proximity)
    ]
    
    # Handle the "Empty = All" logic for counties
    if county_select:
        selected_counties = [c.strip() for c in county_select]
        conditions.append(t.county.isin(selected_counties))

    # Apply all filters at once
    return t.filter(conditions)


def compute_median_house_value_metrics(
    df: pd.DataFrame, state_data: pd.DataFrame
) -> tuple[float, float] | None:
    """
    Compute filtered median house value and percentage difference from state median.
    Returns (filt_value, diff_pct) or None if df is empty/invalid.
    """
    if df is None or df.empty or "median_house_value" not in df.columns:
        return None
    filt_value = round(df.median_house_value.median(), 1)
    state_value = round(state_data.median_house_value.median(), 1)
    if state_value == 0:
        return (filt_value, 0.0)
    diff = round(((filt_value - state_value) / state_value) * 100, 1)
    return (filt_value, diff)


def compute_median_income_metrics(
    df: pd.DataFrame, state_data: pd.DataFrame
) -> tuple[float, float] | None:
    """
    Compute filtered median income and percentage difference from state median.
    Returns (filt_value, diff_pct) or None if df is empty/invalid.
    """
    if df is None or df.empty or "median_income_usd" not in df.columns:
        return None
    filt_value = round(df.median_income_usd.median(), 1)
    state_value = round(state_data.median_income_usd.median(), 1)
    if state_value == 0:
        return (filt_value, 0.0)
    diff = round(((filt_value - state_value) / state_value) * 100, 1)
    return (filt_value, diff)
