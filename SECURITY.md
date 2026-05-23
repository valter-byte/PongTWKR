# Security Policy

## Supported Versions

Security updates and patches are actively provided only to the latest stable release. Older or modified local versions are unsupported.

| Version | Supported |
| ------- | --------- |
| v0.9    | ✅ Yes    |
| v0.8    | ⚠️ Critical fixes only |
| < v0.8  | ❌ No     |

---

## Security Philosophy (The Tweak Dilemma)

`PongTWKR` is a modular performance toolkit that alters core Linux kernel parameters, memory allocations (`ZRAM`, `swappiness`), low-level hardware structures, and — as of v0.9 — the EFI System Partition, NVRAM boot entries, and the kernel execution chain itself.

Because of its deep integration with `sysctl`, `/sys/`, EFI firmware, and hardware controls, **the toolkit requires root privileges (`sudo`) to execute its core modules.**

### ⚠️ Execution Risks

1. **Privilege Abuse:** Since the tool runs as root, any arbitrary command injection into subprocess calls could fully compromise the host system. Always verify you are running code cloned directly from the official repository before executing with `sudo`.

2. **Hardware & System Instability:** Tweaking values like `dirty_ratios` or forcing extreme I/O Scheduler parameters can cause data corruption, kernel panics, or thermal issues if mismatched with the hardware. We provide the freedom to push your system hard — but we prefer it doesn't happen by accident.

3. **v0.9 Boundary — EFI & Kernel Execution (High Risk):** The following modules introduced in v0.9 operate at the absolute limit of system safety:

   - **`efistub`** writes directly to the EFI System Partition and modifies NVRAM boot entries. A malformed or corrupted write can leave a system unbootable. The module implements atomic staging, integrity verification, and fallback backups — but no safety net is perfect, especially across exotic UEFI firmware implementations.

   - **`kexec`** loads a new kernel into physical memory and transfers execution to it, bypassing the BIOS entirely. If the loaded kernel or initrd is malformed, the system will crash with no clean recovery path. The built-in SCRAM protocol mitigates this before the point of no return, but once `kexec -e` is called, there is no undo.

   - **`kernelmgr`** modifies bootloader configuration files (`/etc/default/grub`, `loader.conf`). A bad write without a valid backup can break the boot chain on next reboot. Backups are created automatically before every edit.

4. **The Installer Vector:** The official installer uses `curl | sudo bash`. This is a known risk pattern. Before running the installer, verify the SHA256 hash of the install script against the value published in the corresponding GitHub Release. Never pipe to bash from an untrusted or unverified URL.

---

## Reporting a Vulnerability

If you discover a security vulnerability — including privilege escalation vectors, unvalidated input leading to command injection, unsafe subprocess construction, or logic bugs in the EFI/kexec modules that could cause unrecoverable system damage — please handle it responsibly.

### Reporting Process

1. **Do NOT open a public Issue** if the vulnerability allows full system compromise, malicious root execution, or unrecoverable data loss.

2. **Contact:** Open a confidential draft security advisory via [GitHub Security Advisories](https://github.com/valter-byte/PongTWKR/security/advisories/new), or reach the maintainer directly through the contact information on the GitHub profile.

3. **Include in your report:**
   - A clear description of the vulnerability and its impact.
   - The specific module affected (`efistub`, `kexec`, `kernelmgr`, `ksm`, CPU, RAM, VM, Disk, etc.).
   - A minimal reproducible example or proof of concept.
   - Your assessment of exploitability (local only, requires specific hardware, etc.).

This is a single-maintainer open source project. Reports will be acknowledged and evaluated on a best-effort basis, with a target of within one week. Critical issues affecting bootability or root execution will be prioritized.

---

## Best Practices for Users

- **Verify Source:** Always run code cloned directly from `github.com/valter-byte/PongTWKR`. Verify the installer hash against the value in the GitHub Release before executing.
- **Audit Subprocess Calls:** If you or a third party write custom modules, review all `subprocess` calls before running them with `sudo`.
- **Backup Before v0.9 Modules:** Before using `efistub`, `kexec`, or `kernelmgr`, ensure you have a bootable fallback — a live USB, a known-good GRUB entry, or a backup ESP. The modules create their own backups, but hardware is unpredictable.
- **Do Not Run on Production Systems:** `PongTWKR` is a performance and experimentation toolkit. It is not designed for servers, critical workstations, or any system where an unbootable state is unacceptable.
