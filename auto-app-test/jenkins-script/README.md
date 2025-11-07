# Jenkins Local Template

Example environment variables to configure in a Jenkins job:

- `SERVER_ENV`: `local_aos` | `local_ios`
- `APPIUM_SERVER_URL`: `http://127.0.0.1:4723`
- `ANDROID_APP` / `IOS_APP`: Path to app binaries
- `UDID`, `DEVICE_NAME`, `PLATFORM_VERSION`: Device info
- `DEVICE_COUNT`: e.g., 2 (for pytest-xdist)
- `TEST_TARGET`: e.g., `tests/suite_no1`
- `MARKS`: e.g., `smoke and android`

Pipeline step:

```
#!/bin/bash
set -e
cd auto-app-test
chmod +x run_tests.sh
SERVER_ENV=${SERVER_ENV:-local_aos} \
DEVICE_COUNT=${DEVICE_COUNT:-1} \
./run_tests.sh "${TEST_TARGET:-tests}" -m "${MARKS:-smoke}"
```

