# Explicit opt-in: source /usr/share/qubix/shell/qubix.zsh in your own .zshrc.
if (( $+commands[starship] )); then
    export STARSHIP_CONFIG=${STARSHIP_CONFIG:-/etc/qubix/starship.toml}
    eval "$(starship init zsh)"
else
    PROMPT='[Qubix %n@%m %1~]%# '
fi
