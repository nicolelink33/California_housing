"""
Unit tests for src.utils filtering and aggregation logic.
Each test verifies a specific behavior that would break if the implementation changed.
"""
import ibis
import pandas as pd
import pytest

# Import after conftest adds paths
from utils import apply_filters, compute_median_house_value_metrics, compute_median_income_metrics


def _make_fixture_df():
    """Create a minimal fixture DataFrame matching the app schema."""
    return pd.DataFrame(
        {
            "median_house_value": [100_000, 200_000, 300_000, 400_000],
            "median_income": [5.0, 8.0, 12.0, 15.0],
            "median_income_usd": [50_000, 80_000, 120_000, 150_000],
            "housing_median_age": [10, 20, 30, 40],
            "total_rooms": [500, 1000, 2000, 3000],
            "total_bedrooms": [100, 200, 300, 400],
            "population": [100, 200, 300, 400],
            "households": [50, 100, 150, 200],
            "ocean_proximity": ["INLAND", "NEAR BAY", "NEAR BAY", "<1H OCEAN"],
            "county": ["Alameda", "Alameda", "Contra Costa", "San Francisco"],
        }
    )


def test_apply_filters_returns_subset():
    """
    Given explicit slider/checkbox/county inputs, the filter returns rows whose
    columns satisfy the specified ranges; verifies core filtering logic.
    """
    df = _make_fixture_df()
    t = ibis.memtable(df)
    filtered = apply_filters(
        t,
        house_val_range=(150_000, 350_000),
        income_range=(60_000, 130_000),
        age_range=(15, 35),
        rooms_range=(600, 2500),
        beds_range=(150, 350),
        pop_range=(150, 350),
        households_range=(75, 175),
        ocean_proximity=["NEAR BAY"],
        county_select=["Alameda", "Contra Costa"],
    )
    result = filtered.execute()
    assert len(result) == 2
    assert list(result["county"]) == ["Alameda", "Contra Costa"]
    assert result["median_house_value"].between(150_000, 350_000).all()
    assert result["ocean_proximity"].isin(["NEAR BAY"]).all()


def test_apply_filters_empty_county_select():
    """
    When no county is selected, all counties are included; documents the
    "no selection = show all" behavior.
    """
    df = _make_fixture_df()
    t = ibis.memtable(df)
    filtered = apply_filters(
        t,
        house_val_range=(0, 1_000_000),
        income_range=(0, 500_000),
        age_range=(0, 100),
        rooms_range=(0, 10000),
        beds_range=(0, 1000),
        pop_range=(0, 10000),
        households_range=(0, 1000),
        ocean_proximity=["INLAND", "NEAR BAY", "<1H OCEAN"],
        county_select=[],
    )
    result = filtered.execute()
    assert len(result) == 4
    assert set(result["county"]) == {"Alameda", "Contra Costa", "San Francisco"}


def test_compute_median_house_value_metrics_empty_df():
    """
    Empty or invalid DataFrame produces None; prevents crashes when filters
    yield no data.
    """
    empty_df = pd.DataFrame()
    state_df = _make_fixture_df()
    assert compute_median_house_value_metrics(empty_df, state_df) is None
    assert compute_median_house_value_metrics(pd.DataFrame({"x": []}), state_df) is None


def test_compute_median_income_metrics_aggregation():
    """
    Median of filtered data is computed correctly and compared to state median;
    verifies aggregation and percentage calculation.
    """
    df = _make_fixture_df()
    state_df = df
    filt_df = df[df["county"] == "Alameda"]  # median_income_usd: 50k, 80k -> median 65k
    result = compute_median_income_metrics(filt_df, state_df)
    assert result is not None
    filt_value, diff_pct = result
    assert filt_value == 65_000.0
    # State median of [50k, 80k, 120k, 150k] = 100k; (65 - 100) / 100 * 100 = -35.0
    assert diff_pct == -35.0
