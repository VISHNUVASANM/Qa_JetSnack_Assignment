"""Small wait helpers so tests stay readable."""

import time

import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def wait_visible(driver, by, value, seconds=15):
    return WebDriverWait(driver, seconds).until(ec.presence_of_element_located((by, value)))


def wait_clickable(driver, by, value, seconds=15):
    return WebDriverWait(driver, seconds).until(ec.element_to_be_clickable((by, value)))


def tap_element_center(driver, element):
    """Tap the middle of an element (for Compose nodes that report clickable=false)."""
    try:
        ActionChains(driver).move_to_element(element).click().perform()
    except Exception:
        rect = element.rect
        x = int(rect["x"] + rect["width"] / 2)
        y = int(rect["y"] + rect["height"] / 2)
        driver.execute_script("mobile: clickGesture", {"x": x, "y": y})


def by_uiautomator_text_contains(fragment: str) -> tuple:
    """Find by visible text (partial match). Good for many Android / Compose screens."""
    expr = f'new UiSelector().textContains("{fragment}")'
    return (AppiumBy.ANDROID_UIAUTOMATOR, expr)


def scroll_text_into_view(driver, text: str):
    """Try this when an item is below the fold. Does not work on all Compose lists."""
    rule = (
        "new UiScrollable(new UiSelector().scrollable(true))"
        f'.scrollIntoView(new UiSelector().textContains("{text}"))'
    )
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, rule)


def scroll_home_feed_to_bottom_then_top(
    driver,
    *,
    swipes_toward_bottom=2,
    swipes_toward_top=2,
    pause_s=0.28,
    wait_after_for_delivery_line=True,
):
    """
    Swipe the main scrollable area toward the bottom, then back toward the top (Home or Search).

    Default: **two** gestures toward the bottom then **two** toward the top (override with
    ``swipes_toward_bottom`` / ``swipes_toward_top``). Uses ``mobile: swipeGesture`` (UiAutomator2)
    in a centered band; **up** reveals lower items; **down** moves back toward the top.
    If ``swipeGesture`` fails, tries ``scrollGesture``.

    When ``wait_after_for_delivery_line`` is True (default), waits for the Home delivery banner
    (use on Home). Set False on Search and wait for search UI yourself.
    """
    from assist import locators

    size = driver.get_window_size()
    w, h = size["width"], size["height"]
    box = {
        "left": int(w * 0.08),
        "top": int(h * 0.22),
        "width": int(w * 0.84),
        "height": int(h * 0.52),
        "percent": 0.68,
    }

    def _gesture(name: str, direction: str):
        driver.execute_script(f"mobile: {name}Gesture", {**box, "direction": direction})

    def swipe_or_scroll(direction: str):
        for name in ("swipe", "scroll"):
            try:
                _gesture(name, direction)
                return
            except Exception:
                continue

    for _ in range(swipes_toward_bottom):
        swipe_or_scroll("up")
        time.sleep(pause_s)

    for _ in range(swipes_toward_top):
        swipe_or_scroll("down")
        time.sleep(pause_s)

    if wait_after_for_delivery_line:
        wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE, seconds=20)


def click_snack_card_by_title(driver, title: str, seconds=15):
    """Clicks the snack row (clickable ancestor), not only the title TextView."""
    from assist.locators import SnackCard  # local import avoids heavy cycles at import time

    by, val = SnackCard.title_xpath(title)
    wait_clickable(driver, by, val, seconds=seconds).click()


def type_query_on_search(driver, query: str):
    """
    Open SEARCH, focus the field (tap hint if needed), type ``query``, then wait **3 seconds**
    so results can settle before later steps.
    Returns ``JetsnackApp`` for further navigation. Fails if the field cannot be used.
    """
    from assist import locators

    app = go_to_search_tab(driver)

    try:
        field = wait_visible(driver, *locators.SearchScreen.SEARCH_FIELD, seconds=5)
    except TimeoutException:
        try:
            wait_clickable(driver, *locators.SearchScreen.SEARCH_HINT, seconds=8).click()
            field = wait_visible(driver, *locators.SearchScreen.SEARCH_FIELD, seconds=8)
        except TimeoutException:
            pytest.fail("Could not focus the search field (no EditText, hint tap did not help).")

    try:
        field.clear()
    except Exception:
        pass
    field.send_keys(query)
    time.sleep(3)
    return app


def type_cup_on_search(driver):
    """
    Open SEARCH, type ``cup`` (see ``type_query_on_search``). Returns ``JetsnackApp``.

    Reuse from search tests and cart tests that build the cart via search results.
    """
    return type_query_on_search(driver, "cup")


def search_cup_and_require_cupcake_results(driver, results_wait=15):
    """
    Reusable: SEARCH + type ``cup`` + assert Cupcake appears in results.
    Returns ``JetsnackApp`` for further steps (open snack, MY CART, etc.).
    """
    app = type_cup_on_search(driver)
    try:
        WebDriverWait(driver, results_wait).until(lambda d: "cupcake" in d.page_source.lower())
    except TimeoutException:
        pytest.fail(
            f"Expected 'Cupcake' in search results after typing 'cup', but it did not appear "
            f"within {results_wait}s."
        )
    return app


def go_to_home_tab(driver, wait_for_delivery_banner=True, seconds=15):
    """Tap HOME; optionally wait until the delivery line is visible. Returns ``JetsnackApp``."""
    from assist import locators
    from assist.pages.jetsnack_app import JetsnackApp

    app = JetsnackApp(driver)
    app.tap_bottom_tab(locators.BottomNav.HOME)
    if wait_for_delivery_banner:
        wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE, seconds=seconds)
    return app


def go_to_search_tab(driver):
    """Tap HOME then SEARCH. Returns ``JetsnackApp``."""
    from assist import locators
    from assist.pages.jetsnack_app import JetsnackApp

    app = JetsnackApp(driver)
    app.tap_bottom_tab(locators.BottomNav.HOME)
    app.tap_bottom_tab(locators.BottomNav.SEARCH)
    return app


def wait_search_field_or_hint_visible(driver, field_seconds=6, hint_seconds=12):
    """Wait until the search ``EditText`` or the “Search Jetsnack” hint is present."""
    from assist import locators

    try:
        wait_visible(driver, *locators.SearchScreen.SEARCH_FIELD, seconds=field_seconds)
    except TimeoutException:
        wait_visible(driver, *locators.SearchScreen.SEARCH_HINT, seconds=hint_seconds)


def click_snack_card_by_title_with_scroll_fallback(driver, title: str, first_try_seconds=8):
    """
    Tap snack row by title; if not found in time, scroll then tap again.
    Reuse on HOME or SEARCH snack lists.
    """
    try:
        click_snack_card_by_title(driver, title, seconds=first_try_seconds)
    except TimeoutException:
        scroll_text_into_view(driver, title)
        click_snack_card_by_title(driver, title)


def tap_add_to_cart_on_detail_screen(driver):
    """On snack detail, tap the Add to cart control."""
    from assist import locators

    wait_clickable(driver, *locators.Detail.ADD_TO_CART).click()


def tap_detail_screen_back(driver, seconds=10):
    """
    Leave snack detail via the toolbar **Back** control (Compose View + content-desc Back;
    center-tap when clickable=false). Falls back to Android BACK if not found.
    """
    from assist import locators
    from assist.pages.jetsnack_app import JetsnackApp

    for by, val in (locators.Detail.BACK_VIEW, locators.Detail.BACK):
        try:
            el = WebDriverWait(driver, seconds).until(ec.presence_of_element_located((by, val)))
            tap_element_center(driver, el)
            return
        except Exception:
            continue
    JetsnackApp(driver).tap_android_back()


def open_my_cart_tab(app):
    """From ``JetsnackApp``, open the MY CART bottom tab."""
    from assist import locators

    app.tap_bottom_tab(locators.BottomNav.MY_CART)


def wait_page_source_contains(driver, text: str, seconds=15, ignore_case=True):
    """Wait until ``page_source`` contains ``text`` (default: case-insensitive)."""
    needle = text.lower() if ignore_case else text

    def _ok(d):
        src = d.page_source
        return needle in (src.lower() if ignore_case else src)

    WebDriverWait(driver, seconds).until(_ok)


def assert_cart_shows_text(driver, app, text: str, seconds=15):
    """Open MY CART and wait until ``text`` appears in the page source."""
    open_my_cart_tab(app)
    wait_page_source_contains(driver, text, seconds=seconds)


def verify_home_feed_main_sections(driver):
    """Wait for delivery line + the three main section headers on the home feed."""
    from assist import locators

    wait_visible(driver, *locators.HomeHeader.DELIVERY_LINE)
    wait_visible(driver, *locators.HomeSection.ANDROID_PICKS)
    wait_visible(driver, *locators.HomeSection.POPULAR)
    wait_visible(driver, *locators.HomeSection.WFH)


def add_snack_to_cart_from_list(driver, title: str, use_scroll_fallback=True):
    """
    From HOME or SEARCH list: open snack by title and tap Add to cart on detail.
    Does not open MY CART.
    """
    if use_scroll_fallback:
        click_snack_card_by_title_with_scroll_fallback(driver, title)
    else:
        click_snack_card_by_title(driver, title)
    tap_add_to_cart_on_detail_screen(driver)


def add_cupcake_via_search_and_assert_in_cart(
    driver,
    cart_text="cupcake",
    results_wait=15,
    cart_wait=15,
    *,
    tap_toolbar_back_after_add=False,
    assert_in_cart=True,
):
    """
    Full reusable flow: SEARCH + ``cup`` + require Cupcake → open Cupcake → Add to cart.
    If ``assert_in_cart`` (default True): open MY CART and assert ``cart_text`` in the page.
    If ``tap_toolbar_back_after_add`` is True, taps the snack detail toolbar **Back** (same as home tests)
    after add-to-cart; use with ``assert_in_cart=False`` when the cart UI is not reliable (e.g. search tests).
    Returns ``JetsnackApp``.
    """
    app = search_cup_and_require_cupcake_results(driver, results_wait=results_wait)
    click_snack_card_by_title_with_scroll_fallback(driver, "Cupcake")
    tap_add_to_cart_on_detail_screen(driver)
    if tap_toolbar_back_after_add:
        tap_detail_screen_back(driver)
        time.sleep(0.5)
        try:
            wait_search_field_or_hint_visible(driver, field_seconds=8, hint_seconds=14)
        except TimeoutException:
            # Back may land on Home or another screen without the search chrome yet.
            go_to_search_tab(driver)
            wait_search_field_or_hint_visible(driver, field_seconds=8, hint_seconds=14)
    if assert_in_cart:
        assert_cart_shows_text(driver, app, cart_text, seconds=cart_wait)
    return app


def go_to_profile_tab_and_wait_placeholder(driver):
    """HOME → PROFILE; wait for WIP or “Grab a beverage” placeholder. Returns ``JetsnackApp``."""
    from assist import locators
    from assist.pages.jetsnack_app import JetsnackApp

    app = JetsnackApp(driver)
    app.tap_bottom_tab(locators.BottomNav.HOME)
    app.tap_bottom_tab(locators.BottomNav.PROFILE)
    try:
        wait_visible(driver, *locators.ProfileScreen.WIP, seconds=10)
    except TimeoutException:
        wait_visible(driver, *locators.ProfileScreen.GRAB_BEVERAGE, seconds=10)
    return app


def _tap_filter_sheet_close(driver):
    """Tap the filter sheet close control (not Android BACK)."""
    from assist import locators

    for by, val in (locators.FilterSheet.CLOSE, locators.FilterSheet.CLOSE_BY_DESC):
        try:
            el = WebDriverWait(driver, 5).until(ec.presence_of_element_located((by, val)))
            tap_element_center(driver, el)
            return
        except Exception:
            continue

    # Compose close icon: Inspector often shows android.widget.Button with clickable=false.
    by, val = locators.FilterSheet.CLOSE_BUTTON_COMPOSE
    try:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((by, val)))
    except Exception as ex:
        pytest.fail(f"Could not find filter sheet close button: {ex}")

    candidates = driver.find_elements(by, val)
    if not candidates:
        pytest.fail("Filter sheet close: no android.widget.Button matches after sheet opened.")

    def score(el):
        r = el.rect
        return (r["y"], r["x"])  # topmost, then leftmost (close is top-start)

    # Prefer a small leading-edge control (Material close icon), not full-width sheet actions.
    iconish = [e for e in candidates if 40 <= e.rect["width"] <= 220 and e.rect["x"] < 400]
    pool = iconish if iconish else candidates
    best = min(pool, key=score)
    tap_element_center(driver, best)


def open_filters_wait_for_sheet_then_close(driver, app):
    """
    On HOME: tap Filters, wait for filter sheet content, tap sheet close, wait for Filters again.
    """
    from assist import locators

    app.tap(locators.HomeToolbar.FILTERS)
    WebDriverWait(driver, 10).until(
        lambda d: ("Reset" in d.page_source and "Price" in d.page_source)
        or ("Sort" in d.page_source)
    )
    _tap_filter_sheet_close(driver)
    wait_visible(driver, *locators.HomeToolbar.FILTERS, seconds=10)


def clear_cart_via_ui(driver, max_rounds=30):
    """
    Open MY CART and remove every line item using the “Remove item” control (Compose View;
    content-desc match), tapping the control center when clickable=false.

    Designed for `tests/test_mycart.py` → `test_001_clear_cart_via_remove_item` (not conftest),
    because the cart screen is not fully reliable for global hooks.
    """
    from assist import locators
    from assist.pages.jetsnack_app import JetsnackApp

    try:
        app = JetsnackApp(driver)
        app.tap_bottom_tab(locators.BottomNav.MY_CART)
        time.sleep(0.45)
    except Exception:
        return

    remove_locators = (
        locators.Cart.REMOVE_ITEM_VIEW,
        locators.Cart.REMOVE_ITEM_DESC,
        locators.Cart.REMOVE_ITEM_A11Y,
        locators.Cart.REMOVE_ITEM_A11Y_ALT,
        locators.Cart.REMOVE_ITEM_UI,
    )

    for _ in range(max_rounds):
        tapped = False
        for loc in remove_locators:
            try:
                by, val = loc
                candidates = [e for e in driver.find_elements(by, val) if e.is_displayed()]
                if not candidates:
                    continue
                tap_element_center(driver, candidates[0])
                tapped = True
                time.sleep(0.45)
                break
            except Exception:
                continue
        if not tapped:
            break
