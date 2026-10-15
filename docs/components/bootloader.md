# Bootloader adapters

Status: Implemented candidate; GRUB and Limine preservation/reapplication/file-restoration/version fixtures Tested. Actual boot and recovery still require independent VMs.

Both adapters are mandatory for MVP. `bootloader.enabled` remains false by default. Require an explicit `backend`, `config_path` and `confirm_active: true` based on actual boot-chain evidence. Auto is a schema value for inspection, not permission to guess a loader. Backups precede each activation file change.

## Graphical Limine revision

Status: **Planned corrective contract**. Install the existing attributed Qubix wallpaper at /boot/qubix/wallpaper.png and use a version-supported boot(): URI, blue-gray terminal palette, restrained margins/font size and Qubix heading. Replace only the documented global appearance directives in one marked block; preserve timeout/default selection, every entry, kernel path/argument and snapshot. Reject duplicate globals, shadowed/ambiguous active configurations and native config enrollment requiring unsupported EFI changes. Keep the factory wallpaper and native theme files intact. Test exact reapplication, restoration and negative cases before physical boot observation.

Plymouth's explicitly bound active-image staging may also update selected module_path aliases/digests. Config recovery metadata must record those aliases and ignore only those expected changes during preservation checks; every other entry byte remains protected. See the [active-image contract](plymouth.md#active-limine-image-repair). This is separate from ordinary Limine appearance and does not permit kernel or entry replacement.

GRUB supports `/boot/grub/grub.cfg` and `/boot/grub2/grub.cfg` only when the existing generated configuration actually sources `custom.cfg`. Install a named theme under that prefix and update one marked appearance block in the custom hook. Validate the candidate with `grub-script-check` before atomic replacement. Generated menu entries, kernel arguments, timeout, loader installation and disks are untouched; no grub-mkconfig regeneration is needed. Malformed markers fail rather than stripping unrelated content.

Limine requires a confirmed booted major version 8–12, native entry format and a regular active limine.conf under /boot or /efi. The adapter changes only interface_branding, term_foreground and term_background, whose shared syntax was checked against upstream version documentation. Duplicate directives and malformed markers fail. Entry sections and kernel arguments are preserved. There is no claimed Limine syntax-check command; fixture preservation checks do not establish boot validity.

This is minimal text/colour branding, not the graphical GRUB theme from Qubix OS BlueBuild. The inspected physical target's desktop deployment leaves bootloader.enabled=false, so it has no Qubix Limine appearance changes. Limine 12.9.3 supports wallpaper, terminal palette, margins and font scaling, but this adapter does not yet manage them. A richer Limine appearance needs its own version-aware asset/path design and independent VM boot/recovery evidence; GRUB theme.txt cannot be loaded by Limine. See the [installed-version reference](https://github.com/Limine-Bootloader/Limine/blob/v12.9.3/CONFIG.md).

Restore returns the original activation file and removes newly created named resources using recorded baselines. Before restoring an existing activation file, the boot adapter compares preserved content with the first baseline, ignoring only well-formed Qubix markers, the three managed Limine appearance directives and trailing line breaks. Changed entries, snapshot sections, kernel arguments or unrelated hook commands require reviewed native recovery; even force cannot authorize stale baseline replacement. Reapplication must not erase this protection merely by refreshing receipts. Boot-chain evidence, successful boot into original entries, encrypted-root prompts where applicable, and live-media/VM-snapshot recovery must be verified before MVP acceptance. Do not replace a loader to test branding: use a separate VM installation for each adapter.

Controller file-lifecycle tests use a no-op GRUB checker solely as a dispatch stub; exact original hashes/modes and originally absent theme removal are verified. Native parser/boot validity remains a separate VM gate.

Existing activation-file modes are preserved. Installed verification escalates read-only checks when login/boot/splash is selected, so private configuration is not made public for diagnostics.
