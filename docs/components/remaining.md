# Remaining component contracts

Desktop/shell, SDDM, both loaders, Plymouth and state/recovery have implemented candidate contracts. See [boundaries](../architecture/components.md), [shell](shell.md), [login](login.md), [bootloader](bootloader.md) and [Plymouth](plymouth.md).

Package/system automation is **Planned**; manual prerequisite preparation supports the candidate. Future automation must manage only explicitly required native packages/narrow defaults, retain Pacman ownership and distinguish package removal from file restoration. No general provisioning framework is planned.

New component documents cover responsibilities, platforms, dependencies, options, ownership, deployment, verification, recovery and limits. Use a dedicated document for concrete design; avoid placeholder roles.
