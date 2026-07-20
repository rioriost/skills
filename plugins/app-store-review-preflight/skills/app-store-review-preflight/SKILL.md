---
name: app-store-review-preflight
description: Audit an Apple App Store submission against the current official App Review Guidelines before review. Use when Codex needs to inspect App Store Connect in a browser, check an iOS, iPadOS, macOS, tvOS, visionOS, or watchOS project or built app, prepare for a first submission or update, investigate likely review blockers, verify metadata/privacy/IAP/review notes, or stop immediately before Add for Review or Submit for Review. Default to a read-only preflight and never submit without explicit user authorization and final confirmation.
---

# App Store Review Preflight

Perform a traceable, evidence-based audit before App Review. Cover the entire current guideline set, not only previously observed rejection patterns.

## Safety boundary

- Default to read-only inspection.
- Do not edit metadata, upload files, add items for review, send messages, cancel a submission, or click `Submit for Review` unless the user explicitly requests that action.
- When submission is requested, finish the audit first, show every `BLOCKER`, `WARNING`, and `MANUAL` item, then obtain confirmation immediately before the final submission action.
- Never claim that the audit guarantees approval.
- Treat legal rights, medical validity, regulated activity, regional law, and facts not demonstrated by evidence as `MANUAL`.

## Required references

Read these files before beginning an audit:

- [official-sources.md](references/official-sources.md) for authoritative Apple sources and refresh rules.
- [audit-matrix.md](references/audit-matrix.md) for full-scope applicability routing.
- [report-format.md](references/report-format.md) before producing the final report.

## Workflow

### 1. Establish scope

Identify or infer:

- App, platform, version, build, first submission versus update, and distribution regions.
- Business model, account/login behavior, target audience, and regulated domain.
- Payments, subscriptions, ads, UGC, messaging, AI-generated content, web content, external hardware, background behavior, and third-party services.
- Data collected, permissions requested, SDKs used, and content or trademarks owned by others.

Do not stop for facts that can be read from the repository or App Store Connect. Record unresolved facts as `UNKNOWN` and route them to `MANUAL` when material.

### 2. Refresh Apple requirements

Open the current official App Review Guidelines and the relevant Apple help or documentation pages from `official-sources.md`. Apple describes the guidelines as a living document; do not rely only on remembered wording or the bundled matrix. Use only Apple primary sources for normative claims. Record the guideline page's displayed update date when available.

### 3. Inspect local evidence

When a local project is available, run:

```bash
python3 <skill-dir>/scripts/inspect_apple_project.py \
  --project <project-path> \
  --format json
```

When a built `.app` is available, add `--app <path-to-app>`. Treat script findings as evidence and risk signals, not automatic proof of compliance. Inspect the relevant source and configuration files when a signal affects a guideline decision.

Check at minimum:

- Info.plist purpose strings and metadata.
- Entitlements and macOS App Sandbox scope.
- Privacy Manifest declarations and third-party SDK manifests.
- StoreKit configuration and product identifiers.
- Version/build identifiers and embedded helpers or extensions.
- Code paths corresponding to protected resources, payments, login items, ads, tracking, UGC, AI, web content, and external hardware.

### 4. Inspect App Store Connect

If the user names the in-app browser, use the Browser skill and the existing signed-in tab. Inspect the submission without changing it. Otherwise use an applicable connector or the browser surface selected by the user.

Review every applicable area, including:

- App version metadata, screenshots/previews, build selection, release method, and localization.
- App Review contact, credentials/demo mode, notes, attachments, backend availability, and hardware instructions.
- App Information, age rating, content rights, categories, and license agreement.
- App Privacy, privacy policy, tracking, collected-data answers, and user privacy choices URL.
- Pricing/availability, export compliance, regional compliance, and trader status where applicable.
- In-App Purchases, subscriptions, agreements, tax/banking readiness, product metadata, review screenshots, and submission association.
- Game Center, events, custom product pages, or other items included in the draft submission.

Capture exact visible labels, statuses, version/build numbers, and missing fields as evidence. Do not infer that a collapsed or inaccessible section is complete.

### 5. Apply the complete matrix

Evaluate all five current guideline families in `audit-matrix.md`: Safety, Performance, Business, Design, and Legal. Mark an item `NOT APPLICABLE` only when the app inventory or evidence supports that conclusion. Do not omit a guideline family merely because no previous rejection mentioned it.

Correlate four evidence classes:

1. App Store Connect declarations.
2. Repository or signed-bundle configuration.
3. Observed runtime behavior, screenshots, or review video.
4. Developer statements or legal documents.

Flag contradictions between evidence classes even when each field is individually complete.

### 6. Classify findings

- `BLOCKER`: A required field/item is missing, evidence directly conflicts, or the current official rule clearly prevents submission or approval.
- `WARNING`: A plausible rejection risk, ambiguous presentation, excessive entitlement, weak review evidence, or likely mismatch needs attention.
- `MANUAL`: A material fact cannot be established from available technical/UI evidence or requires legal, medical, regulatory, or business judgment.
- `PASS`: Sufficient evidence supports the applicable check.
- `NOT APPLICABLE`: Evidence shows the feature or condition is absent.
- `UNKNOWN`: Evidence was unavailable; convert to `MANUAL` if it can affect review.

Use cautious language. Cite the exact current guideline number and an official Apple URL for every `BLOCKER`, `WARNING`, and `MANUAL` item.

### 7. Report and stop

Follow `report-format.md`. Lead with readiness and counts, then list actionable findings, evidence checked, and remaining manual confirmations. End with one of:

- `NOT READY`: at least one blocker remains.
- `READY WITH MANUAL CONFIRMATIONS`: no blockers, but manual items remain.
- `READY FOR SUBMISSION`: no blockers and all material manual items were resolved.

Do not translate `READY FOR SUBMISSION` into a submission action without explicit authorization.

## Remediation

When the user asks for fixes, distinguish between:

- Local project edits.
- App Store Connect metadata edits.
- New build/archive/upload requirements.
- Evidence preparation such as demo credentials, video, hardware, or authorization documents.

After any fix, rerun only the affected checks plus contradiction checks. Require a full preflight again after selecting a different build or materially changing app behavior.
