# Page Object Guide

POM 규칙과 예시, 확장 방법을 설명합니다.

## 기본 규칙
- `BasePage` 공통 유틸 사용: `wait_visible`, `tap`, `type`, `by_*` 헬퍼
- 단일 클래스에 플랫폼별 로케이터를 `LOCATORS` 맵으로 분기
- 가능한 Accessibility ID 우선, 불가 시 XPath/Text 헬퍼 사용
- 화면 단일 액션은 Page, 복합 플로우는 `module_*`로 분리

## 예시
```python
class HomePage(BasePage):
    LOCATORS = {
        "android": {
            "welcome_text": BasePage.by_accessibility_id("welcome"),
            "get_started_button": BasePage.by_accessibility_id("get_started"),
        },
        "ios": {
            "welcome_text": BasePage.by_accessibility_id("welcome"),
            "get_started_button": BasePage.by_accessibility_id("get_started"),
        },
    }

    def _l(self, name: str):
        return self.LOCATORS[self.platform][name]

    def assert_loaded(self):
        self.wait_visible(self._l("welcome_text"))
```

## 로케이터 헬퍼
- `utils/locator_handler/`의 `acc_id`, `xpath`, `text` 헬퍼 활용
- 공통화 가능한 패턴은 헬퍼로 이동하여 중복 제거

## 모듈 구성
- `module_common`: 공통/유틸 액션(백그라운드, 앱 재기동 등)
- `module_precondition`: 사전조건 보장(콜드 스타트 등)
- `module_scenario`: 비즈니스 플로우 조합(E2E 시나리오)

