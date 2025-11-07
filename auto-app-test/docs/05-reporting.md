# Reporting

Allure 및 JUnit 리포팅을 활성화하는 방법을 설명합니다.

## Allure 결과 생성
1) 플러그인 설치
```
uv sync --extra report
```
2) 실행 시 결과 디렉토리 지정
```
ALLURE=1 ALLURE_DIR=allure-results ./run_tests.sh -m smoke
```
3) (선택) Allure HTML 생성
```
# Allure CLI가 설치되어 있어야 함 (brew install allure 등)
ALLURE=1 ALLURE_GENERATE=1 ALLURE_DIR=allure-results ALLURE_HTML_DIR=allure-report ./run_tests.sh
```

## JUnit XML
```
JUNIT=1 JUNIT_XML=reports/junit/report.xml ./run_tests.sh
```

## 실패 산출물
- 스크린샷: `reports/screenshots/*.png`
- 페이지소스: Allure 첨부 또는 `reports/pagesource/*.xml`

## Allure 환경 메타
- 테스트 세션 시작 시 `ALLURE_DIR/environment.properties` 자동 생성
- 포함 값 예시: `server.env`, `server.url`, `platform`, 캡빌리티 주요 키(`deviceName`, `udid`, `platformVersion`, `bundleId` 등)

