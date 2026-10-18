#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
fixture=$(mktemp -d)
trap 'rm -rf -- "$fixture"' EXIT
mkdir -p "$fixture/bin" "$fixture/home" "$fixture/xdg"
python3 - "$repo_dir" "$fixture" <<'PY'
import sys
from pathlib import Path
repo, root = map(Path, sys.argv[1:])
source = (repo / 'roles/qubix_niri/templates/wezterm.sh.j2').read_text()
(root / 'wrapper').write_text(source.replace('/usr/bin/wezterm', str(root / 'bin/wezterm')))
PY
cat > "$fixture/bin/wezterm" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@"
SH
chmod +x "$fixture/bin/wezterm"
qubix_test_home="$fixture/home"
qubix_test_config="$fixture/xdg"
run_wrapper() {
  env -u WEZTERM_CONFIG_FILE HOME="$qubix_test_home" XDG_CONFIG_HOME="$qubix_test_config" bash "$fixture/wrapper" "$@"
}
result=$(run_wrapper start)
[[ "$result" == $'--config-file\n/etc/qubix/wezterm/wezterm.lua\nstart' ]]
[[ $(env HOME="$qubix_test_home" XDG_CONFIG_HOME="$qubix_test_config" WEZTERM_CONFIG_FILE=/explicit.lua bash "$fixture/wrapper" start) == start ]]
[[ $(run_wrapper --skip-config start) == $'--skip-config\nstart' ]]
[[ $(run_wrapper --config-file /explicit.lua start) == $'--config-file\n/explicit.lua\nstart' ]]
for candidate in "$qubix_test_config/wezterm/wezterm.lua" "$qubix_test_home/.config/wezterm/wezterm.lua" "$qubix_test_home/.wezterm.lua"; do
  mkdir -p "$(dirname -- "$candidate")"
  printf '%s\n' 'personal configuration' > "$candidate"
  [[ $(run_wrapper start) == start ]]
  [[ $(cat "$candidate") == 'personal configuration' ]]
  rm -- "$candidate"
  ln -s "$fixture/absent.lua" "$candidate"
  [[ $(run_wrapper start) == start ]]
  rm -- "$candidate"
done
# Program arguments that resemble global flags must not disable the managed default.
[[ $(run_wrapper start -- program --skip-config) == $'--config-file\n/etc/qubix/wezterm/wezterm.lua\nstart\n--\nprogram\n--skip-config' ]]
printf '%s\n' 'WezTerm defaults respect explicit and personal configurations and preserve arguments.'
