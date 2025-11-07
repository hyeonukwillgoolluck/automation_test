import pytest

from appium_pom.pages.example.home_page import HomePage


@pytest.mark.smoke
def test_smoke_session_starts(driver, platform):
    # Basic sanity that a session has started and appium reports platform
    caps = driver.capabilities or {}
    assert "platformName" in caps
    # Optional: log current activity/bundle
    if platform.lower() == "android":
        _ = getattr(driver, "current_activity", None)
    else:
        _ = caps.get("bundleId")


@pytest.mark.smoke
@pytest.mark.android
def test_home_page_placeholder_android(driver, platform):
    if platform.lower() != "android":
        pytest.skip("Android only")
    page = HomePage(driver, platform)
    # Placeholder: won't fail if locators don't exist; this is a template
    # Use try/except to avoid hard failure on template projects
    try:
        page.assert_loaded()
    except Exception:
        pytest.skip("Replace locators to enable this assertion on your app")


@pytest.mark.smoke
@pytest.mark.ios
def test_home_page_placeholder_ios(driver, platform):
    if platform.lower() != "ios":
        pytest.skip("iOS only")
    page = HomePage(driver, platform)
    try:
        page.assert_loaded()
    except Exception:
        pytest.skip("Replace locators to enable this assertion on your app")

