# Preflight report format

Use this structure. Keep evidence concrete and avoid repeating the guideline text.

## Header

```text
App Store Review Preflight
App / platform: <name> / <platform>
Version / build: <version> / <build>
Submission type: <first submission | update | other>
Guidelines checked: <displayed last-updated date or retrieval date>
Readiness: <NOT READY | READY WITH MANUAL CONFIRMATIONS | READY FOR SUBMISSION>
Counts: BLOCKER n / WARNING n / MANUAL n / PASS n / NOT APPLICABLE n
```

## Actionable findings

Order by `BLOCKER`, `WARNING`, then `MANUAL`.

```text
[BLOCKER] Guideline 2.1(b) — In-App Purchase review access

Observation:
The purchase is visible in the build, but no matching item is included in the draft submission.

Evidence:
- Build: StoreKit product ID `example.pro`
- App Store Connect: draft submission contains only app version 1.0

Required action:
Complete the product metadata and add the IAP to the submission.

How to verify:
Confirm the product ID, status, review screenshot, and submission association.

Source:
<direct Apple URL>
```

## Coverage summary

Provide one compact table:

| Family | Status | Evidence or reason |
|---|---|---|
| Safety | PASS/MANUAL/... | Short summary |
| Performance | PASS/MANUAL/... | Short summary |
| Business | PASS/N/A/... | Short summary |
| Design | PASS/MANUAL/... | Short summary |
| Legal | PASS/MANUAL/... | Short summary |

## Evidence reviewed

List exact App Store Connect sections, local files, bundle path, runtime/video evidence, and developer-supplied documents. State what was unavailable.

## Final gate

- List unresolved manual confirmations.
- State whether the current selected build was audited.
- State explicitly: `No submission action was performed.`
- If the user requested submission and the result permits it, ask for confirmation immediately before clicking the final submit control.
