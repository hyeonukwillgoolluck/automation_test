from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy


def xpath(value: str):
    return (AppiumBy.XPATH, value)

