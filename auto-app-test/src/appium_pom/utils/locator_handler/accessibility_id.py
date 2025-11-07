from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy


def acc_id(value: str):
    return (AppiumBy.ACCESSIBILITY_ID, value)

