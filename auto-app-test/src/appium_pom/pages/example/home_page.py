from __future__ import annotations

from typing import Dict

from appium_pom.pages.base_page import BasePage, Locator


class HomePage(BasePage):
    """Example page object with platform-specific locators in one class.

    Replace identifiers to match your app. Use accessibility IDs where possible
    for cross-platform reuse.
    """

    LOCATORS: Dict[str, Dict[str, Locator]] = {
        "android": {
            "welcome_text": BasePage.by_accessibility_id("welcome"),
            "get_started_button": BasePage.by_accessibility_id("get_started"),
        },
        "ios": {
            "welcome_text": BasePage.by_accessibility_id("welcome"),
            "get_started_button": BasePage.by_accessibility_id("get_started"),
        },
    }

    def _l(self, name: str) -> Locator:
        return self.LOCATORS[self.platform][name]

    def assert_loaded(self) -> None:
        self.wait_visible(self._l("welcome_text"))

    def tap_get_started(self) -> None:
        self.tap(self._l("get_started_button"))

