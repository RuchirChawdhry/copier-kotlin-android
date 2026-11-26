#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports
trap 'adb logcat -d > reports/logcat.txt || true' EXIT
case "${ANDROID_CI_MODE:-checks}" in
    screenshots) bash scripts/screenshots.sh ;;
    checks) ./gradlew :app:connectedDebugAndroidTest --stacktrace ;;
    *) echo 'Unsupported CI mode' >&2; exit 2 ;;
esac
