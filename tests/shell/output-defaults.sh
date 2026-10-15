#!/usr/bin/env bash
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
test_root=$(mktemp -d "${TMPDIR:-/tmp}/qubix-output-defaults.XXXXXX")
trap 'rm -rf -- "$test_root"' EXIT
export QUBIX_SCALE_TEST_ROOT="$test_root"
export QUBIX_JQ_BIN
QUBIX_JQ_BIN=$(command -v jq)
export QUBIX_NIRI_BIN="$test_root/niri"
export NIRI_SOCKET="$test_root/fixture.sock"
helper="$repo_dir/roles/qubix_niri/templates/output-defaults.sh.j2"

cat > "$test_root/niri" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=$QUBIX_SCALE_TEST_ROOT
printf '%s\n' "$*" >> "$root/commands"
case "$*" in
  'msg --json outputs')
    index=$(cat "$root/index")
    printf '%s\n' "$((index + 1))" > "$root/index"
    cat "$root/outputs-$index.json"
    ;;
  'msg --json event-stream')
    cat "$root/events"
    exit "${QUBIX_SCALE_STREAM_STATUS:-0}"
    ;;
  'msg output '*' scale 1.0') printf '%s\n' "$3" >> "$root/applied" ;;
  *) exit 10 ;;
esac
SH
chmod 0700 "$test_root/niri"
python3 - "$test_root" <<'PY'
import json,pathlib,sys
root=pathlib.Path(sys.argv[1])
states=[{'eDP-1':1.25}, {'eDP-1':1}, {'eDP-1':1.5},
        {'eDP-1':1.5,'DP-1':1.5}, {'DP-1':1},
        {'eDP-1':1.75,'DP-1':1}, {'eDP-1':1,'DP-1':1,'HDMI-A-1':None}]
for index,state in enumerate(states,1):
    (root/f'outputs-{index}.json').write_text(json.dumps({name:{'logical':{'scale':scale} if scale else None} for name,scale in state.items()}))
events=[{'WorkspacesChanged':{}},{'ConfigLoaded':{'failed':False}}]+[{'WorkspacesChanged':{}}]*4
(root/'events').write_text('\n'.join(json.dumps(e,separators=(',',':')) for e in events)+'\n')
(root/'index').write_text('1\n')
PY
bash "$helper"
printf 'eDP-1\nDP-1\neDP-1\n' > "$test_root/expected"
cmp "$test_root/applied" "$test_root/expected"

# Explicit once activation does not leave an event watcher.
printf '1\n' > "$test_root/index"
: > "$test_root/commands"
: > "$test_root/applied"
bash "$helper" --once
[[ $(wc -l < "$test_root/applied") -eq 1 ]]
if grep -q event-stream "$test_root/commands"; then exit 1; fi

# Bad input and a missing session fail before scale operations.
printf 'not-json\n' > "$test_root/outputs-1.json"
printf '1\n' > "$test_root/index"
: > "$test_root/applied"
if bash "$helper" --once > "$test_root/invalid.log" 2>&1; then exit 1; fi
[[ ! -s "$test_root/applied" ]]
if (unset NIRI_SOCKET; bash "$helper" --once) > "$test_root/session.log" 2>&1; then exit 1; fi
if bash "$helper" --unknown > "$test_root/usage.log" 2>&1; then exit 1; fi
printf '%s\n' 'Output defaults passed: startup, hotplug/reconnect, manual-scale preservation, disabled outputs, once mode and invalid input.'
