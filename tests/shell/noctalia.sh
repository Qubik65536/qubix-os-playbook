#!/usr/bin/env bash
# Exercise the actual profile launcher with exec intercepted before Noctalia starts.
# Cases intentionally isolate variables and invoke exec indirectly through the sourced launcher.
# shellcheck disable=SC1090,SC2030,SC2031,SC2329
set -euo pipefail
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
fixture_dir="$(mktemp -d)"
profile="$fixture_dir/noctalia"
trap 'rm -rf -- "$fixture_dir"' EXIT
python3 - "$repo_dir/roles/qubix_niri/templates/noctalia.sh.j2" "$profile" <<'PY'
from pathlib import Path
import sys
from jinja2 import Template
Path(sys.argv[2]).write_text(Template(Path(sys.argv[1]).read_text()).render(
    qubix_profile_resolved={'niri': {'presentation': 'native'}}))
PY
if bash "$profile" --application; then
  printf '%s\n' 'Empty application invocation unexpectedly succeeded.' >&2
  exit 1
fi

(
  unset GSETTINGS_BACKEND
  exec() {
    [[ "$GSETTINGS_BACKEND" == memory ]]
    [[ "$NOCTALIA_CONFIG_HOME" == /etc/qubix ]]
    [[ "$NOCTALIA_STATE_HOME" == "$XDG_STATE_HOME/qubix" ]]
    [[ "$NOCTALIA_DATA_HOME" == "$XDG_DATA_HOME/qubix" ]]
    [[ "$XDG_CONFIG_HOME" == /preserved/config ]]
    [[ "$QUBIX_NATIVE_GSETTINGS_BACKEND_SET" == 0 ]]
    [[ "$1" == /usr/bin/noctalia ]]
    exit 0
  }
  export XDG_CONFIG_HOME=/preserved/config
  export XDG_STATE_HOME=/preserved/state
  export XDG_DATA_HOME=/preserved/data
  source "$profile"
)

(
  export GSETTINGS_BACKEND=memory
  export QUBIX_NATIVE_GSETTINGS_BACKEND_SET=0
  exec() {
    [[ "${GSETTINGS_BACKEND+x}" != x ]]
    [[ "$1" == app && "$2" == 'argument with spaces' ]]
    exit 0
  }
  set -- --application app 'argument with spaces'
  source "$profile"
)

(
  export GSETTINGS_BACKEND=memory
  export QUBIX_NATIVE_GSETTINGS_BACKEND_SET=1
  export QUBIX_NATIVE_GSETTINGS_BACKEND=keyfile
  exec() {
    [[ "$GSETTINGS_BACKEND" == keyfile ]]
    [[ "$1" == app ]]
    exit 0
  }
  set -- --application app
  source "$profile"
)

cat > "$fixture_dir/checksum" <<'SH'
#!/usr/bin/env bash
read -r input
[[ "$input" == 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff  /usr/bin/noctalia' ]] || exit 9
exit "${QUBIX_TEST_HASH_RESULT:-0}"
SH
chmod 700 "$fixture_dir/checksum"
python3 - "$repo_dir/roles/qubix_niri/templates/noctalia.sh.j2" "$profile" "$fixture_dir/checksum" <<'PY'
from pathlib import Path
import shlex
import sys
from jinja2 import Template
rendered = Template(Path(sys.argv[1]).read_text()).render(
    qubix_profile_resolved={'niri': {'presentation': 'qubix'}}, qubix_niri_ui_native_sha256='f' * 64)
# Substitute only the external checksum transport; run the production selecting logic.
Path(sys.argv[2]).write_text(rendered.replace('/usr/bin/sha256sum', shlex.quote(sys.argv[3])))
PY
for result in 0 1; do
  (
    export QUBIX_TEST_HASH_RESULT="$result"
    exec() {
      if [[ "$QUBIX_TEST_HASH_RESULT" == 0 ]]; then
        [[ "$1" == /usr/share/qubix/bin/noctalia ]]
      else
        [[ "$1" == /usr/bin/noctalia ]]
      fi
      exit 0
    }
    source "$profile"
  )
done

printf '%s\n' 'Noctalia profile and application environment preservation passed.'
