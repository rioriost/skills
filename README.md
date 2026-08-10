# Rio's Codex Skills

Reusable skills and skill-only plugins for Codex.

## Available plugins

### App Store Review Preflight

`app-store-review-preflight` audits an Apple App Store submission before review. It checks the current official App Review Guidelines, App Store Connect metadata, and evidence from a local iOS, iPadOS, macOS, tvOS, visionOS, or watchOS project or built app.

The audit covers:

- All five App Review Guideline families: Safety, Performance, Business, Design, and Legal.
- Version metadata, screenshots, review credentials, notes, and build selection.
- App Privacy, privacy manifests, permissions, entitlements, and third-party SDK signals.
- In-App Purchases, subscriptions, content rights, export compliance, and regional requirements.
- Contradictions between App Store Connect declarations, project configuration, signed bundles, and observed behavior.

Findings are classified as `BLOCKER`, `WARNING`, `MANUAL`, `PASS`, `NOT APPLICABLE`, or `UNKNOWN`. The workflow defaults to read-only inspection and never submits an app without explicit authorization and final confirmation.

### Mac Performance Maintenance

`mac-performance-maintenance` runs a read-only health audit of an Apple Silicon Mac before recommending any cleanup. It covers storage, memory pressure and swap, CPU load, background items, Time Machine local snapshots, Xcode and Simulator data, Homebrew, container runtimes, virtual machines, large `~/Library` directories, and notebook battery health.

The bundled audit script never deletes data, starts or stops services, changes settings, or requests elevated privileges. Volatile tools such as Apple Container are inspected only after detecting the commands advertised by the locally installed CLI. Cleanup remains a separate, explicitly approved step.

#### Recommended workflow

1. Install **Mac Performance Maintenance** from this marketplace.
2. Ask Codex to run a read-only audit, using the skill name in the prompt.
3. Review findings classified as `ACTION`, `REVIEW`, `OK`, or `UNKNOWN`. Command failures are reported as coverage gaps rather than zero usage.
4. If cleanup is wanted, approve only the specific recommendation and target after Codex shows the expected benefit and risk.
5. Have Codex rerun the relevant checks and report the before-and-after result.

An audit request does not authorize cleanup. For example, after reviewing the report, a separate follow-up can approve one exact scope:

```text
Approve cleanup of the Homebrew cache preview only. Do not clean container
images, volumes, Simulator data, VM bundles, or any other target.
```

## Install

Add this repository as a Codex plugin marketplace:

```sh
codex plugin marketplace add rioriost/skills
```

Then open the Plugins Directory, select **Rio's Skills**, and install the plugin you need.

## Example prompts

```text
Use App Store Review Preflight to audit the App Store Connect submission
open in the in-app browser and the local app project. Do not submit it.
```

```text
App Store Review Preflightを使って、in-appブラウザで開いている
App Store Connectとローカルのアプリプロジェクトを監査してください。
提出操作は行わないでください。
```

```text
Use Mac Performance Maintenance to run a read-only audit of this Mac and rank
cleanup opportunities. Do not delete or change anything.
```

```text
Mac Performance Maintenanceを使って、このMacを読み取り専用で診断し、
改善候補を優先順位付きで示してください。削除や設定変更は行わないでください。
```

## Bundled tools

The bundled scanner can also collect static evidence directly:

```sh
python3 plugins/app-store-review-preflight/skills/app-store-review-preflight/scripts/inspect_apple_project.py \
  --project /path/to/project \
  --format markdown
```

Add `--app /path/to/App.app` to inspect a built app, verify its code signature, and extract signed entitlements on macOS.

The Mac maintenance audit can also be run directly:

```sh
/bin/bash plugins/mac-performance-maintenance/skills/mac-performance-maintenance/scripts/audit.sh
```

Use `--quick` to skip the broad `~/Library` size crawl during a fast first pass, and `--top N` to limit ranked lists:

```sh
/bin/bash plugins/mac-performance-maintenance/skills/mac-performance-maintenance/scripts/audit.sh \
  --quick \
  --top 10
```

The script writes its report to standard output. It performs no cleanup, writes no report file, starts no inactive runtime, and does not use `sudo`.

## Important notes

- Apple changes its requirements over time. The skill refreshes current official Apple sources during each audit rather than treating its bundled matrix as authoritative.
- A successful preflight cannot guarantee App Review approval.
- Legal rights, medical validity, regulated activity, and other facts that cannot be established technically remain manual confirmations.
- The Mac audit is a point-in-time diagnosis. It does not treat every cache, login item, snapshot, container volume, or VM as safe to remove.
- Some storage and background-item evidence can be unavailable unless the Codex host has macOS privacy permission to read it.
- This project is not affiliated with or endorsed by Apple Inc. Apple, App Store, iOS, and macOS are trademarks of Apple Inc.

## License

MIT License. See [LICENSE](LICENSE).
