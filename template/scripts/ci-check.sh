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
        if [[ -n "${GITHUB_ENV:-}" && -n "${MAVEN_CENTRAL_URL:-}" ]]; then
            echo "MAVEN_CENTRAL_URL=$MAVEN_CENTRAL_URL" >> "$GITHUB_ENV"
        fi
        exit 0
    fi
    if ! grep -Eq 'Received status code (429|502|503|504)|Read timed out|Connection reset' "reports/gradle-$attempt.log"; then
        exit 1
    fi
    [[ "$attempt" != 3 ]] || exit 1
    if grep -q "Received status code 429" "reports/gradle-$attempt.log"; then
        export MAVEN_CENTRAL_URL=https://maven-central.storage-download.googleapis.com/maven2
    fi
    sleep "$((attempt * 20))"
done
