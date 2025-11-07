# CI / Jenkins

Jenkins에서 로컬 및 BrowserStack 실행을 구성하는 방법을 설명합니다.

## 공통 환경변수
- `SERVER_ENV` (예: `local_aos`, `bs_ios`)
- `APPIUM_SERVER_URL` (로컬)
- `ANDROID_APP` / `IOS_APP`
- `UDID`, `DEVICE_NAME`, `PLATFORM_VERSION`
- `DEVICE_COUNT`, `TARGET_UDIDS`
- (BS) `BS_USERNAME`, `BS_ACCESS_KEY`, `BS_PROJECT`, `BS_BUILD`, `BS_SESSION_NAME`, `BS_LOCAL`
- (리포트) `ALLURE`, `ALLURE_DIR`, `ALLURE_GENERATE`, `ALLURE_HTML_DIR`, `JUNIT`, `JUNIT_XML`

## 파이프라인 스니펫 (로컬)
```
#!/bin/bash
set -e
cd auto-app-test
uv sync
chmod +x run_tests.sh
SERVER_ENV=${SERVER_ENV:-local_aos} \
DEVICE_COUNT=${DEVICE_COUNT:-1} \
ALLURE=1 ALLURE_DIR=allure-results \
JUNIT=1 JUNIT_XML=reports/junit/report.xml \
./run_tests.sh "${TEST_TARGET:-tests}" -m "${MARKS:-smoke}"
```

## 파이프라인 스니펫 (BrowserStack)
```
#!/bin/bash
set -e
cd auto-app-test
uv sync
chmod +x run_tests.sh
export SERVER_ENV=${SERVER_ENV:-bs_aos}
export DEVICE_COUNT=${DEVICE_COUNT:-2}
export BS_USERNAME BS_ACCESS_KEY
ALLURE=1 ALLURE_DIR=allure-results \
./run_tests.sh "${TEST_TARGET:-tests}" -m "${MARKS:-smoke}"
```

## 산출물 업로드
- JUnit XML: Jenkins JUnit 플러그인으로 테스트 리포트 게시
- Allure: Allure 플러그인을 통해 결과 디렉토리 수집(또는 HTML 아티팩트 업로드)

