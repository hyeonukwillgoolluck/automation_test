from __future__ import annotations

from typing import Any, Dict, Tuple

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, platform: str):
        self.driver = driver
        self.platform = platform.lower()

    def wait_visible(self, locator: Locator, timeout: int = 20):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find(self, locator: Locator):
        return self.driver.find_element(*locator)

    def tap(self, locator: Locator):
        self.wait_visible(locator)
        self.find(locator).click()

    def type(self, locator: Locator, text: str, clear: bool = True):
        self.wait_visible(locator)
        el = self.find(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    @staticmethod
    def by_accessibility_id(value: str) -> Locator:
        return (AppiumBy.ACCESSIBILITY_ID, value)

    @staticmethod
    def by_id(value: str) -> Locator:
        return (AppiumBy.ID, value)

    @staticmethod
    def by_xpath(value: str) -> Locator:
        return (AppiumBy.XPATH, value)

