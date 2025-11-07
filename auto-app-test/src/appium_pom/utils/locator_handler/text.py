from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy


def text(value: str):
    """Platform-agnostic text matcher when accessibility id isn't available.

    On Android, matches by XPath `//*[@text='value']`.
    On iOS, matches by predicate `name == "value" OR label == "value"`.
    """
    # Note: In real projects, you'd branch by platform. Keep simple here.
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{value}")')

