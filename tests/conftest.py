import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from assist import config

# When running the whole suite (`pytest` / `pytest tests/`), run modules in this order so the
# device flow matches: Home → Search → My Cart → Profile. (Default discovery is alphabetical.)
_MODULE_RUN_ORDER = {
    "test_home.py": 0,
    "test_search.py": 1,
    "test_mycart.py": 2,
    "test_profile.py": 3,
}


def pytest_collection_modifyitems(config, items):
    def sort_key(item):
        try:
            mod_name = item.path.name
        except AttributeError:
            mod_name = ""
        priority = _MODULE_RUN_ORDER.get(mod_name, 99)
        # Stable order within the same file (line number, then node id).
        lineno = getattr(item, "location", (None, 0, None))[1]
        return (priority, lineno, item.nodeid)

    items[:] = sorted(items, key=sort_key)


@pytest.fixture(scope="module")
def driver():
    """
    One Appium session per test **file** (module): all tests in that file share the same driver,
    so the app is not quit/relaunched between tests. The session ends after the last test in the file.
    """
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.udid = config.UDID
    opts.app = config.APK_PATH
    opts.app_package = config.APP_PACKAGE
    opts.app_activity = config.APP_ACTIVITY
    opts.automation_name = "UiAutomator2"
    opts.set_capability("appium:newCommandTimeout", 120)

    d = webdriver.Remote(config.APPIUM_SERVER_URL, options=opts)
    try:
        yield d
    finally:
        try:
            d.quit()
        except Exception:
            pass
