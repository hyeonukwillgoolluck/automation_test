# Troubleshooting

자주 발생하는 이슈와 해결 방법을 정리합니다.

## 공통
- Appium v2 드라이버 설치 확인: `appium driver list`
- 설치:
  - Android: `appium driver install uiautomator2`
  - iOS: `appium driver install xcuitest`

## Android
- `adb devices`에 대상 디바이스/에뮬레이터 표시 확인
- 포트 충돌: `systemPort` 자동 할당되지만, 충돌 시 `EXTRA_CAPS_JSON`로 고정 지정
- 권한/초기화: `autoGrantPermissions`, `noReset` 플래그 조정
- 앱 경로: `ANDROID_APP` 경로 유효성 확인, 로컬 권한 문제 점검

## iOS
- Xcode/Developer 계정/서명: `xcodeOrgId`, `xcodeSigningId` 확인
- WDA 신뢰 문제: 첫 연결 시 디바이스에서 신뢰 허용 필요
- 포트 충돌: `wdaLocalPort` 자동 할당, 충돌 시 고정 지정
- 시뮬레이터/실기기 선택: `DEVICE_NAME`, `UDID` 정확히 지정

## BrowserStack
- 앱 업로드 후 `bs://<app-id>`로 교체 필요
- 자격증명: `BS_USERNAME/BS_ACCESS_KEY`
- 로컬 연결 사용 시: `BS_LOCAL=true`, BrowserStack Local 바이너리 동작 확인

