# Jenkins BrowserStack Template

Required credentials in Jenkins credentials store or environment variables:

- `BS_USERNAME`
- `BS_ACCESS_KEY`

Optional:

- `BS_PROJECT`, `BS_BUILD`, `BS_SESSION_NAME`, `BS_LOCAL`

Pipeline step:

```
#!/bin/bash
set -e
cd auto-app-test
chmod +x run_tests.sh
export SERVER_ENV=bs_aos  # or bs_ios
export DEVICE_COUNT=${DEVICE_COUNT:-2}
./run_tests.sh "${TEST_TARGET:-tests}" -m "${MARKS:-smoke}"
```

