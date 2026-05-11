# QA test cases — JetSnack (`com.example.jetsnack`)

This document lists **user steps** and **expected results** for each automated test in `tests/`. Wording matches the docstrings in the Python test modules so you can compare automation to intent side by side.

## Known limitations (JetSnack sample build)

Read this before the test case sections. In this app build, the following areas are **not implemented or not fully functional**; automated tests still cover what the UI exposes (taps, navigation, visibility), not end-to-end commerce flows.

1. **Home — delivery address:** Choosing a delivery address and updating address details are **not functional** (e.g. “Select delivery address” does not lead to a working address flow).
2. **Add to cart:** The **add to cart** behaviour is **not functional** as a real cart flow (controls may appear; persistence and cart reliability are limited in this build).
3. **Profile:** The **Profile** area is **not fully developed** (placeholder / work-in-progress content only).
4. **Cart / checkout:** **Cart checkout** is **not functional** (no complete purchase path).
5. **Filters and categories (Home / Search):** **Filter** and **category** behaviour on the Home and Search experiences is **not functional** as a real merchandising flow .

**Environment:** see **doc/SETUP.md** (Appium, device, APK path in **assist/config.py**).

**Run automated tests**

```bash
python -m pytest tests/<file>.py -v
```

**Priority legend**

Use **H**, **M**, and **L** so critical paths are not all lumped together; counts below follow this scheme.


| Tag   | Meaning                                                                                                                                                |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **H** | **High** — Smoke and core journeys (wrong build, Home/Search entry, primary navigation).                                                               |
| **M** | **Medium** — Regression and secondary flows (filters, detail/add-to-cart tap, search results, scroll stress, cart best-effort).                        |
| **L** | **Low** — Lower product value in this build, gesture-only checks, or areas called out under **Known limitations** (e.g. address, Profile placeholder). |


**Coverage snapshot:** Home **H H L M L H M M** · Search **L H M M** · My Cart **M** · Profile **L** (mixed **H** / **M** / **L** across the suite).

---

## `tests/test_home.py`

### **H** — `test_001_verify_app_package_and_open_home_tab`

**User steps:**

1. After the app opens, confirm the running app is JetSnack (package matches the project config).
2. Open the Home tab on the bottom navigation.
3. Wait until the delivery banner (“Delivery to …”) is visible on the feed.

**Expected:** Correct app; Home feed is shown with the delivery line.

---

### **H** — `test_002_verify_delivery_banner_and_section_headers_on_feed`

**User steps:**

1. Go to the Home tab.
2. On the feed, read the delivery banner and the main section titles (e.g. Android’s picks, Popular, WFH).

**Expected:** Delivery line and the expected section headers are all visible.

---

### **L** — `test_003_tap_select_delivery_address_stays_on_home`

**User steps:**

1. Go to the Home tab.
2. Tap “Select delivery address” on the delivery banner.
3. Stay on Home: in this app build, no separate address screen is expected.

**Expected:** After the tap, the delivery line and a feed section (e.g. Android’s picks) are still visible.

---

### **M** — `test_004_tap_filters_opens_filter_sheet_then_close`

**User steps:**

1. Go to the Home tab.
2. Tap “Filters” on the toolbar.
3. Wait until the filter sheet shows (e.g. Reset / Price or Sort).
4. Close the sheet using the close control on the sheet (not the device Back key).
5. Confirm the “Filters” control on Home is visible again.

**Expected:** Sheet opens and closes cleanly; you return to the Home feed with Filters available.

---

### **L** — `test_005_toggle_diet_filter_chips_on_home`

**User steps:**

1. Go to the Home tab.
2. Tap the “Organic” diet chip, then “Gluten-free”.
3. Tap “Organic” again, then “Gluten-free” again (toggle each twice).

**Expected:** App remains stable; no crash.

---

### **H** — `test_006_visit_other_bottom_tabs_then_return_home_feed_still_visible`

**User steps:**

1. Start on Home and wait until the delivery banner is visible.
2. Use the bottom bar: open Search, then My Cart, then Profile.
3. Open Home again.
4. Wait until the delivery banner appears on Home.

**Expected:** Home feed still shows after round-trip navigation.

---

### **M** — `test_007_from_home_open_cupcake_detail_and_add_to_cart`

**User steps:**

1. Go to the Home tab.
2. On the snack list, open the “Cupcake” item (card opens the snack detail).
3. On the detail screen, tap “Add to cart”.
4. Tap the **Back** control on the detail toolbar (content-desc “Back”).
5. Confirm the Home feed is visible again (e.g. delivery banner).

**Expected:** Snack detail opens; **Add to cart** is tapped; **Back** returns to Home with the feed visible (cart persistence is not verified in this build; see **Known limitations**).

---

### **M** — `test_008_home_feed_scroll_to_bottom_then_back_to_top`

**User steps:**

1. Go to the Home tab (delivery banner visible).
2. Scroll the home feed toward the bottom **twice** (two vertical gestures).
3. Scroll back toward the top **twice** (two vertical gestures).
4. Confirm the delivery line and main section headers (Android’s picks, Popular, WFH) are visible again.

**Expected:** No crash; after scrolling down and up, the top of the feed is reachable and visible.

---

## `tests/test_search.py`

### **L** — `test_001_search_screen_scroll_feed_down_then_up_once`

**User steps:**

1. Open the Search tab and wait for the search field or “Search Jetsnack” hint.
2. Scroll the search/results area **down** once then **up** once (same gesture helper as Home `test_008`, one cycle each).
3. Confirm the search field or hint is still visible.

**Expected:** Scroll completes; Search UI remains usable.

---

### **H** — `test_002_open_search_tab_and_verify_search_ui_visible`

**User steps:**

1. From a stable start on Home, open the Search tab on the bottom bar.
2. On Search, look for a real search field or the “Search Jetsnack” hint so you know search is ready.

**Expected:** Search screen shows a recognizable search control (field or hint).

---

### **M** — `test_003_search_cup_then_open_cupcake_and_add_to_cart`

**User steps:**

1. Open the Search tab.
2. Type “cup” in the search field.
3. Confirm “Cupcake” appears in the results.
4. Open the Cupcake row to its detail screen.
5. Tap “Add to cart”.
6. Tap the detail toolbar **Back** (same pattern as home snack detail) so Search results are visible again.

**Expected:** Search → detail → add to cart → back to search completes. MY CART is not checked here (cart screen not fully reliable). Optional UI emptying: **tests/test_mycart.py** → **test_001_clear_cart_via_remove_item**.

---

### **M** — `test_004_search_chi_shows_chips_and_apple_chips_visible`

**User steps:**

1. Open the Search tab and type “chi”.
2. Wait until the results show chips-related copy (e.g. “Chips” and “Apple chips” / “apple chip” in the page).

**Expected:** Search results include chips items; both **chips** and **apple chip** substrings appear (case-insensitive check on page source).

---

## `tests/test_mycart.py`

This module contains **only** the clear-cart test (add-to-cart assertions were removed; cart UI not fully reliable).

### **M** — `test_001_clear_cart_via_remove_item`

**User steps:**

1. Open My Cart.
2. Tap **Remove item** on each line until no more remove controls appear (best effort).

**Expected:** Run completes without error; cart UI may still be flaky in this build (clearing is not run from conftest).

---

## `tests/test_profile.py`

### **L** — `test_001_open_profile_tab_and_verify_placeholder_content`

**User steps:**

1. Open the Home tab, then open the Profile tab on the bottom bar.
2. On Profile, wait for the placeholder content (either a “work in progress” style message or the “Grab a beverage” line).

**Expected:** Profile shows the expected placeholder, not a blank broken screen.

---

## `tests/conftest.py` (driver only)

For each test **file** (module), pytest starts **one** Appium session: all tests in that file share the same driver (the app is not restarted between tests). The session ends in `finally` with `**driver.quit()`**.

**MY CART** is not modified in setup or teardown. Optional cart line removal via the UI is **tests/test_mycart.py** → **test_001_clear_cart_via_remove_item** only.

---

