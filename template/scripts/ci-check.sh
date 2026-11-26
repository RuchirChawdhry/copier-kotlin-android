#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports
case "${1:-checks}" in
    checks) tasks=(ktlintCheck detekt lintDebug testDebugUnitTest assembleDebug assembleRelease) ;;
    screenshots) tasks=(:app:assembleDebug :app:assembleDebugAndroidTest) ;;
    *) exit 2 ;;
esac
for attempt in 1 2 3; do
    if ./gradlew "${tasks[@]}" --continue --stacktrace 2>&1 | tee "reports/gradle-$attempt.log"; then
        exit 0
    fi
    if ! grep -Eq 'Received status code (429|502|503|504)|Read timed out|Connection reset' "reports/gradle-$attempt.log"; then
        exit 1
    fi
    [[ "$attempt" != 3 ]] || exit 1
    sleep "$((attempt * 20))"
done
