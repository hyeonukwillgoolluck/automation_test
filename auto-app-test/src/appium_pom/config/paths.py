from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    # src/appium_pom/config -> src -> project
    return Path(__file__).resolve().parents[3]


ROOT = project_root()
SRC = ROOT / "src"
RES = ROOT / "res"
CONF = RES / "config"
APPS = ROOT / "apps"

