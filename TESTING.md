# Testing

## How to run

```bash
conda activate dsci-532-dashboard  # or california-housing
playwright install                 # one-time
pytest --base-url http://127.0.0.1:8765
```

## Test coverage

### Unit tests (`tests/test_utils.py`)

| Test | What it covers | What breaks if behavior changes |
|------|----------------|---------------------------------|
| `test_apply_filters_returns_subset` | Core filtering logic: given explicit ranges and selections, only rows satisfying all conditions are returned. | Filters would return incorrect subsets; manual filtering tab would show wrong data. |
| `test_apply_filters_empty_county_select` | When no county is selected, all counties are included (“no selection = show all”). | Selecting no county would incorrectly filter out all rows. |
| `test_compute_median_house_value_metrics_empty_df` | Empty or invalid DataFrame returns `None`, avoiding crashes when filters yield no data. | Value boxes could crash or show wrong values for empty state. |
| `test_compute_median_income_metrics_aggregation` | Median income is computed correctly and percentage difference from state median is accurate. | Median income value box and percent-difference display would be wrong. |

### E2E tests (`tests/test_e2e.py`)

| Test | What it covers | What breaks if behavior changes |
|------|----------------|---------------------------------|
| `test_edge_case_filter_zero_rows` | Unchecking all ocean proximity options yields zero rows; dashboard shows “N/A” or “No data” instead of crashing. | Empty filter state would crash or show misleading data. |
| `test_aggregation_displayed_medians` | Filtering (including optional county selection) displays median house value and income as dollar amounts. | Value boxes would not update or show incorrect aggregations. |
| `test_boundary_slider_values` | Reset button and full-range sliders work; app handles boundary inputs without errors. | Extreme or reset filter states could cause errors or incorrect display. |

## Reflection

The tests focus on the manual filtering flow: `apply_filters` logic, empty-state handling, and aggregation correctness. If the filter semantics change (e.g., OR vs AND, inclusive bounds, empty county meaning), the unit tests will fail and signal the breaking change. The E2E tests ensure the UI still renders and shows expected empty or populated states under realistic filter combinations. The AI Chatbot tab is not covered by these tests and may require `GITHUB_TOKEN` for the app to start.
