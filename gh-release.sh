#!/usr/bin/env bash

# Creates a github release. Needs the gh command
# TODO: move to the ci-build directory

# Extract the version from the TOML
version=$(egrep '^version\s*=\s*\".+\"' pyproject.toml | sed -E 's/version\s*=\s*"(.+)"/\1/')

rel_notes=$(cat <<EOT
The package is on [PyPI](https://pypi.org/project/brandizpyes/).
Release notes [here](https://github.com/marco-brandizi/brandizpyes/blob/main/CHANGELOG.md).
EOT
)

echo gh release create "$version" --notes "$rel_notes"  
