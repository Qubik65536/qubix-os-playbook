#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$repo_dir"
revision="$(git rev-parse --verify "${1:-HEAD}^{commit}")"
package="qubix-os-playbook-$revision"
work_dir="$(mktemp -d)"
trap 'rm -rf -- "$work_dir"' EXIT
export PATH="$repo_dir/.venv/bin:$PATH"
(
  cd .cache/dist
  shasum -a 256 -c SHA256SUMS
)
tar -xzf ".cache/dist/$package.tar.gz" -C "$work_dir"
source_dir="$work_dir/$package"
test "$(cat "$source_dir/SOURCE_REVISION")" = "$revision"
test -x "$source_dir/bootstrap.sh"
for item in roles playbooks assets tests docs LICENSE NOTICE ansible.cfg requirements-dev.txt; do
  test -e "$source_dir/$item"
done
for item in .git .cache .venv config/local.yml inventory/target.local.ini; do
  test ! -e "$source_dir/$item"
done
# Run outside any checkout so Git parent discovery cannot mask archive failures.
cd "$source_dir"
export ANSIBLE_CONFIG="$source_dir/ansible.cfg"
export ANSIBLE_HOME="$work_dir/ansible"
ansible-playbook tests/playbooks/archive-state.yml
printf '%s\n' invalid > SOURCE_REVISION
if ansible-playbook tests/playbooks/archive-state.yml > "$work_dir/invalid.log" 2>&1; then
  echo 'Malformed archive revision was accepted.' >&2
  exit 1
fi
# Require the intended refusal, not an unrelated controller error.
grep -q 'Use the packaged source archive' "$work_dir/invalid.log"
printf '%s\n' 'Archive contents, checksum, executable modes and deployment provenance passed.'
