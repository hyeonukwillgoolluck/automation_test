from __future__ import annotations

from appium.webdriver.webdriver import WebDriver


class ModuleCommon:
    """Reusable common actions across pages (e.g., kill app, relaunch, background)."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def background_app(self, seconds: int = 1) -> None:
        self.driver.background_app(seconds)

    def terminate_app(self, bundle_or_package: str) -> None:
        try:
            self.driver.terminate_app(bundle_or_package)
        except Exception:
            pass

    def activate_app(self, bundle_or_package: str) -> None:
        self.driver.activate_app(bundle_or_package)

