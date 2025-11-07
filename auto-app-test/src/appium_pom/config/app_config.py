from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .paths import CONF


@dataclass
class TargetAppInfo:
    app_name: str
    android: Dict[str, Any]
    ios: Dict[str, Any]
    project: Dict[str, Any]
    api_base: str
    cloud: Dict[str, Any]

    @staticmethod
    def load(path: Path | None = None) -> "TargetAppInfo":
        p = path or (CONF / "target_app_info.json")
        with p.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        return TargetAppInfo(
            app_name=raw.get("appName", ""),
            android=raw.get("android", {}),
            ios=raw.get("ios", {}),
            project=raw.get("project", {}),
            api_base=raw.get("apiBase", ""),
            cloud=raw.get("cloud", {}),
        )

