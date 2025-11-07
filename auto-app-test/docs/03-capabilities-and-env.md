# Capabilities & Environment

캡빌리티와 환경변수 해석/병합 규칙을 설명합니다.

## 파일 구성
- `res/config/common.json`: 모든 환경 공통 값
- `res/config/conf_local_aos.json`: 로컬 Android
- `res/config/conf_local_ios.json`: 로컬 iOS
- `res/config/conf_bs_aos.json`: BrowserStack Android
- `res/config/conf_bs_ios.json`: BrowserStack iOS
- `res/config/target_app_info.json`: 앱 메타(패키지/번들ID 등)

## 병합 규칙
1) `common.json` + 환경별 파일을 딥머지
2) `target_app_info.json`의 누락 값 자동 보완
   - Android: `appPackage`, `appActivity`, `appWaitActivity`
   - iOS: `bundleId`
3) 환경변수 오버라이드
   - `ANDROID_APP` / `IOS_APP` → `app` 설정
   - `UDID`, `DEVICE_NAME`, `PLATFORM_VERSION` → 1:1 매핑
   - `EXTRA_CAPS_JSON` → JSON 문자열을 최종 캡에 딥머지
4) BrowserStack (`bstack:options`)
   - `BS_PROJECT`, `BS_BUILD`, `BS_SESSION_NAME`, `BS_LOCAL`로 자동 보완
5) 포트 자동 할당(미지정 시)
   - Android: `systemPort`
   - iOS: `wdaLocalPort`

## 예시: EXTRA_CAPS_JSON
```
EXTRA_CAPS_JSON='{"noReset": true, "language": "en", "locale": "US"}'
```

## 서버 URL
- `SERVER_ENV`
  - `local_aos|local_ios`: 기본 `http://127.0.0.1:4723`
  - `bs_aos|bs_ios`: `BS_USERNAME/BS_ACCESS_KEY` 기반 BrowserStack 허브 URL
- `APPIUM_SERVER_URL` 지정 시 우선 사용

