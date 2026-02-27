#!/usr/bin/env bash
set -e

function stage_build_setup_local
{
	if [[ ! -z "$CI_SECRETS_GIST_TOKEN" ]]; then
		printf "== Downloading Project Secrets from gist location\n"
		gist_url="https://gist.githubusercontent.com/marco-brandizi/$CI_SECRETS_GIST_TOKEN/raw/github-brandizi-secrets.sh"
		source <(curl --fail-with-body -o - "$gist_url")
	fi
	
	stage_build_setup
}


printf "== Installing ci-build scripts and then running the build\n"
ci_build_url_base="https://raw.githubusercontent.com/Rothamsted/knetminer-common/refs/heads/ci-build-v2"
script_url="$ci_build_url_base/ci-build-v2/install.sh"
. <(curl --fail-with-body -o - "$script_url") "$ci_build_url_base" python-poetry

main
