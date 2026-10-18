#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$repo_dir"
revision="$(git rev-parse --verify "${1:-HEAD}^{commit}")"
package="qubix-os-playbook-$revision"
mkdir -p .cache/dist
# Only committed source is distributable; never include caches or local credentials.
git archive --format=tar --prefix="$package/" "$revision" | gzip -n > ".cache/dist/$package.tar.gz"
(
  cd .cache/dist
  shasum -a 256 "$package.tar.gz" > SHA256SUMS
)
printf 'Packaged committed revision %s in .cache/dist/%s.tar.gz\n' "$revision" "$package"
