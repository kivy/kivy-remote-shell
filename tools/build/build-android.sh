#!/usr/bin/env bash
set -eux pipefail

ROOT=$(realpath $(dirname "$0")/../..)

cd "$ROOT/tools/build"

BUILDOZER_BIN_DIR="$ROOT/.buildozer/bin" BUILDOZER_BUILD_DIR="${ROOT}"/.buildozer buildozer android debug deploy run logcat
