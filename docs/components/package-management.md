# CachyOS package management and terminal preparation

Status: **Implemented; controller fixtures and native existing-manager/WezTerm deployment Tested; fresh Brew/physical input pending**. Focused task: add an explicit CachyOS preparation step for
Paru, Homebrew on Linux (formerly Linuxbrew), and WezTerm; retire Alacritty and Foot.
Acceptance: CachyOS-only preflight, non-root Homebrew ownership, pinned installer,
check-mode transaction preview, idempotent package selection, dependency-safe removal,
and WezTerm on both Qubix terminal shortcuts and the session terminal environment.
Controller checks must pass; native installation, second application and graphical
shortcut/launcher checks require a disposable CachyOS VM and remain separate gates.

Run `playbooks/prepare-packages.yml` before desktop deployment. It is an explicit
preparation operation, like the existing login/keyring package playbooks, and is not
called by bootstrap or deployment. There are no new `qubix` switches: this is the
standard package selection for CachyOS Niri. Pacman installs Paru, WezTerm and the
Homebrew build prerequisites from configured repositories, without refreshing databases
or disabling package hooks. Bring the system fully up to date before preparation.
Paru/AUR builds and routine Brew operations run as the ordinary account, never root.

The connection account owns `/home/linuxbrew/.linuxbrew`, Homebrew's documented Linux
prefix. Root connections, unsupported architectures, unexpected prefix ownership,
prefix-directory symlinks and unfinished pre-existing prefixes are refused before writes. An existing
working installation owned by this account is preserved, including installed formulae;
preparation does not force an update. The official `bin/brew` symlink is resolved for executable validation. A fresh installation uses the official installer
at revision `be041513824fd2666a0e93cf5c3b0ca3bb0eb4b6`, SHA-256
`5f333bbe53bc490e51e7ccb1df8779b3dd6ee73a1a7379efda216edb08ccb148`,
with a pre-created writable prefix, no installer sudo and no dotfile editing.
The installer retrieves current Homebrew itself; the installer pin does not pin formulae.
See [upstream installation](https://docs.brew.sh/Installation) and
[Linux prerequisites](https://docs.brew.sh/Homebrew-on-Linux).

After successful package and Homebrew verification, Pacman removes only installed
`alacritty` and `foot`, using `-R` with dependency checks. It never cascades, forces
removal or deletes user settings. A dependent package blocks the transaction; resolve
that dependency explicitly and rerun. Other user-installed terminals are preserved.
This gives the stock CachyOS Niri installation a single terminal, WezTerm; it does not
purge arbitrary personal software. No running terminal or session is terminated.

The Qubix session sets `TERMINAL=/usr/bin/wezterm`; Super+T and Super+Return execute
`wezterm start`. WezTerm uses its own defaults and preserved personal configuration;
there is no new colour/font override. Legacy Qubix Foot resources remain inert with
existing recovery receipts. Native Niri configuration and personal shortcuts remain
preserved. Reload/select the Qubix session to activate changed shortcuts and log out/in
for its environment. Package changes are outside file restoration; reinstall removed
terminals with Pacman when reverting. For Brew shell access, follow the preparation
instructions; personal shell configuration is never edited automatically.

Check mode performs read-only package resolution and reports planned installation/removal;
it does not download/run the installer or prove a future package transaction will succeed.
No native installation, parser, session, screenshot or boot result is implied by controller tests.

The operator-authorized SSH installation now passes native parser/rendering, active-shell
selection and zero-change package/file reapplication. See [deployment evidence and
comparison captures](../project/package-management-test-results.md). This target already
had working Brew; fresh-install acceptance remains open.
