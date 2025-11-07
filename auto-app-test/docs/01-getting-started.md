# Getting Started

이 문서는 템플릿을 빠르게 설치하고 첫 테스트를 실행하기 위한 최소 절차를 설명합니다.

## 준비물
- Python 3.9 이상
- uv 패키지 매니저 (https://docs.astral.sh/uv)
- Appium Server v2 (로컬 실행 시)
  - Node.js, Appium server, 플랫폼 드라이버(UiAutomator2, XCUITest)
- (선택) Allure CLI (HTML 리포트 생성 시)

## 설치
```
cd auto-app-test
uv sync            # 의존성 설치 (가상환경 자동 생성)
```

## 환경파일(.env)
```
cp .env.example .env
# APPIUM_SERVER_URL, SERVER_ENV, ANDROID_APP/IOS_APP, UDID/DEVICE_NAME 등 필요 값 채우기
```

## 실행 예시
- 로컬 Android:
```
SERVER_ENV=local_aos ANDROID_APP=./apps/app.apk ./run_tests.sh tests/suite_no1 -m smoke
```
- 로컬 iOS:
```
SERVER_ENV=local_ios IOS_APP=./apps/MyApp.app ./run_tests.sh tests/suite_no1 -m smoke
```
- BrowserStack:
```
export BS_USERNAME=xxx BS_ACCESS_KEY=yyy
SERVER_ENV=bs_aos DEVICE_COUNT=2 ./run_tests.sh -m smoke
```

## 드라이버 빠른 기동 CLI
```
uv run appium-pom-open --server-env local_aos --android-app ./apps/app.apk --duration 5
```
옵션: `--server-env`, `--udid`, `--android-app`, `--ios-app`, `--duration`

