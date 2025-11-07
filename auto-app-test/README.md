# Appium Android/iOS UI 테스트 템플릿 (POM 기반)

PRD(루트 `README.md`) 내용을 반영한, 중복을 최소화하고 유지보수에 용이한 초기 프로젝트 구성입니다. Python + pytest + Appium 클라이언트를 사용하며, POM(Page Object Model)·캡빌리티 분리·로컬/BrowserStack 실행·병렬(pytest-xdist) 실행을 지원합니다.

## 구조 개요
- `src/appium_pom/`: 프레임워크 코드
  - `config/`: 경로/앱 정보/서버 환경 해석
  - `driver/driver_factory.py`: 플랫폼별 Appium 드라이버 생성
  - `utils/`: 캡빌리티 병합, 포트 할당, 로깅
  - `pages/`: POM 베이스 및 공통/예시 모듈
- `res/config/`: 캡빌리티 및 앱 메타 분리(JSON)
  - `common.json`: 공통 캡빌리티
  - `conf_local_{aos,ios}.json`: 로컬 디바이스/시뮬레이터
  - `conf_bs_{aos,ios}.json`: BrowserStack
  - `target_app_info.json`: 번들 ID/패키지 등 앱 메타
- `tests/`: 예시 스위트/테스트 + `conftest.py`로 드라이버/설정 관리
- `run_tests.sh`: 환경변수 기반 실행 래퍼 (uv/pytest 자동 선택)
- `jenkins-*`: 로컬/BrowserStack 파이프라인 템플릿

## 설치 (uv 권장)
- Python 3.9+ 환경
- Appium Server(v2) 및 플랫폼별 드라이버 설치(로컬 실행 시)
- uv 사용: `cd auto-app-test && uv sync` (자동 `.venv` 생성 및 의존성 설치)
- 직접 실행 시: `uv run pytest -V`로 확인 가능
 - Allure 리포팅을 사용하려면: `uv sync --extra report`

## 빠른 시작
1) `.env` 작성 (`.env.example` 복사):
```
cp .env.example .env
# 서버/앱/디바이스/BrowserStack 정보 채우기
```
2) 로컬 Android 실행 예시:
```
SERVER_ENV=local_aos ANDROID_APP=./apps/app.apk ./run_tests.sh tests/suite_no1 -m smoke
```
3) 로컬 iOS 실행 예시:
```
SERVER_ENV=local_ios IOS_APP=./apps/MyApp.app ./run_tests.sh tests/suite_no1 -m smoke
```
4) BrowserStack 실행 예시:
```
export BS_USERNAME=xxx BS_ACCESS_KEY=yyy
SERVER_ENV=bs_aos DEVICE_COUNT=2 ./run_tests.sh -m smoke
```

참고: `run_tests.sh`는 uv가 설치되어 있으면 자동으로 `uv run pytest`를 사용합니다. uv가 없다면 로컬 `pytest`로 폴백합니다.

## 환경 변수 (핵심)
- `SERVER_ENV`: `local_aos | local_ios | bs_aos | bs_ios`
- `APPIUM_SERVER_URL`: 기본 `http://127.0.0.1:4723` (BrowserStack 시 자동 허브 URL 사용)
- 앱 경로: `ANDROID_APP`, `IOS_APP`
- 디바이스: `UDID`, `DEVICE_NAME`, `PLATFORM_VERSION`
- BrowserStack: `BS_USERNAME`, `BS_ACCESS_KEY`, `BS_PROJECT`, `BS_BUILD`, `BS_SESSION_NAME`, `BS_LOCAL`
- 병렬: `DEVICE_COUNT` (pytest-xdist 워커 수)
- 추가 캡: `EXTRA_CAPS_JSON` (JSON 문자열로 병합)
 - 다중 디바이스: `TARGET_UDIDS`(콤마 분리)로 워커-디바이스 매핑
 - 리포트: `ALLURE=1`, `ALLURE_DIR=allure-results`, `ALLURE_GENERATE=1`, `ALLURE_HTML_DIR=allure-report`, `JUNIT=1`, `JUNIT_XML=reports/junit/report.xml`

## 캡빌리티 설계 (중복 최소화)
- `res/config/common.json`: 모든 환경 공통 값
- 개별 파일(`conf_local_aos.json` 등) + 공통을 `utils/caps_loader.py`에서 딥머지
- `target_app_info.json`의 `appPackage/bundleId` 등은 각 환경 파일에서 누락 시 자동 보완
- 포트 충돌 방지: Android `systemPort`, iOS `wdaLocalPort` 자동 할당(미지정 시)

## 드라이버 팩토리
- `driver/driver_factory.py`에서 플랫폼에 맞는 Options(`UiAutomator2Options`, `XCUITestOptions`)로 Remote 세션 오픈
- 서버/캡 경로/플랫폼은 `config/server_env.py`에서 `SERVER_ENV`를 기준으로 자동 해석

## POM 구성 가이드
- 베이스: `pages/base_page.py` (find/tap/type/wait 유틸)
- 공통 모듈: `pages/common/{module_common, module_precondition, module_scenario}.py`
- 예시 페이지: `pages/example/home_page.py`
  - 단일 클래스에 플랫폼별 로케이터 맵 구성(`LOCATORS["android"|"ios"]`)
  - 신규 화면은 이 패턴을 복제하여 로케이터만 교체

## 테스트 작성
- 공통 픽스처: `tests/conftest.py`
  - `.env` 로딩 → 서버/캡 결정 → 드라이버 생성/종료
- 예시: `tests/suite_no1/test_smoke_example.py`
  - 세션 기동 확인 및 예시 페이지 확인(로케이터 교체 전까지는 skip)

## 병렬 실행
- `pytest -n <workers>` 또는 `DEVICE_COUNT` 환경변수 사용
- Android는 `systemPort`, iOS는 `wdaLocalPort`를 자동 할당하므로 기본 병렬 안전
- 다중 디바이스: `TARGET_UDIDS="udid1,udid2" DEVICE_COUNT=2 ./run_tests.sh`처럼 지정하면 각 워커가 인덱스에 맞는 UDID를 사용

## 드라이버 빠른 기동 CLI
- uv로 설치 후:
```
uv run appium-pom-open --server-env local_aos --android-app ./apps/app.apk --duration 5
```
옵션:
- `--server-env` (`SERVER_ENV` 대체): `local_aos|local_ios|bs_aos|bs_ios`
- `--udid` (`UDID` 대체), `--android-app`, `--ios-app`, `--duration`

## 리포팅
- Allure 결과 생성(플러그인 필요):
```
uv sync --extra report
ALLURE=1 ALLURE_DIR=allure-results ./run_tests.sh -m smoke
# (선택) Allure HTML 생성(별도 CLI 필요: brew install allure 또는 공식 설치)
ALLURE=1 ALLURE_GENERATE=1 ALLURE_DIR=allure-results ALLURE_HTML_DIR=allure-report ./run_tests.sh -m smoke
```
- JUnit XML 생성:
```
JUNIT=1 JUNIT_XML=reports/junit/report.xml ./run_tests.sh
```
- 실패 자동 첨부: 스크린샷(`reports/screenshots/*.png`), 페이지소스(Allure 첨부 또는 `reports/pagesource/*.xml`).
- Allure 환경 메타: `environment.properties` 자동 생성(`server.env`, `platform`, 디바이스/앱 관련 주요 캡빌리티).

## 확장 포인트
- 로케이터 헬퍼(`utils/locator_handler/*`) 추가 가능: text/xpath/accessibility_id 템플릿화
- 리포트: `allure-pytest`(선택) 추가 후 `--alluredir` 사용
- CI: `jenkins-*` 템플릿을 파이프라인으로 이식

## 트러블슈팅
- Appium v2: 드라이버/플러그인 설치 상태 확인(`appium driver list`)
- iOS: 서명, WDA 권한, `xcodeOrgId/xcodeSigningId` 확인
- BrowserStack: `BS_USERNAME/BS_ACCESS_KEY` 및 `app` 값(`bs://<app-id>`) 확인

---
본 템플릿은 루트 PRD 요구사항(구조/분리/병렬/클라우드/문서화)을 기준으로 최소 실행 예시를 제공합니다. 언어/러너 전환(예: Java + TestNG, TS + WDIO)도 가능합니다. 원하시면 해당 스택으로 동일 구조 변환을 추가해드릴게요.

## 문서(Manual)
- docs/01-getting-started.md
- docs/02-project-structure.md
- docs/03-capabilities-and-env.md
- docs/04-running-and-parallel.md
- docs/05-reporting.md
- docs/06-page-object-guide.md
- docs/07-ci-jenkins.md
- docs/08-troubleshooting.md
