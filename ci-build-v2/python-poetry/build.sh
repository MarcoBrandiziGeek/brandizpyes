#!/usr/bin/env bash
set -eE -o pipefail


printf "== Installing ci-build scripts and then running the build\n"
ci_build_version='1.1'
ci_build_url_base="https://github.com/KnetMiner/knetminer-ci/blob/$ci_build_version"
script_url="$ci_build_url_base/ci-build-v2/install.sh"
. <(curl --fail-with-body -o - "$script_url") "$ci_build_url_base" python-poetry

main
