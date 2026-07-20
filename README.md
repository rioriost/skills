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

## Install

Add this repository as a Codex plugin marketplace:

```sh
codex plugin marketplace add rioriost/skills
```

Then open the Plugins Directory, select **Rio's Skills**, and install **App Store Review Preflight**.

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

## Local project inspection

The bundled scanner can also collect static evidence directly:

```sh
python3 plugins/app-store-review-preflight/skills/app-store-review-preflight/scripts/inspect_apple_project.py \
  --project /path/to/project \
  --format markdown
```

Add `--app /path/to/App.app` to inspect a built app, verify its code signature, and extract signed entitlements on macOS.

## Important notes

- Apple changes its requirements over time. The skill refreshes current official Apple sources during each audit rather than treating its bundled matrix as authoritative.
- A successful preflight cannot guarantee App Review approval.
- Legal rights, medical validity, regulated activity, and other facts that cannot be established technically remain manual confirmations.
- This project is not affiliated with or endorsed by Apple Inc. Apple, App Store, iOS, and macOS are trademarks of Apple Inc.

## License

MIT License. See [LICENSE](LICENSE).
