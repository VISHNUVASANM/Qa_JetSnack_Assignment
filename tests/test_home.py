"""
================================================================================
HOME TAB – automated tests (numbered: test_001 … test_008)
================================================================================
Preconditions (manual / environment):
  • Appium server is running on the URL in assist/config.py.
  • One Android device or emulator is connected (adb devices).
  • JetSnack installs and opens once for this file; all tests run in the same app session (no relaunch between tests).

How to run only this file:
  python -m pytest tests/test_home.py -v
================================================================================
"""

import time

from assist import config, locators
from assist.helpers import (
    add_snack_to_cart_from_list,
    go_to_home_tab,
    open_filters_wait_for_sheet_then_close,
    scroll_home_feed_to_bottom_then_top,
    tap_detail_screen_back,
    verify_home_feed_main_sections,
    wait_visible,
)
from assist.pages.jetsnack_app import JetsnackApp


def test_001_verify_app_package_and_open_home_tab(driver):
    """
    User steps:
      1. After the app opens, confirm the running app is JetSnack (package matches the project config).
      2. Open the Home tab on the bottom navigation.
      3. Wait until the delivery banner (“Delivery to …”) is visible on the feed.

    Expected: Correct app; Home feed is shown with the delivery line.
    """
    assert driver.current_package == config.APP_PACKAGE
    go_to_home_tab(driver, wait_for_delivery_banner=True, seconds=15)


def test_002_verify_delivery_banner_and_section_headers_on_feed(driver):
    """
    User steps:
      1. Go to the Home tab.
      2. On the feed, read the delivery banner and the main section titles (e.g. Android’s picks, Popular, WFH).

    Expected: Delivery line and the expected section headers are all visible.
    """
    go_to_home_tab(driver)
    verify_home_feed_main_sections(driver)


def test_003_tap_select_delivery_address_stays_on_home(driver):
    """
    User steps:
      1. Go to the Home tab.
      2. Tap “Select delivery address” on the delivery banner.
      3. Stay on Home: in this app build, no separate address screen is expected.

    Expected: After the tap, the delivery line and a feed section (e.g. Android’s picks) are still visible.
    """
    app = go_to_home_tab(driver)
    app.tap(locators.HomeHeader.SELECT_DELIVERY_ADDRESS)
    wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE, seconds=10)
    wait_visible(driver, *locators.HomeSection.ANDROID_PICKS, seconds=10)


def test_004_tap_filters_opens_filter_sheet_then_close(driver):
    """
    User steps:
      1. Go to the Home tab.
      2. Tap “Filters” on the toolbar.
      3. Wait until the filter sheet shows (e.g. Reset / Price or Sort).
      4. Close the sheet using the close control on the sheet (not the device Back key).
      5. Confirm the “Filters” control on Home is visible again.

    Expected: Sheet opens and closes cleanly; you return to the Home feed with Filters available.
    """
    app = go_to_home_tab(driver)
    open_filters_wait_for_sheet_then_close(driver, app)


def test_005_toggle_diet_filter_chips_on_home(driver):
    """
    User steps:
      1. Go to the Home tab.
      2. Tap the “Organic” diet chip, then “Gluten-free”.
      3. Tap “Organic” again, then “Gluten-free” again (toggle each twice).

    Expected: App remains stable; no crash.
    """
    app = go_to_home_tab(driver)
    app.tap(locators.FilterChips.ORGANIC)
    time.sleep(0.5)
    app.tap(locators.FilterChips.GLUTEN_FREE)
    time.sleep(0.5)
    app.tap(locators.FilterChips.ORGANIC)
    time.sleep(0.5)
    app.tap(locators.FilterChips.GLUTEN_FREE)


def test_006_visit_other_bottom_tabs_then_return_home_feed_still_visible(driver):
    """
    User steps:
      1. Start on Home and wait until the delivery banner is visible.
      2. Use the bottom bar: open Search, then My Cart, then Profile.
      3. Open Home again.
      4. Wait until the delivery banner appears on Home.

    Expected: Home feed still shows after round-trip navigation.
    """
    app = go_to_home_tab(driver)
    app.tap_bottom_tab(locators.BottomNav.SEARCH)
    app.tap_bottom_tab(locators.BottomNav.MY_CART)
    app.tap_bottom_tab(locators.BottomNav.PROFILE)
    app.tap_bottom_tab(locators.BottomNav.HOME)
    wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE, seconds=15)


def test_007_from_home_open_cupcake_detail_and_add_to_cart(driver):
    """
    User steps:
      1. Go to the Home tab.
      2. On the snack list, open the “Cupcake” item (card opens the snack detail).
      3. On the detail screen, tap “Add to cart”.
      4. Tap the **Back** control on the detail screen (toolbar), not only the device key.
      5. Confirm you are on the Home feed again (e.g. delivery banner visible).

    Expected: Add to cart works; Back returns to Home (cart contents are asserted in other tests).
    """
    go_to_home_tab(driver)
    add_snack_to_cart_from_list(driver, "Cupcake")
    tap_detail_screen_back(driver)
    wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE, seconds=15)


def test_008_home_feed_scroll_to_bottom_then_back_to_top(driver):
    """
    User steps:
      1. Go to the Home tab (delivery banner visible).
      2. Swipe the feed toward the bottom twice (two upward gestures on the list area).
      3. Swipe back toward the top twice (two downward gestures).
      4. Confirm the top of the home feed is visible again (delivery line and main section headers).

    Expected: Scroll down then up completes without error; header area of the feed is visible again.
    """
    go_to_home_tab(driver)
    scroll_home_feed_to_bottom_then_top(driver)
    verify_home_feed_main_sections(driver)
