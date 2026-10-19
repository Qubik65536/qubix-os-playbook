# Installation prerequisites

Prepare the **CachyOS Niri machine being customized**. Run all playbook commands
locally there as your ordinary desktop account with sudo access. Do not run the
entire playbook with sudo or as root: Homebrew/private UI builds require a non-root
account, and the three managed WezTerm files belong to the invoking account.

The target needs CachyOS x86-64, Linux/systemd, Pacman, Niri and Python 3.12+
(the validated Ansible environment uses 3.13). Qubix installs neither Linux nor an ISO.
Use a snapshot and console access for disposable-VM acceptance; boot activation
retains the project's explicit authorization policy.

Update the machine through the normal CachyOS full-system upgrade procedure first.
Prepare native desktop companions after reviewing the package transaction and native
Snapper/Limine hooks:

```bash
pacman -Sp --needed --print-format '%n %v' python noctalia wezterm jq starship fontconfig gsettings-desktop-schemas
sudo pacman -S --needed python noctalia wezterm jq starship fontconfig gsettings-desktop-schemas
noctalia --version
```

Standalone Noctalia >=5.2.0 and <6.0.0 is required for the desktop; default private
caption/compact builds require the exact versions in the [login guide](login.md).
No SSH daemon, network inventory, Node.js or Luau fixture interpreter is required for
ordinary user deployment. Those testing tools belong to [developer setup](../development/environment.md).

Download/extract the playbook and create its local Python environment using
[deployment instructions](deployment.md#obtain-the-playbook). The locked tool file
includes validators as well as Ansible; users need not run the development test suite.
Prepare Paru/Homebrew/WezTerm, the pinned fonts, private UI clients and KWallet through
the separate commands in that guide. Normal `deploy` validates these prerequisites
without installing packages or downloading fonts. Preparation may require network access.

Keep the playbook root writable by your account and run from that directory. The
shipped `inventory/local.ini` explicitly selects `localhost ansible_connection=local`.
Always pass it in user commands. It needs no address, username or credentials.

Continue with [local deployment](deployment.md); consult the [configuration contract](../architecture/configuration.md)
for all defaults and prerequisite/ownership exceptions.
