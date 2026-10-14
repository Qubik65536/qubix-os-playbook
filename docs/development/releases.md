# Release process

Status: **Planned**. Bootstrap creates no release tags.

A release requires all scope acceptance criteria for its advertised capabilities, passing CI, recorded target/version evidence, updated compatibility/recovery procedures, and curated changelog. MVP cannot be released without independent GRUB and Limine tests and both Plymouth initramfs combinations.

Git tags identify reproducible source. Runtime manifests must later record the source revision and effective configuration digest. Dirty trees and unverified targets must be reported. Release publishing/tagging requires a separate authorized workflow; no image, ISO, or distribution release pipeline is part of this repository.
