## PRD: 모바일 앱 자동화 템플릿 고도화

### 1. 문서 개요
- **작성 목적**: 어떤 앱이든 번들 ID와 로케이터만 교체하면 자동화 스크립트를 구축할 수 있는 템플릿을 정의한다.
- **대상 독자**: 자동화 프레임워크를 확장·유지보수할 개발자 및 QA 엔지니어.

### 2. 배경 및 목표
- 다양한 모바일 앱을 빠르게 자동화하기 위한 템플릿이 필요하다.
- 프로젝트마다 구조를 새로 짜던 비효율을 제거하고, 공통 구성으로 재사용 가능하도록 한다.
- 최소한의 설정(앱 번들 ID, 로케이터, 디바이스 정보)만으로 로컬/BrowserStack/병렬 테스트 환경을 구성할 수 있어야 한다.

### 3. 범위 (In Scope)
- 공통 설정/구조 정의 및 예시 구현 제공
- POM(Page Object Model) 기반 모듈 구조 확립
- 로컬/BrowserStack 환경 실행 스크립트 제공
- 병렬 테스트 실행 지원(pytest-xdist)
- Jenkins 등 CI 파이프라인을 위한 템플릿 문서화

(In scope) 앱 개발팀/QA팀이 직접 추가할 로케이터, 시나리오 작성 가이드  
(Out of scope) 실제 서비스용 계정/크리덴셜, 비즈니스 로직별 상세 시나리오

### 4. 요구사항

#### 4.1 구조 및 설정
- `app_config.py` + `res/config/target_app_info.json`
  - 앱 이름, Android/iOS 번들 ID, API 호스트, 병령 테스트 프로젝트명 등을 중앙에서 관리
  - 기본값은 템플릿 예시로 제공하고, 실제 값은 해당 앱에서 덮어쓴다.
- `res/config/conf_local_{aos,ios}.json`, `conf_bs_{aos,ios}.json`
  - 로컬 및 클라우드 또는 온프래미스 병렬 환경의 디바이스/계정 정보를 입력하는 템플릿
  - UDID, 이메일 등은 사용자가 채워 넣도록 주석/가이드 포함

#### 4.2 로케이터 및 페이지 모듈
- `utils/locator_handler/{text,xpath,accessibility_id}.py`
  - 공통 로케이터 템플릿 제공, 신규 앱 로케이터만 정의하면 재사용 가능
- `page/`
  - 공통 모듈(`module_common.py`, `module_precondition.py`, `module_scenario.py`)
  - 예시 페이지(`page_name_no1/`) 제공 → 새 앱 화면별로 복제/확장
  - POM 규칙: 모듈(비즈니스 로직), func 파일(단일 액션), registry 등으로 역할 분리

#### 4.3 테스트 스위트
- `tests/suite_no1/`, `suite_no2/` 예시 구성
  - Pytest 기반, 스위트/시나리오 추가 가이드 포함
  - `pytest.ini`와 `run_tests.sh`에서 환경 변수로 실행 대상 제어

#### 4.4 실행 및 병렬화
- 단일 실행: `SERVER_ENV=local_aos poetry run pytest ...`
- 병렬 실행: `pytest -n <workers>` / `DEVICE_COUNT` 등을 활용
- `run_tests.sh`에서 DEVICE_COUNT, TESTCASES, TARGET_UDIDS, SERVER_ENV 등을 설정해 CLI 없이도 실행 가능

#### 4.5 CI / Jenkins 템플릿
- `jenkins-script/`, `jenkins-bs/`, `local_jenkins/`에 플레이스홀더 스크립트 유지
- 크리덴셜/버킷/슬랙 알림은 조직별 값으로 교체하도록 README에 안내

### 5. 비기능 요구사항
- 특정 회사/서비스명을 하드코딩하지 않는다(플레이스홀더 사용).
- README 및 하위 문서에서 구조/사용법을 문서화한다.
- Git 커밋 히스토리를 유지하며, 토큰·비밀값은 `.env` 또는 CI 설정으로 관리한다.
- 테스트 산출물(`results`, `allure-results` 등)은 gitignore 처리하거나 필요 시 자동 삭제 스크립트 제공.

### 6. 산출물 및 완료 기준
- 템플릿 저장소(또는 브랜치) 내 구조/README/예시 코드가 완성되어야 한다.
- README(루트 및 `/README` 폴더)에서 모든 요구사항이 문서화돼 있어야 한다.
- 새로운 앱을 대상으로 번들 ID와 로케이터만 교체해도 기동 가능한 최소 예시 테스트가 포함되어야 한다.
- 병렬 실행(`pytest -n`) 및 BrowserStack 실행 검증 로그 또는 가이드가 제공되어야 한다.

### 7. 승인 기준
- 템플릿 기반으로 새로운 앱 테스트를 구성해 성공적으로 실행/보고서 생성 가능해야 함
- 로컬/BrowserStack/병렬 등 주요 실행 시나리오에서 문제없이 동작할 것
- 문서만 보고도 다른 팀원이 템플릿을 이해하고 확장할 수 있을 것
