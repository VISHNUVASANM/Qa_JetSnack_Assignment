"""
================================================================================
PROFILE TAB – automated tests (test_001, …)
================================================================================
Preconditions (manual / environment):
  • Appium server is running; one Android device or emulator is connected.
  • JetSnack opens once for this file; tests run in one continuous app session (no relaunch between tests).

How to run only this file:
  python -m pytest tests/test_profile.py -v
================================================================================
"""

from assist.helpers import go_to_profile_tab_and_wait_placeholder


def test_001_open_profile_tab_and_verify_placeholder_content(driver):
    """
    User steps:
      1. Open the Home tab, then open the Profile tab on the bottom bar.
      2. On Profile, wait for the placeholder content (either a “work in progress” style message
         or the “Grab a beverage” line).

    Expected: Profile shows the expected placeholder, not a blank broken screen.
    """
    go_to_profile_tab_and_wait_placeholder(driver)
