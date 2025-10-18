#!/usr/bin/env bash
set -euo pipefail

echo "Top 20 largest objects in repo:" 1>&2
git verify-pack -v .git/objects/pack/*.idx 2>/dev/null | sort -k3 -n | tail -n 20 || true

echo "List all blobs (size then object) - may be heavy:" 1>&2
git rev-list --objects --all | sort -k2 || true

