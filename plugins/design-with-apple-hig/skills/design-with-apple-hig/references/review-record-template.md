# Review and regression record template

Copy/adapt for substantial reviews; omit irrelevant fields with a reason. This is a skill-owned checklist, not an Apple certification. Use short inline results for small tasks.

## Context and version matrix

- Task/mode and core user flow:
- Repository revision/diff and pre-existing failures:
- Platforms, framework, minimum deployment OS, build SDK/Xcode:
- Current public release / relevant prerelease, dates and official URLs:
- Actual device/simulator, OS/build, screen/window, locale, input:
- Appearance, text size, motion/accessibility settings, data/state:

## Source ledger

| ID | Claim / decision | Class | Title, URL and section | Retrieved UTC | Apple update date if provided | Platform / OS / component / conditions | Original modal / strength | Freshness / extraction limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use `APPLE-HIG`, `APPLE-SDK`, `APPLE-POLICY`, `APPLE-RESOURCE`, `ACCESSIBILITY`, `OBSERVATION`, `AUDIT`, or `HEURISTIC`. Keep short source wording only when needed for a disputed modal; paraphrase the rest. Do not relabel an unverified source as a heuristic to hide uncertainty.

## Findings

| Stable ID | Finding / location / state | Severity | Evidence and source IDs | Impact | Fix | Reproduction / acceptance criterion | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use `open`, `fixed-pending-verification`, `verified-fixed`, or `accepted-with-rationale`. An accepted risk is not a passing check. Preserve IDs through retests.

## Validation checklist

Each applicable row needs `pass`, `fail`, `blocked`, `not-run`, or `not-applicable`, plus evidence or a reason. Unexecuted rows never default to pass. Add risk-specific cases; this is not a mandatory full Cartesian product.

| Check | Result | Configuration and procedure / command | Artifact / observation / reason |
| --- | --- | --- | --- |
| Baseline and target build | not-run | | |
| Relevant existing tests / lints | not-run | | |
| Actual screenshot and visual inspection | not-run | | |
| Resizing / compact and expanded layout | not-run | | |
| Light / Dark / contrast | not-run | | |
| Dynamic Type or platform text-size equivalent | not-run | | |
| Accessibility tree / Inspector / automated audit | not-run | | |
| VoiceOver core flow and reading order | not-run | | |
| Keyboard navigation / focus / dismissal and restoration | not-run | | |
| Platform primary input (touch, Crown, spatial, remote) | not-run | | |
| Reduce Motion on / off and equivalent outcome | not-run | | |
| Loading / empty / error / recovery | not-run | | |
| Affected minimum / current OS and sibling platform | not-run | | |
| Fix retest and adjacent regressions | not-run | | |

## Before/after and handoff

- Same-state before/after artifact paths, revisions, and configuration:
- Re-tested finding IDs, affected existing tests, and actual outcomes:
- New regressions or baseline differences (separate from pre-existing failures):
- Remaining unverified devices, versions, input methods and accessibility modes:
- Manual follow-up: specific flow, required environment, expected result:
- Conclusion bounded by evidence; scoring denominator only if scoring requested:
