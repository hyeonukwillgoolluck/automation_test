#!/usr/bin/env bash
set -euo pipefail

# Usage examples:
#   SERVER_ENV=local_aos DEVICE_COUNT=1 ./run_tests.sh tests/suite_no1 -m smoke
#   SERVER_ENV=bs_ios BS_USERNAME=xxx BS_ACCESS_KEY=yyy DEVICE_COUNT=2 ./run_tests.sh -m smoke

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)

TEST_TARGET=${1:-tests}
shift || true

MARKS=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--markers)
      MARKS=$2
      shift 2
      ;;
    *)
      EXTRA_ARGS+=("$1")
      shift
      ;;
  esac
done

export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

DEVICE_COUNT=${DEVICE_COUNT:-1}

# Reporting flags
ALLURE_FLAG=${ALLURE:-}
ALLURE_DIR=${ALLURE_DIR:-}
JUNIT_FLAG=${JUNIT:-}
JUNIT_XML=${JUNIT_XML:-}

if command -v uv >/dev/null 2>&1; then
  RUNNER=(uv run pytest)
else
  RUNNER=(pytest)
fi

CMD=("${RUNNER[@]}" -n "$DEVICE_COUNT" "$TEST_TARGET")

if [[ -n "$MARKS" ]]; then
  CMD+=( -m "$MARKS" )
fi

if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
  CMD+=("${EXTRA_ARGS[@]}")
fi

# Allure reporting (only if plugin available)
if [[ -n "$ALLURE_FLAG" || -n "$ALLURE_DIR" ]]; then
  ALLURE_DIR=${ALLURE_DIR:-allure-results}
  export ALLURE_DIR
  if "${RUNNER[@]}" --help 2>/dev/null | grep -q -- "--alluredir"; then
    CMD+=( --alluredir "$ALLURE_DIR" )
  else
    echo "WARN: allure-pytest plugin not detected; skipping --alluredir. Run 'uv sync --extra report'." >&2
  fi
fi

# JUnit XML reporting
if [[ -n "$JUNIT_FLAG" || -n "$JUNIT_XML" ]]; then
  JUNIT_XML=${JUNIT_XML:-reports/junit/report.xml}
  mkdir -p "$(dirname "$JUNIT_XML")"
  CMD+=( --junitxml "$JUNIT_XML" )
fi

echo "Running: ${CMD[*]}"
"${CMD[@]}"

# Optionally generate Allure HTML if requested and CLI exists
if [[ -n "$ALLURE_FLAG" && -n "$ALLURE_DIR" && -n "$ALLURE_GENERATE" ]]; then
  if command -v allure >/dev/null 2>&1; then
    OUT_DIR=${ALLURE_HTML_DIR:-allure-report}
    echo "Generating Allure report to $OUT_DIR"
    allure generate "$ALLURE_DIR" -o "$OUT_DIR" --clean || true
  else
    echo "Allure CLI not found; skip HTML generation" >&2
  fi
fi
