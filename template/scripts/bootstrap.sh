#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
if ! command -v java >/dev/null || ! java -version 2>&1 | grep -q 'version "17\.'; then
    sudo apt-get update
    sudo apt-get install -y openjdk-17-jdk-headless
fi
source scripts/env.sh
for command in curl unzip python3 git; do
    command -v "$command" >/dev/null || { sudo apt-get update; sudo apt-get install -y "$command"; }
done
if ! command -v task >/dev/null; then
    case "$(uname -m)" in
        x86_64)
            arch=amd64
            checksum=4367eba04abcbcb407578d18d2439ee32604a872419601abec76a829c797fb82
            ;;
        aarch64|arm64)
            arch=arm64
            checksum=61d773d7a81af2283079e640f14e8aa52a4e793460733a0da37228a283f4ce00
            ;;
        *) echo 'Unsupported Go Task host architecture' >&2; exit 2 ;;
    esac
    archive=$(mktemp)
    curl -fL --retry 3 "https://github.com/go-task/task/releases/download/v3.45.4/task_linux_$arch.tar.gz" -o "$archive"
    printf '%s  %s\n' "$checksum" "$archive" | sha256sum --check
    mkdir -p "$HOME/.local/bin"
    tar -xzf "$archive" -C "$HOME/.local/bin" task
    rm "$archive"
    export PATH="$HOME/.local/bin:$PATH"
fi
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
