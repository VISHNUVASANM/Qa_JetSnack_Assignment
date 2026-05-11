from assist.helpers import wait_clickable


class JetsnackApp:
    """Navigation + common taps from Inspector hierarchy."""

    def __init__(self, driver):
        self.driver = driver

    def tap(self, locator: tuple):
        by, value = locator
        wait_clickable(self.driver, by, value).click()

    def tap_bottom_tab(self, locator: tuple):
        self.tap(locator)

    def tap_android_back(self):
        self.driver.press_keycode(4)  # KEYCODE_BACK
