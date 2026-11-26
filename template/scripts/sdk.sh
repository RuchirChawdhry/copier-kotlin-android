#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
property() { sed -n "s/^$1=//p" gradle.properties; }
case "${1:-install}" in
    install)
        sdkmanager "platforms;android-$(property android.compileSdk)" \
            "build-tools;$(property android.buildTools)" platform-tools emulator
        ;;
    api) property android.compileSdk ;;
    *) exit 2 ;;
esac
