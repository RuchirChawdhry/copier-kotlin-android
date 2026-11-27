#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
name="${ANDROID_AVD_NAME:-template-dev}"
api=$(bash scripts/sdk.sh api)
case "$(uname -m)" in
    x86_64) arch=x86_64 ;;
    aarch64|arm64) arch=arm64-v8a ;;
    *) echo 'Unsupported emulator host architecture' >&2; exit 2 ;;
esac
image="${ANDROID_AVD_IMAGE:-system-images;android-$api;google_apis;$arch}"
serial="${ANDROID_SERIAL:-emulator-5554}"
case "${1:-status}" in
    create)
        sdkmanager "$image"
        if ! avdmanager list avd -c | grep -Fxq "$name"; then
            device_args=()
            if [[ -n "${ANDROID_AVD_DEVICE:-}" ]]; then
                device_args=(-d "$ANDROID_AVD_DEVICE")
            fi
            printf 'no\n' | avdmanager create avd -n "$name" -k "$image" "${device_args[@]}"
        fi
        ;;
    start)
        if ! adb -s "$serial" get-state >/dev/null 2>&1; then
            mkdir -p reports
            nohup emulator -avd "$name" -port "${serial#emulator-}" -no-window -no-audio \
                -no-boot-anim -gpu swiftshader_indirect > reports/emulator.log 2>&1 &
        fi
        timeout 240 adb -s "$serial" wait-for-device
        for attempt in $(seq 1 120); do
            [[ "$(adb -s "$serial" shell getprop sys.boot_completed | tr -d '\r')" != 1 ]] || exit 0
            sleep 2
        done
        echo 'Emulator did not boot' >&2; exit 1
        ;;
    stop) adb -s "$serial" emu kill ;;
    reset)
        adb -s "$serial" emu kill || true
        echo 'Restarting with erased AVD data'
        emulator -avd "$name" -wipe-data -no-window -no-audio
        ;;
    status) adb -s "$serial" shell getprop sys.boot_completed ;;
    *) exit 2 ;;
esac
