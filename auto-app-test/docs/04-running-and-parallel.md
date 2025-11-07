# Running & Parallel

테스트 실행 옵션과 병렬 전략을 설명합니다.

## 기본 실행
```
./run_tests.sh [tests/경로] [-m "표식"] [추가 Pytest 인자]
```
- uv가 설치되어 있으면 `uv run pytest`, 없으면 `pytest` 사용
- 예: `./run_tests.sh tests/suite_no1 -m smoke -k login`

## 환경변수
- `DEVICE_COUNT`: 워커 수(`pytest -n DEVICE_COUNT`)
- `SERVER_ENV`: `local_aos|local_ios|bs_aos|bs_ios`
- `TARGET_UDIDS`: `udid1,udid2,...` (워커 인덱스로 라운드로빈 매핑)
- `UDID`, `DEVICE_NAME`, `PLATFORM_VERSION`: 단일 디바이스 지정
- `EXTRA_CAPS_JSON`: 추가 캡빌리티 JSON 병합

## 워커-UDID 매핑
`tests/conftest.py`에서 `PYTEST_XDIST_WORKER`를 읽어 인덱싱합니다.
```
TARGET_UDIDS="emulator-5554,emulator-5556" DEVICE_COUNT=2 ./run_tests.sh -m smoke
```
각 워커는 자신의 인덱스에 해당하는 UDID를 사용합니다.

