from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from appium_pom.config.app_config import TargetAppInfo
from appium_pom.config.paths import CONF
from appium_pom.utils.port_allocator import get_free_port


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_caps(caps_file: str, platform: str) -> Dict[str, Any]:
    common = _load_json(CONF / "common.json")
    specific = _load_json(Path(caps_file))
    merged = deep_merge(common, specific)

    # Fill from target app info if not explicitly provided
    app_info = TargetAppInfo.load()
    if platform.lower() == "android":
        merged.setdefault("appPackage", app_info.android.get("appPackage", ""))
        merged.setdefault("appActivity", app_info.android.get("appActivity", ""))
        merged.setdefault("appWaitActivity", app_info.android.get("appWaitActivity", ""))
        app_env = os.getenv("ANDROID_APP")
        if app_env:
            merged["app"] = app_env
    else:
        merged.setdefault("bundleId", app_info.ios.get("bundleId", ""))
        app_env = os.getenv("IOS_APP")
        if app_env:
            merged["app"] = app_env

    # Environment overrides
    if os.getenv("UDID"):
        merged["udid"] = os.getenv("UDID")
    if os.getenv("DEVICE_NAME"):
        merged["deviceName"] = os.getenv("DEVICE_NAME")
    if os.getenv("PLATFORM_VERSION"):
        merged["platformVersion"] = os.getenv("PLATFORM_VERSION")

    # Extra caps as JSON string
    extra_json = os.getenv("EXTRA_CAPS_JSON")
    if extra_json:
        try:
            merged = deep_merge(merged, json.loads(extra_json))
        except Exception:
            # Ignore malformed extra caps
            pass

    # BrowserStack tuning
    if "bstack:options" in merged:
        bstack = merged["bstack:options"]
        bstack.setdefault("projectName", os.getenv("BS_PROJECT") or app_info.cloud.get("browserstack", {}).get("projectName"))
        if os.getenv("BS_BUILD"):
            bstack["buildName"] = os.getenv("BS_BUILD")
        if os.getenv("BS_SESSION_NAME"):
            bstack["sessionName"] = os.getenv("BS_SESSION_NAME")
        if os.getenv("BS_LOCAL"):
            bstack["local"] = os.getenv("BS_LOCAL").lower() == "true"

    # Allocate ports for parallel if not given
    if platform.lower() == "android" and not merged.get("systemPort"):
        merged["systemPort"] = get_free_port()
    if platform.lower() == "ios" and not merged.get("wdaLocalPort"):
        merged["wdaLocalPort"] = get_free_port()

    return merged

