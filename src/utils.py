"""
Pure functions for dashboard filtering and aggregation logic.
Extracted for testability.
"""
import pandas as pd


def apply_filters(
    df: pd.DataFrame,
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
) -> pd.DataFrame:
    """
    Filter the housing dataframe by the given ranges and selections.
    Returns rows where all conditions are satisfied (AND logic).
    Empty county_select means include all counties.
    """
    idx_house_val = df.median_house_value.between(
        left=house_val_range[0], right=house_val_range[1], inclusive="both"
    )
    idx_income = df.median_income_usd.between(
        left=income_range[0], right=income_range[1], inclusive="both"
    )
    idx_age = df.housing_median_age.between(
        left=age_range[0], right=age_range[1], inclusive="both"
    )
    idx_rooms = df.total_rooms.between(
        left=rooms_range[0], right=rooms_range[1], inclusive="both"
    )
    idx_beds = df.total_bedrooms.between(
        left=beds_range[0], right=beds_range[1], inclusive="both"
    )
    idx_pop = df.population.between(
        left=pop_range[0], right=pop_range[1], inclusive="both"
    )
    idx_households = df.households.between(
        left=households_range[0], right=households_range[1], inclusive="both"
    )
    idx_ocean = df.ocean_proximity.isin(ocean_proximity)

    selected_counties = [c.strip() for c in county_select] if county_select else []
    idx_county = (
        df.county.isin(selected_counties)
        if selected_counties
        else pd.Series(True, index=df.index)
    )

    return df[
        idx_house_val
        & idx_income
        & idx_age
        & idx_rooms
        & idx_beds
        & idx_pop
        & idx_households
        & idx_ocean
        & idx_county
    ]


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
