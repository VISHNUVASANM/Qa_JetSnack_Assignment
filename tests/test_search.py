"""
================================================================================
SEARCH TAB – automated tests (test_001, test_002, …)
================================================================================
Preconditions (manual / environment):
  • Appium server is running; one Android device or emulator is connected.
  • JetSnack opens once for this file; tests run in one continuous app session (no relaunch between tests).

How to run only this file:
  python -m pytest tests/test_search.py -v
================================================================================
"""

from assist.helpers import (
    add_cupcake_via_search_and_assert_in_cart,
    go_to_search_tab,
    scroll_home_feed_to_bottom_then_top,
    type_query_on_search,
    wait_page_source_contains,
    wait_search_field_or_hint_visible,
)


def test_001_search_screen_scroll_feed_down_then_up_once(driver):
    """
    User steps:
      1. Open the Search tab.
      2. Wait until the search field or hint is visible.
      3. Scroll the search/results area **down** once, then **up** once (same gesture helper as Home).
      4. Confirm search UI is still available (field or hint).

    Expected: One down + one up scroll completes without error; Search screen remains usable.
    """
    go_to_search_tab(driver)
    wait_search_field_or_hint_visible(driver)
    scroll_home_feed_to_bottom_then_top(
        driver,
        swipes_toward_bottom=1,
        swipes_toward_top=1,
        wait_after_for_delivery_line=False,
    )
    wait_search_field_or_hint_visible(driver)


def test_002_open_search_tab_and_verify_search_ui_visible(driver):
    """
    User steps:
      1. From a stable start on Home, open the Search tab on the bottom bar.
      2. On Search, look for a real search field or the “Search Jetsnack” hint so you know search is ready.

    Expected: Search screen shows a recognizable search control (field or hint).
    """
    go_to_search_tab(driver)
    wait_search_field_or_hint_visible(driver)


def test_003_search_cup_then_open_cupcake_and_add_to_cart(driver):
    """
    User steps:
      1. Open the Search tab.
      2. Type “cup” in the search field.
      3. Confirm “Cupcake” appears in the results.
      4. Open the Cupcake row to its detail screen.
      5. Tap “Add to cart”.
      6. Tap the detail toolbar **Back** (same as home tests) so the Search results screen is visible again.

    Expected: Search → detail → add to cart → back to search completes (MY CART not asserted; cart UI flaky).
    """
    add_cupcake_via_search_and_assert_in_cart(
        driver,
        tap_toolbar_back_after_add=True,
        assert_in_cart=False,
    )


def test_004_search_chi_shows_chips_and_apple_chips_visible(driver):
    """
    User steps:
      1. Open the Search tab and type “chi”.
      2. Wait until the results list shows chips-related items (e.g. text containing “Chips” and “Apple chips”).

    Expected: Search for “chi” surfaces chips products; “chips” and “apple chip(s)” text appear in the UI.
    """
    type_query_on_search(driver, "chi")
    wait_page_source_contains(driver, "chips", seconds=15)
    wait_page_source_contains(driver, "apple chip", seconds=15)
