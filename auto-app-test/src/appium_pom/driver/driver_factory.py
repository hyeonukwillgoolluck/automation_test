from __future__ import annotations

from typing import Any, Dict

from appium import webdriver

try:
    from appium.options.android import UiAutomator2Options
except Exception:  # pragma: no cover
    UiAutomator2Options = None  # type: ignore

try:
    from appium.options.ios import XCUITestOptions
except Exception:  # pragma: no cover
    XCUITestOptions = None  # type: ignore

from appium.options.common import AppiumOptions


def create_driver(server_url: str, platform: str, capabilities: Dict[str, Any]):
    platform_lower = platform.lower()
    if platform_lower == "android" and UiAutomator2Options is not None:
        options = UiAutomator2Options()
        options.load_capabilities(capabilities)
        return webdriver.Remote(server_url, options=options)
    if platform_lower == "ios" and XCUITestOptions is not None:
        options = XCUITestOptions()
        options.load_capabilities(capabilities)
        return webdriver.Remote(server_url, options=options)

    # Fallback generic options
    options = AppiumOptions()
    options.load_capabilities(capabilities)
    return webdriver.Remote(server_url, options=options)

