# From Appium page source / Inspector. Change here if the app build changes.

from appium.webdriver.common.appiumby import AppiumBy


class BottomNav:
    HOME = (AppiumBy.ACCESSIBILITY_ID, "HOME")
    SEARCH = (AppiumBy.ACCESSIBILITY_ID, "SEARCH")
    MY_CART = (AppiumBy.ACCESSIBILITY_ID, "MY CART")
    PROFILE = (AppiumBy.ACCESSIBILITY_ID, "PROFILE")


class HomeHeader:
    SELECT_DELIVERY_ADDRESS = (AppiumBy.ACCESSIBILITY_ID, "Select delivery address")
    DELIVERY_LINE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Delivery to")',
    )


class HomeToolbar:
    FILTERS = (AppiumBy.ACCESSIBILITY_ID, "Filters")


class FilterChips:
    ORGANIC = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Organic")')
    GLUTEN_FREE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Gluten-free")')
    DAIRY_FREE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Dairy-free")')
    SWEET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sweet")')


class HomeSection:
    ANDROID_PICKS = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Android")',
    )
    POPULAR = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Popular on Jetsnack")',
    )
    WFH = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("WFH favourites")',
    )


class SnackCard:
    """Snack title is a TextView; the clickable row is an ancestor (see Inspector hierarchy)."""

    @staticmethod
    def title_xpath(title: str) -> tuple:
        safe = title.replace("'", "\\'")
        return (
            AppiumBy.XPATH,
            f"//android.widget.TextView[@text=\"{safe}\"]/ancestor::*[@clickable='true'][1]",
        )


class Detail:
    ADD_TO_CART = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textMatches("(?i).*add.*cart.*")',
    )
    # Snack detail top bar: Compose View, content-desc "Back", often clickable=false.
    BACK_VIEW = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").description("Back")',
    )
    BACK = (AppiumBy.ACCESSIBILITY_ID, "Back")


class SearchScreen:
    # JetSnack search placeholder (from app strings).
    SEARCH_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText")',
    )
    SEARCH_HINT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Search Jetsnack")',
    )


class ProfileScreen:
    WIP = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("work in progress")',
    )
    GRAB_BEVERAGE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Grab a beverage")',
    )


class FilterSheet:
    """Opened after tapping Filters (filter bottom sheet)."""
    RESET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reset")')
    PRICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Price")')
    # Sheet header close (Compose IconButton): often a11y "Close"; hierarchy may show clickable=false.
    CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close")
    CLOSE_BY_DESC = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Close")',
    )
    CLOSE_BUTTON_COMPOSE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.Button").packageName("com.example.jetsnack")'
        ".clickable(false).enabled(true)",
    )


class Cart:
    """MY CART line-item actions (JetSnack strings vary by casing)."""
    # Inspector: android.view.View, content-desc "Remove item", often clickable=false — tap center in helpers.
    REMOVE_ITEM_VIEW = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").description("Remove item")',
    )
    REMOVE_ITEM_DESC = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Remove item")',
    )
    REMOVE_ITEM_UI = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textMatches("(?i).*remove.*item.*")',
    )
    REMOVE_ITEM_A11Y = (AppiumBy.ACCESSIBILITY_ID, "Remove item")
    REMOVE_ITEM_A11Y_ALT = (AppiumBy.ACCESSIBILITY_ID, "Remove Item")
