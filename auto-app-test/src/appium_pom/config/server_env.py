from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

from .paths import CONF


ServerEnv = Literal["local_aos", "local_ios", "bs_aos", "bs_ios"]


@dataclass
class ServerConfig:
    name: ServerEnv
    server_url: str
    caps_file: str
    platform: Literal["Android", "iOS"]


def resolve_server_config() -> ServerConfig:
    env: ServerEnv = os.getenv("SERVER_ENV", "local_aos")  # type: ignore[assignment]

    # Prefer explicit URL if provided
    explicit_url = os.getenv("APPIUM_SERVER_URL")

    if env == "local_aos":
        return ServerConfig(
            name=env,
            server_url=explicit_url or "http://127.0.0.1:4723",
            caps_file=str((CONF / "conf_local_aos.json").resolve()),
            platform="Android",
        )
    if env == "local_ios":
        return ServerConfig(
            name=env,
            server_url=explicit_url or "http://127.0.0.1:4723",
            caps_file=str((CONF / "conf_local_ios.json").resolve()),
            platform="iOS",
        )

    if env == "bs_aos":
        url = explicit_url or _browserstack_hub_url()
        return ServerConfig(
            name=env,
            server_url=url,
            caps_file=str((CONF / "conf_bs_aos.json").resolve()),
            platform="Android",
        )
    if env == "bs_ios":
        url = explicit_url or _browserstack_hub_url()
        return ServerConfig(
            name=env,
            server_url=url,
            caps_file=str((CONF / "conf_bs_ios.json").resolve()),
            platform="iOS",
        )

    # Fallback to Android local
    return ServerConfig(
        name="local_aos",
        server_url=explicit_url or "http://127.0.0.1:4723",
        caps_file=str((CONF / "conf_local_aos.json").resolve()),
        platform="Android",
    )


def _browserstack_hub_url() -> str:
    user = os.getenv("BS_USERNAME", "")
    key = os.getenv("BS_ACCESS_KEY", "")
    if user and key:
        return f"https://{user}:{key}@hub-cloud.browserstack.com/wd/hub"
    # Without creds, return public hub (will fail at runtime if used)
    return "https://hub-cloud.browserstack.com/wd/hub"

