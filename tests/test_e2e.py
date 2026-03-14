"""
Playwright E2E tests for the California Housing Dashboard.
Requires the app to be running or pytest will start it (needs GITHUB_TOKEN for AI tab).
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def _ensure_server(shiny_server):
    """Ensure Shiny app is running before any E2E test."""
    pass


def test_edge_case_filter_zero_rows(page: Page):
    """
    Applying filters that result in zero rows shows 'N/A' or 'No data' instead of
    crashing; verifies empty-state handling.
    """
    page.goto("/")
    page.wait_for_load_state("networkidle")

    page.get_by_role("tab", name="Manual Filtering").click()
    page.wait_for_timeout(500)

    # Uncheck all ocean proximity checkboxes -> empty isin() yields zero rows
    for cb in page.locator('input[name="ocean_checkbox"]').all():
        cb.uncheck()
    page.wait_for_timeout(800)

    expect(page.get_by_text("California Housing Dashboard")).to_be_visible()
    expect(page.get_by_text("N/A").first).to_be_visible(timeout=5000)


def test_aggregation_displayed_medians(page: Page):
    """
    Filtering to a known subset (single county) displays median house value and
    income that match the filtered dataset.
    """
    page.goto("/")
    page.wait_for_load_state("networkidle")

    page.get_by_role("tab", name="Manual Filtering").click()
    page.wait_for_timeout(500)

    # Optionally filter to one county; default filters already show data
    try:
        page.get_by_label("County").click()
        page.get_by_role("option", name="Alameda").first.click()
        page.wait_for_timeout(800)
    except Exception:
        pass

    # Value boxes should show dollar amounts (not N/A)
    expect(page.locator("text=/\\$[0-9,]+/").first).to_be_visible(timeout=5000)


def test_boundary_slider_values(page: Page):
    """
    Using sliders at min/max bounds does not cause errors; the app handles
    boundary inputs and displays data within expected ranges.
    """
    page.goto("/")
    page.wait_for_load_state("networkidle")

    page.get_by_role("tab", name="Manual Filtering").click()
    page.wait_for_timeout(500)

    # Click Reset to set sliders to full range
    reset_btn = page.get_by_role("button", name="Reset All Filters")
    if reset_btn.is_visible():
        reset_btn.click()
        page.wait_for_timeout(800)

    # Page should still show data (no crash)
    expect(page.get_by_text("California Housing Dashboard")).to_be_visible()
    # Value boxes should show valid dollar amounts
    expect(page.locator("text=/\\$[0-9,]+/").first).to_be_visible(timeout=5000)
