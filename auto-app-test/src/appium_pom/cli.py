from __future__ import annotations

import argparse
import os
import pathlib
import time

from dotenv import load_dotenv

from appium_pom.config.server_env import resolve_server_config
from appium_pom.driver.driver_factory import create_driver
from appium_pom.utils.caps_loader import load_caps
from appium_pom.utils.logger import setup_logging


def parse_args():
    p = argparse.ArgumentParser(description="Open an Appium session quickly (Android/iOS)")
    p.add_argument("--server-env", dest="server_env", default=os.getenv("SERVER_ENV", "local_aos"),
                   help="Server env: local_aos|local_ios|bs_aos|bs_ios (default: env SERVER_ENV)")
    p.add_argument("--duration", type=int, default=5, help="Keep session open for N seconds (default 5)")
    p.add_argument("--udid", default=os.getenv("UDID"), help="Override device UDID")
    p.add_argument("--android-app", dest="android_app", default=os.getenv("ANDROID_APP"))
    p.add_argument("--ios-app", dest="ios_app", default=os.getenv("IOS_APP"))
    return p.parse_args()


def main() -> int:
    # Load .env if present
    root = pathlib.Path(__file__).resolve().parents[3]
    env_file = root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    setup_logging()

    args = parse_args()
    os.environ["SERVER_ENV"] = args.server_env
    if args.android_app:
        os.environ["ANDROID_APP"] = args.android_app
    if args.ios_app:
        os.environ["IOS_APP"] = args.ios_app
    if args.udid:
        os.environ["UDID"] = args.udid

    server = resolve_server_config()
    caps = load_caps(server.caps_file, server.platform)
    if args.udid:
        caps["udid"] = args.udid

    print(f"Connecting to {server.server_url} | platform={server.platform}")
    drv = create_driver(server.server_url, server.platform, caps)
    try:
        caps_eff = drv.capabilities or {}
        print("Session started:")
        print(f"  sessionId: {getattr(drv, 'session_id', 'n/a')}")
        print(f"  platformName: {caps_eff.get('platformName')}")
        print(f"  deviceName: {caps_eff.get('deviceName')}")
        print(f"  udid: {caps_eff.get('udid')}")
        time.sleep(max(0, args.duration))
    finally:
        try:
            drv.quit()
        except Exception:
            pass
    print("Session closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

