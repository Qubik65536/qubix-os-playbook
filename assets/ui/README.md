# Native presentation variants

These patches apply to the exact released source archives in [manifest.yml](manifest.yml).
Both projects are MIT licensed; the original [copyright and license](LICENSE) are retained
and installed beside each private Qubix binary. Their native distribution packages remain intact.

- [Noctalia 5.3.0](https://github.com/noctalia-dev/noctalia/tree/v5.3.0): two caption changes,
  **QubixOS** in the launcher and **QubixOS (Noctalia version)** in Control Center Home.
  The System tab continues reporting the actual distribution/kernel. No os-release override.
- [Noctalia Greeter 1.6.0](https://github.com/noctalia-dev/noctalia-greeter/tree/v1.6.0):
  UI constants only; 340–380 px card, 36 px avatar, 13 px body/11 px captions,
  30/34 px controls and tighter spacing. No auth/session/compositor code changes.

`playbooks/prepare-ui.yml` verifies archive and patch SHA256, builds as the ordinary remote
account with two compiler jobs, stages only clients under root-owned `/var/cache/qubix-ui/`
and removes its temporary source directories. It never runs upstream installation hooks.
The private clients use assets from the exact matching installed native packages.
Unsupported releases fail deployment preflight. The selecting wrappers bind the exact native
binary checksum. Any native binary update, including a rebuild of the same version, falls back
to the updated native client with a diagnostic until a matching variant is reviewed and rebuilt.

See the [feature contract](../../docs/architecture/login-refinement.md) for ownership,
activation, native comparisons and acceptance boundaries. Build artifacts are host-specific
generated files, excluded from Git; the repository retains sources, checksums and patch history.
