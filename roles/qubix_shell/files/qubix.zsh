# Explicit opt-in: source /usr/share/qubix/shell/qubix.zsh in your own .zshrc.
if (( $+commands[starship] )); then
    if [[ -z "${STARSHIP_CONFIG:-}" && ! -f "${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml" ]]; then
        export STARSHIP_CONFIG=/etc/qubix/starship.toml
    fi
    eval "$(starship init zsh)"
else
    PROMPT='[Qubix %n@%m %1~]%# '
fi
