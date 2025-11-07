from __future__ import annotations

from appium.webdriver.webdriver import WebDriver


class ModuleScenario:
    """Higher-level business flows composed from page objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def sample_smoke_flow(self) -> None:
        # Placeholder for an end-to-end flow
        # e.g., launch -> accept permissions -> verify home -> logout
        pass

