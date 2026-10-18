#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
fixture=$(mktemp -d)
trap 'rm -rf -- "$fixture"' EXIT
mkdir -p "$fixture/bin"
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
[[ $(bash "$fixture/wrapper" start) == start ]]
[[ $(bash "$fixture/wrapper" --config-file /explicit.lua start) == $'--config-file\n/explicit.lua\nstart' ]]
[[ $(bash "$fixture/wrapper" -e sh -lc 'printf test') == $'-e\nsh\n-lc\nprintf test' ]]
printf '%s\n' 'WezTerm compatibility entrypoint preserves native arguments and configuration discovery.'
