---
name: mac-performance-maintenance
description: Diagnose and maintain Apple Silicon Macs safely. Use when Codex needs to investigate a slow Mac, low SSD space, memory pressure or swap, high CPU load, background/login items, Time Machine local snapshots, Xcode and Simulator data, Homebrew, Docker, Podman, Apple Container, Parallels, UTM, other local VMs, large Library folders, or MacBook battery health; rank cleanup opportunities; or carry out a specifically approved cleanup. Default to a read-only audit, detect volatile CLI capabilities from local help before use, and require explicit approval before any deletion or configuration change.
---

# Mac Performance Maintenance

Diagnose before changing anything. Separate measured facts from hypotheses, and prefer targeted cleanup over broad purges.

## Safety boundary

- Default to read-only inspection. Do not delete, prune, uninstall, stop services, modify login items, change settings, or start dormant VMs or container services during the audit.
- Do not use `sudo` for diagnosis. Report inaccessible evidence as unknown instead of escalating privileges.
- Treat container volumes, VM bundles, Xcode archives, Simulator data, Homebrew packages, and Time Machine snapshots as potentially valuable user data.
- Never run a bulk cleanup such as `docker system prune`, `container ... prune`, recursive cache deletion, or Time Machine snapshot deletion without naming the exact scope and obtaining explicit approval.
- Re-check the installed CLI's `--help` before proposing or running an operation. Apple Container and other fast-moving tools may not match remembered syntax.
- Stop and ask when a cleanup target is ambiguous, shared, active, or difficult to recover.

## Workflow

### 1. Establish scope

Confirm whether the user wants diagnosis only or has already requested cleanup. Infer the Mac type, current symptoms, urgency, and important development workloads from local evidence when possible. Do not delay a safe audit for facts the machine can provide.

### 2. Run the read-only audit

Run the bundled script from the skill directory:

```bash
/bin/bash scripts/audit.sh
```

Use `--quick` only when the user needs a faster first pass; it skips the broad `~/Library` size crawl while retaining focused checks. The script performs no deletion, writes no files, starts no service, and requests no elevated privileges.

Read command failures as coverage gaps, not as proof that usage is zero. macOS privacy controls may hide some directories unless the host app has Full Disk Access.

### 3. Interpret evidence

Report a compact health summary with these states:

- `ACTION`: Current evidence indicates material storage pressure, sustained resource contention, or another clear problem.
- `REVIEW`: A meaningful cleanup opportunity or background load exists, but intent or recoverability must be confirmed.
- `OK`: The observed snapshot is within a comfortable range.
- `UNKNOWN`: The check was unavailable, denied, inactive, or inconclusive.

Use thresholds as prompts for investigation, not universal guarantees:

- Treat less than roughly 10% free storage or less than 20 GB free as urgent; review below roughly 20% free.
- Give current memory pressure more weight than RAM occupancy. Swap alone is not proof of a present problem; correlate it with pressure, compression, page-outs, uptime, and symptoms.
- Treat a single CPU sample as transient. Re-sample before blaming a process and distinguish expected builds, indexing, backups, or media work.
- Do not classify an item as harmful merely because it is a login item or launch service. Identify its owner, current state, and measured impact.
- Time Machine local snapshots and APFS purgeable space can be managed automatically by macOS. Do not recommend deleting them first.
- Explain that `du` and container disk-usage totals can differ from Finder/APFS reclaimable space.

Rank findings by likely impact and recoverability. For every proposed action, show the observed size or load, what would be removed or disabled, expected benefit, risk, and whether it can be recreated.

### 4. Propose a cleanup plan

End a diagnosis-only run with recommendations; do not execute them. Group candidates as:

1. Rebuildable or low-risk after confirmation, such as an unused build cache.
2. Tool-managed but potentially disruptive, such as unused images or old Simulator runtimes.
3. User data or state requiring careful manual selection, such as container volumes, VM bundles, Xcode archives, or package removal.

Prefer the owning tool's supported cleanup command over deleting its storage directories. For volatile tools, inspect root and subgroup help, verify that the target command exists, and use a dry-run or preview option when available.

### 5. Obtain approval and clean only the approved scope

Before each destructive group, present the exact command or UI action and its targets. Obtain explicit user approval after the plan is visible. Approval for one target does not authorize adjacent targets.

Record before metrics, perform only the approved operation, preserve failures for review, and do not widen scope automatically. If the installed command differs from the plan, stop and re-propose it.

### 6. Verify

Rerun the relevant audit sections, or the full audit when practical. Report reclaimed space and any changed CPU, memory, background-item, or runtime state. State what remains unresolved and what was not inspected.

## Coverage notes

- Apple Silicon and macOS are the supported baseline. Report a non-Apple-Silicon or non-macOS host as unsupported rather than guessing.
- On Mac notebooks, include battery power and health evidence. On desktop Macs, mark battery checks not applicable.
- Do not start Docker Desktop, Podman machines, Apple Container services, Parallels VMs, UTM VMs, or other dormant runtimes merely to inspect them.
- Use the focused developer and VM directory sizes as signals. Do not delete bundles or internal runtime files directly.
- Avoid sharing raw audit output publicly without review because process names, paths, VM names, and background items can reveal local project or organization details.
