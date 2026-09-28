---
name: mac-performance-maintenance
description: Diagnose and maintain Apple Silicon Macs safely. Use for a slow Mac, low SSD space, memory pressure or swap, high CPU, background/login items, Time Machine snapshots, Xcode and Simulator storage, Homebrew, Docker, Podman, Apple Container, Parallels, UTM, other local VMs, large Library folders, or MacBook battery health. Default to read-only diagnosis, verify installed CLI capabilities, rank measured findings, and require explicit scoped approval before cleanup or configuration changes.
---

# Mac Performance Maintenance

Diagnose before changing anything. Separate measured facts, hypotheses, recommendations, approved actions and verified results.

This standalone edition contains the complete workflow for Zed's Markdown URL import. Use available local terminal and read-only inspection tools; no adjacent files, downloaded helpers or Codex-specific tools are required. Do not download and execute a remote audit script to use this skill. If local execution is unavailable, provide a focused manual plan and label all unobserved conditions unknown.

## Scope and safety

- A diagnosis request authorizes observation, not deletion, pruning, uninstalling, service changes, login-item changes or settings changes. Keep recommendations separate from execution.
- Do not use `sudo`, change privacy permissions, install missing utilities, or start dormant apps, containers, VMs or services just to inspect them. Report inaccessible data and missing tools as coverage gaps.
- Treat container volumes, VM disks, Xcode archives, Simulator data, packages and Time Machine snapshots as potentially valuable. Size or age alone never establishes that an item is disposable.
- Do not run broad cleanup commands, erase caches indiscriminately, edit system-managed internals, or stop a busy process to make a report cleaner.
- Use the user's existing exact authorization when applicable. If scope, targets, consequences or ownership are unclear, present a concrete plan and obtain explicit approval before changing anything. A tool permission grant is not cleanup authorization.
- Inspect the intended local Mac. In remote development or a terminal connected to another host, do not assume the shell belongs to the user's Mac. Do not query remote Docker/Podman endpoints as part of a local audit.
- Raw output may expose account paths, project/process/VM names and organization details. Minimize collection, summarize locally, and review/redact before sharing. Never collect credentials or publish raw logs by default.

## 1. Establish the baseline

Infer the user's symptom, urgency, current workload and requested scope from available context. Ask only for missing information that affects diagnosis or action. For a focused complaint, inspect the baseline and relevant areas; a full inventory is not mandatory.

Run small, separate read-only checks. Record timestamp, host context, macOS version/build, Apple Silicon capability, memory, uptime and selected evidence. Example platform checks:

```sh
date '+%Y-%m-%d %H:%M:%S %Z'
uname -s
```

Proceed with macOS commands only when the host reports Darwin:

```sh
sw_vers
uname -m
sysctl -n hw.optional.arm64
sysctl -n hw.model
sysctl -n hw.memsize
uptime
```

Require `hw.optional.arm64` to report `1` for this Apple Silicon workflow. A translated shell can report `x86_64`; distinguish that from the hardware capability. If the host is unsupported or detection fails, explain the limitation instead of guessing macOS commands or diagnosing a different machine.

For a quick baseline, run the following individually where available. These examples do not authorize other options such as memory-pressure simulation:

```sh
df -h / /System/Volumes/Data
memory_pressure -Q
sysctl vm.swapusage
vm_stat
ps -Ao pid,%cpu,%mem,etime,comm -r
```

Show only the relevant leading processes in the report. Prefer executable names to full command arguments, which can contain secrets. Capture exit status and errors before filtering output; a failed command or partial scan is never zero usage or a successful check.

Use execution time limits appropriate to the available tool. Expensive inventories and size scans should be bounded and cancellable; mark interrupted results partial. Do not install a timeout utility solely for diagnosis. Never terminate an unrelated process to enforce a diagnostic timeout.

## 2. Inspect relevant areas

Check tool availability first. For volatile third-party CLIs, read the installed version and local help for each intended subcommand and option. Commands below are candidates, not a guarantee that a particular version supports them. A missing command means unknown or not installed, not permission to install/update it.

### Storage and Library

- Record mounted-volume free space. APFS volumes share capacity; do not sum their free space or count the system/data pair as independent disks.
- Measure only relevant existing directories with a quoted path, for example `du -sk "$HOME/Library/Developer/Xcode/DerivedData"`. Preserve errors: a partial total is a lower bound, not a complete measurement.
- Start with likely workload-related folders; expand to a bounded top-level `~/Library` size scan only when necessary. Skip cloud placeholders and broad home-directory crawls when they could trigger downloads or disproportionate I/O.
- Distinguish allocated directory usage, logical VM disk size, APFS clones/snapshots, purgeable storage and immediately reclaimable bytes. Container and directory totals may overlap; do not add them into a promised recovery figure.
- Never directly remove files inside managed app containers, VM bundles, Simulator storage or live databases merely because a scan ranks them highly.

### Memory and CPU

- Interpret `memory_pressure -Q`, `vm_stat`, swap and the workload together. High occupied RAM, cumulative counters or nonzero swap alone do not establish a current problem.
- Take timestamped samples during the reported symptom and compare with an idle/recovered interval where practical. For counter deltas, use the reported page size, sampling duration and uptime; do not treat counters since boot as instantaneous rates.
- Correlate sustained CPU with process ownership, elapsed time and expected builds, indexing, backups, virtualization or media work. A single process sample is insufficient to recommend disabling it.
- If symptoms are intermittent, explain the missing reproduction window. Do not infer thermal throttling or defective hardware solely from CPU usage; use supported observations and label hypotheses.

### Login and background items

- Inspect System Settings' login/background-item list if available, or locally supported read-only `sfltool dumpbtm` with a time limit. Treat changing output formats and permissions as possible coverage gaps.
- Inventory relevant plist names under `~/Library/LaunchAgents`, `/Library/LaunchAgents` and `/Library/LaunchDaemons`. Read a selected plist only when necessary to identify its owner and executable.
- A registration or file's presence does not prove the service is running or harmful. Correlate it with runtime state, measured resource use and the user's need for the software.
- Do not disable, unload, reset or delete registrations during diagnosis. Avoid enumerating system-owned services without a symptom-specific reason.

### Time Machine and APFS snapshots

- Use `tmutil listlocalsnapshots /` when supported. Preserve errors and distinguish no snapshots from an unavailable inventory.
- Snapshots are managed recovery data, not a default cleanup target. Do not thin or delete them during an audit, disable backups, or promise their apparent size as recoverable space.
- If snapshot cleanup is proposed, identify the exact snapshots, recovery consequences and relevant backup state before seeking scoped approval.

### Xcode and Simulator

- Use `xcode-select -p` to identify the configured developer directory; do not switch it, install components or accept licenses as an audit side effect.
- Measure relevant existing folders: `~/Library/Developer/Xcode/DerivedData`, `Archives`, `iOS DeviceSupport`, `~/Library/Developer/CoreSimulator`, `~/Library/Developer/XCTestDevices`, and `/Library/Developer/CoreSimulator`.
- Runtime bundles or mounted runtime volumes are inventory clues, not an authoritative complete list on every Xcode generation. Absence from a known path does not establish absence of installed runtimes.
- Avoid commands that boot devices or activate dormant Simulator services solely for inventory. If a supported enumeration requires activation, report that coverage gap.
- Separate rebuildable build products from archives needed for distribution/symbolication, test-device data and Simulator app/user data. Prefer supported Xcode/Simulator management for any later approved removal.

### Homebrew

- If installed, inspect version, prefix and installed formulae/casks using supported read-only commands. Do not update, upgrade, uninstall or autoremove during diagnosis.
- For a cleanup opportunity, first inspect `brew cleanup --help`. Only if it advertises `--dry-run`, preview with `env HOMEBREW_NO_AUTO_UPDATE=1 brew cleanup --dry-run`.
- A preview is not approval to execute it. Identify which versions/cache entries it covers, whether active projects depend on them, and the cost of downloading or rebuilding again.

### Containers and virtual machines

- Discover installed Docker, Podman, Apple Container, Parallels, UTM, Lima, Colima or VirtualBox tools without launching their applications. Read local help before assuming subcommand compatibility.
- Check configured contexts/connections without changing them. Establish that the intended endpoint belongs to this Mac and that its required runtime is already active before making daemon-dependent queries. If that cannot be established safely, skip those queries.
- For an already active local runtime, use supported inventory/disk-usage commands such as Docker/Podman `system df` and container listings. Apple Container's available status, list, image, volume, machine, network and builder commands vary by release; inspect help at each level. Do not assume it implements Docker commands.
- Prefer supported read-only VM list/status commands when they do not start a dormant application or service. Never boot, resume, compact, prune or stop a VM/container during diagnosis.
- For offline size evidence, inspect relevant existing locations such as `~/Library/Containers/com.docker.docker`, `~/Library/Group Containers/group.com.docker`, `~/.local/share/containers`, `~/.colima`, `~/.lima`, `~/Library/Application Support/com.apple.container`, `~/Parallels`, `~/Documents/Parallels`, and UTM's app container. Installation-specific paths may differ; do not call this inventory exhaustive.
- Images, build caches, writable container layers, volumes and whole VM disks have different recovery risks. An unused or stopped resource can still contain the only copy of data. Do not delete bundle internals or use prune-all commands to reach a space target.

### Battery

- Use `pmset -g batt` and, on a notebook when relevant, `system_profiler SPPowerDataType -detailLevel mini`. Record reported condition, cycle count, maximum capacity if present, power source and workload.
- Classify a confirmed desktop without an internal battery as not applicable. A command error, absent field or failed model identification means unknown, not desktop/not applicable.
- Treat battery health indicators and observed drain as different findings. Do not infer a fault from one charge reading or apply a universal replacement threshold without model-specific current Apple evidence.

## 3. Rank findings and propose actions

Use these labels consistently:

| Label | Meaning |
| --- | --- |
| ACTION | Evidence supports a concrete issue worth addressing; this label does not authorize a change |
| REVIEW | Potential concern requiring context, trend evidence or a user decision |
| OK | Observed check showed no concern in the measured conditions |
| UNKNOWN | Missing, failed, inaccessible, partial or unperformed check |
| NOT APPLICABLE | Confirmed irrelevant to this hardware/workload, with a reason |

As a triage heuristic, less than 10% free space or 20 GB merits prompt attention; less than 20% merits review. These are not Apple requirements or guarantees of failure. Apply workload needs and volume context; avoid false precision.

For each recommendation include the measured evidence, target, expected benefit, uncertainty, data/recovery risk and recreation cost. Prioritize sustained performance problems and recoverable storage before valuable data. Separate rebuildable caches from managed but disruptive resources and irreplaceable data. If no meaningful issue is observed, say so without inventing cleanup work.

Use local help and observations for installed behavior. Fetch current official Apple or tool-vendor documentation when a command's side effects, compatibility, platform behavior or a model-specific claim remains uncertain. Do not bake a latest OS/tool version into this skill. Record source/version context and distinguish vendor requirements from operational heuristics. Offline uncertainty limits the recommendation; it is not grounds to experiment with destructive options.

## 4. Execute only the approved scope

Before any change, present the exact command or UI action, specific paths/resource identifiers, preview results where available, expected benefit, loss/recovery implications and verification plan. Check for active use and shared ownership. For irreplaceable data, establish a suitable backup or export before proceeding.

Obtain explicit approval for each destructive or configuration-changing group unless the existing user instruction already covers that concrete scope and consequences. Do not ask again for the same valid approval. A broad request to make the Mac faster or free space is not approval for arbitrary deletion.

Prefer the owning application's supported cleanup mechanism. Recheck current help and targets immediately before execution. If a target, preview, command behavior or consequence differs from the approved plan, stop and present the changed scope. Do not broaden cleanup after a failure or silently substitute direct filesystem deletion.

Record what actually succeeded, failed or remained untouched. Never describe a proposed or dry-run action as performed. Stop on unexpected results and preserve diagnostic evidence.

## 5. Verify and report

Rerun the relevant checks after an approved change using comparable timing, workload and volume context. Compare measured free space or performance with the baseline; actual reclaimed space can differ from estimates. Verify affected apps/services still work within the approved scope, without starting unrelated workloads.

Finish with a concise report containing: host/time/symptom, prioritized findings and evidence, proposed versus performed actions, before/after measurements, and unknown or uninspected areas. A successful command is not proof that the original symptom improved. State if the symptom could not be reproduced or if no cleanup was performed.

## Attribution and maintenance

Adapted from [Rio's Mac Performance Maintenance skill](https://github.com/rioriost/skills/tree/main/plugins/mac-performance-maintenance). This is a portable workflow, not the bundled script's automated report. Review this edition alongside source changes; URL imports save a local copy and do not update automatically.

MIT License

Copyright (c) 2026 Rio Fujita

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
