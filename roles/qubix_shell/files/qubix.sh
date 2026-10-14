# shellcheck shell=sh
# Qubix defaults, read by login shells. Existing personal settings take precedence.
if [ -z "${STARSHIP_CONFIG:-}" ] && [ ! -f "${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml" ]; then
    export STARSHIP_CONFIG=/etc/qubix/starship.toml
fi
if [ -n "${BASH_VERSION:-}" ]; then
    case "$-" in
        *i*)
            if command -v starship >/dev/null 2>&1; then
                eval "$(starship init bash)"
            else
                PS1='[Qubix \u@\h \W]\$ '
            fi
            ;;
    esac
fi
