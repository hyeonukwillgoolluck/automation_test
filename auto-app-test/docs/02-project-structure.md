# Project Structure

템플릿 전체 구조와 각 디렉토리의 역할을 설명합니다.

## 디렉토리 개요
- `src/appium_pom/`: 프레임워크 핵심 코드
  - `config/`: 경로/앱 메타/서버 환경 해석
  - `driver/`: 플랫폼별 드라이버 팩토리(Remote 세션 생성)
  - `utils/`: 캡 병합, 포트, 로깅, 로케이터 헬퍼 등 공통 유틸
  - `pages/`: POM 베이스/공통 모듈/예시 페이지
- `res/config/`: 캡빌리티 및 앱 메타 정의(JSON)
- `tests/`: pytest 스위트/픽스처
- `run_tests.sh`: uv/pytest 자동 선택, 병렬/리포팅 플래그 처리
- `pyproject.toml`: PEP 621(uv) 기반 프로젝트 정의
- `jenkins-*`: 로컬/BrowserStack 파이프라인 예시

## 원칙
- POM을 통한 역할 분리: Page(Action)와 Module(Flow) 분리
- 캡빌리티/앱 메타 분리: JSON + 런타임 환경변수 병합
- 다중 플랫폼 공통화: 가능한 Accessibility ID 우선, 불가 시 플랫폼 분기 최소화
- 병렬 안전: Android `systemPort`, iOS `wdaLocalPort` 자동 할당

