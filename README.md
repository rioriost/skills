# Rio's Codex Skills

Reusable skills and skill-only plugins for Codex, with standalone Markdown imports for Zed.

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

### Apple HIG Design

`design-with-apple-hig` designs, implements and reviews Apple-platform interfaces using current primary sources. It separates HIG guidance, SDK requirements, App Review policy, observed behavior and heuristic advice; routes iOS, iPadOS, macOS, watchOS, tvOS and visionOS; and verifies builds, actual screenshots, accessibility, Dynamic Type, VoiceOver-relevant limits, keyboard/focus and Reduce Motion.

The [complete plugin](plugins/design-with-apple-hig/skills/design-with-apple-hig/SKILL.md) preserves the tested skill from [rioriost/design-with-apple-hig](https://github.com/rioriost/design-with-apple-hig), including its references, source reader and 20 regression tests. [SOURCE.json](plugins/design-with-apple-hig/SOURCE.json) records the exact revision and file digests. The original [Sunwood AI Labs MIT notice](plugins/design-with-apple-hig/LICENSE) is retained.

### Import Apple HIG Design into Zed by URL

In Zed, run **agent: create skill from url**, paste the following URL, review the imported skill, and save it in the User scope for use across projects:

```text
https://github.com/rioriost/skills/blob/main/zed/design-with-apple-hig/SKILL.md
```

This is the [standalone Zed edition](zed/design-with-apple-hig/SKILL.md). A Markdown URL import should not assume adjacent reference files or scripts are installed. This edition includes the essential workflow in one file, requires no Codex-specific tools or downloaded helpers, and retains MIT attribution inside the file. It is a portable adaptation, not a byte-for-byte copy of the complete edition.

After saving, select `/design-with-apple-hig` from the Agent Panel's slash-command menu and describe the app/design task. Importing saves a local skill; it is not a live subscription to this repository. Re-import to pick up future changes. If you already installed a skill with this name, inspect the existing entry before replacing it; you only need one edition per scope.

Zed's native skills apply to Zed Agent. External ACP agents use their own native skill configuration. See [Zed Skills](https://zed.dev/docs/ai/skills) for the current import behavior.

日本語: Zedの **agent: create skill from url** に上記URLを貼り付け、内容を確認してUserスコープへ保存します。参照ファイルやスクリプトを別途取得しなくても使える単一ファイル版です。完全版をフォルダーごと導入済みの場合は、同名スキルを上書きする前に内容を確認してください。

### Import Mac Performance Maintenance into Zed by URL

Run **agent: create skill from url**, paste this URL, review the content, and save it in the **User** scope to use it across projects:

```text
https://github.com/rioriost/skills/blob/main/zed/mac-performance-maintenance/SKILL.md
```

The [standalone Mac edition](zed/mac-performance-maintenance/SKILL.md) includes the diagnostic workflow, read-only command examples, coverage guidance, approval boundaries, before/after verification and MIT notice in one file. It needs no bundled audit script or downloaded helper. Zed Agent uses its available local tools to perform the relevant checks; importing the file does not itself run an audit. The complete Codex plugin and its audit script remain available separately.

Select `/mac-performance-maintenance` in the Agent Panel, then describe the symptom. For example:

```text
このMacを読み取り専用で診断し、改善候補を優先順位付きで示してください。
削除、設定変更、停止中のVMやコンテナの起動は行わないでください。
```

The same [Zed import and scope rules](https://zed.dev/docs/ai/skills) described above apply. Check for an existing skill with the same name before replacing it, and re-import when you want updates. External ACP agents use their own skill configuration.

日本語: 上記URLから取り込み、Userスコープへ保存すると各プロジェクトで利用できます。診断のみでは削除や設定変更を行わず、具体的な対象への明示的な承認がある場合だけ実行します。

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

## Validate skill packaging

Validate all standalone Zed editions with Python 3.10 or later:

```sh
python3 scripts/validate_zed_skills.py
```

This offline check validates skill metadata, size, Markdown resource links, embedded MIT notices and shell-example syntax without executing diagnostics. It does not establish agent behavior or successful import in Zed's UI. The dedicated Zed packaging workflow runs it when standalone editions change. When updating the Mac plugin, review the single-file edition against the source workflow and coverage before publication; the two editions are maintained explicitly rather than synchronized automatically.

Run from this repository root with Python 3.10 or later:

```sh
python3 scripts/validate_apple_hig.py
python3 plugins/design-with-apple-hig/skills/design-with-apple-hig/scripts/validate_repository.py
python3 -m unittest discover -s plugins/design-with-apple-hig/skills/design-with-apple-hig/tests -v
```

These offline checks verify provenance, standalone resource independence and the full edition's helper behavior. They do not certify UI quality, VoiceOver behavior or execution by Zed's agent. Native app verification happens when applying the skill to an app. GitHub Actions runs these checks on Python 3.10, 3.12 and 3.13.

To refresh the complete edition, select a reviewed source revision, replace its bundled files, update `SOURCE.json`, and review the standalone adaptation against changed instructions before running the checks. Do not silently update digests without reviewing source changes.

## Important notes

- Apple changes its requirements over time. The skill refreshes current official Apple sources during each audit rather than treating its bundled matrix as authoritative.
- A successful preflight cannot guarantee App Review approval.
- Legal rights, medical validity, regulated activity, and other facts that cannot be established technically remain manual confirmations.
- The Mac audit is a point-in-time diagnosis. It does not treat every cache, login item, snapshot, container volume, or VM as safe to remove.
- Some storage and background-item evidence can be unavailable unless the Codex host has macOS privacy permission to read it.
- This project is not affiliated with or endorsed by Apple Inc. Apple, App Store, iOS, and macOS are trademarks of Apple Inc.

## License

MIT License. See [LICENSE](LICENSE). The Apple HIG plugin also retains the original [Sunwood AI Labs license](plugins/design-with-apple-hig/LICENSE); its standalone adaptation carries both notices. Apple materials remain subject to their own terms.
