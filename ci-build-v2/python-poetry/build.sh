#!/usr/bin/env bash
set -e

function stage_init_release_local
{
	is_release_mode true || return 0
	stage_init_release

	printf "== DISABLING, remove when debugged\n"
	exit 1
}



printf "== Installing ci-build scripts and then running the build\n"
ci_build_url_base="https://raw.githubusercontent.com/Rothamsted/knetminer-common/refs/heads/ci-build-v2"
script_url="$ci_build_url_base/ci-build-v2/install.sh"
. <(curl --fail-with-body -o - "$script_url") "$ci_build_url_base" python-poetry

main
