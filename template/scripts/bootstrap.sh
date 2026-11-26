#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
if ! command -v java >/dev/null || ! java -version 2>&1 | grep -q 'version "17\.'; then
    sudo apt-get update
    sudo apt-get install -y openjdk-17-jdk-headless
fi
for command in curl unzip python3; do
    command -v "$command" >/dev/null || { sudo apt-get update; sudo apt-get install -y "$command"; }
done
if ! command -v sdkmanager >/dev/null; then
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' EXIT
    curl -fL --retry 3 https://dl.google.com/android/repository/commandlinetools-linux-12266719_latest.zip -o "$tmp/tools.zip"
    unzip -q "$tmp/tools.zip" -d "$tmp"
    mkdir -p "$ANDROID_HOME/cmdline-tools"
    mv "$tmp/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest"
fi
echo 'Review and accept Android SDK licenses:'
sdkmanager --licenses
bash scripts/setup.sh
bash scripts/emulator.sh create
