from __future__ import annotations

from appium.webdriver.webdriver import WebDriver


class ModulePrecondition:
    """Example preconditions: ensure app is on home screen, logged-out state, etc."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def ensure_cold_start(self, bundle_or_package: str) -> None:
        try:
            self.driver.terminate_app(bundle_or_package)
        except Exception:
            pass
        self.driver.activate_app(bundle_or_package)

