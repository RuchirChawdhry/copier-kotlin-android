#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
bash scripts/sdk.sh install
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init
chmod +x gradlew
./gradlew addKtlintFormatGitPreCommitHook
