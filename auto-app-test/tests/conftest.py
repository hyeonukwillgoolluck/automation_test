from __future__ import annotations

import os
import pathlib
import re
import time
from pathlib import Path
from typing import Generator, Optional

import pytest
from dotenv import load_dotenv

from appium_pom.config.app_config import TargetAppInfo
from appium_pom.config.server_env import resolve_server_config
from appium_pom.driver.driver_factory import create_driver
from appium_pom.utils.caps_loader import load_caps
from appium_pom.utils.logger import setup_logging


@pytest.fixture(scope="session", autouse=True)
def _env_setup() -> None:
    # Load .env from project root if exists
    root = pathlib.Path(__file__).resolve().parents[1]
    env_file = root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    setup_logging()


@pytest.fixture(scope="session")
def server_config():
    return resolve_server_config()


@pytest.fixture(scope="session")
def worker_index() -> int:
    wid = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    m = re.search(r"(\d+)$", wid)
    return int(m.group(1)) if m else 0


@pytest.fixture(scope="session")
def udid(worker_index) -> Optional[str]:
    target = os.getenv("TARGET_UDIDS")
    if target:
        arr = [x.strip() for x in target.split(",") if x.strip()]
        if arr:
            return arr[worker_index % len(arr)]
    # fallback single UDID
    return os.getenv("UDID") or None


@pytest.fixture(scope="session")
def capabilities(server_config, udid):
    caps = load_caps(server_config.caps_file, server_config.platform)
    if udid:
        caps["udid"] = udid
    return caps


@pytest.fixture(scope="session")
def app_info():
    return TargetAppInfo.load()


@pytest.fixture(scope="session")
def driver(server_config, capabilities) -> Generator:
    drv = create_driver(server_config.server_url, server_config.platform, capabilities)
    # Small grace period for app launch
    time.sleep(1)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture(scope="session")
def platform(server_config):
    return server_config.platform


# --- Failure diagnostics: screenshot on failure (and Allure attach if present) ---

def _sanitize_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)[:180]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or rep.passed:
        return
    # On failure, try to capture screenshot
    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if not driver:
        return
    try:
        image = driver.get_screenshot_as_png()
        root = Path(__file__).resolve().parents[1]
        out_dir = root / "reports" / "screenshots"
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = _sanitize_filename(item.nodeid) + ".png"
        with (out_dir / fname).open("wb") as f:
            f.write(image)
        try:
            import allure  # type: ignore

            allure.attach(image, name=f"screenshot: {item.name}", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
    except Exception:
        pass

    # Try to capture page source and attach
    try:
        src = driver.page_source
        try:
            import allure  # type: ignore

            allure.attach(src, name=f"pagesource: {item.name}", attachment_type=allure.attachment_type.XML)
        except Exception:
            # also write raw file for local debugging
            root = Path(__file__).resolve().parents[1]
            out_dir = root / "reports" / "pagesource"
            out_dir.mkdir(parents=True, exist_ok=True)
            fname = _sanitize_filename(item.nodeid) + ".xml"
            with (out_dir / fname).open("w", encoding="utf-8") as f:
                f.write(src)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    # Write allure environment.properties if ALLURE_DIR is provided
    allure_dir = os.getenv("ALLURE_DIR")
    if not allure_dir:
        return
    try:
        env_path = Path(allure_dir) / "environment.properties"
        env_path.parent.mkdir(parents=True, exist_ok=True)

        # Lazily import to avoid circulars
        server = resolve_server_config()
        caps = load_caps(server.caps_file, server.platform)
        lines = []
        put = lines.append
        put(f"server.env={server.name}")
        put(f"server.url={server.server_url}")
        put(f"platform={server.platform}")
        for key in [
            "deviceName",
            "udid",
            "platformVersion",
            "appPackage",
            "appActivity",
            "bundleId",
        ]:
            if caps.get(key) is not None:
                put(f"cap.{key}={caps.get(key)}")
        with env_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception:
        # non-fatal
        pass
