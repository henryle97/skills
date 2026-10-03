#!/usr/bin/env bash
# Require a numeric x.y.z version strictly greater than the base version.
#   scripts/check-version.sh <version> <base>
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <version> <base>" >&2
  exit 1
fi
version="$1"
base="$2"
for value in "$version" "$base"; do
  if [[ ! "$value" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]]; then
    echo "ERROR: invalid version $value; expected x.y.z without leading zeros." >&2
    exit 1
  fi
done

if ! jq -en --arg version "$version" --arg base "$base" \
  '($version | split(".") | map(tonumber)) > ($base | split(".") | map(tonumber))' >/dev/null; then
  echo "ERROR: version $version must be greater than $base. Run scripts/bump-version.sh <x.y.z>." >&2
  exit 1
fi
