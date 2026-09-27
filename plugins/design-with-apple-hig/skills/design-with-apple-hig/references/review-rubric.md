# Evidence-based review rubric

Use this rubric for formal reviews and requested scores. A score summarizes verified evidence; it does not certify HIG compliance.

## Review order

1. Core task failure, misleading state, data loss, privacy or safety harm, or inaccessible core action
2. Platform model, navigation, input, windowing, and adaptation mismatch
3. Hierarchy, readability, targets, contrast, state communication, content, and recovery
4. Motion, materials, visual refinement, performance, and delight

## Evidence reliability

| Label | Use | Minimum record |
| --- | --- | --- |
| `APPLE-HIG` | Current design guidance | title, URL, retrieval date, platform/section, wording strength |
| `APPLE-SDK` | API or implementation fact | documentation URL, SDK/OS availability when relevant |
| `APPLE-POLICY` | Distribution or App Review rule | current URL, section, retrieval date, distribution/region applicability |
| `APPLE-RESOURCE` | Official kit or asset rule | resource/version and license context |
| `ACCESSIBILITY` | Standard, API, or assistive test | standard criterion or test configuration |
| `OBSERVATION` | Visible/reproducible artifact fact | location, state, and reproduction condition |
| `AUDIT` | Automated signal | tool version, rule ID, engine, and classification |
| `HEURISTIC` | Design judgment | rationale and tradeoff; never call it an HIG violation |

Do not attach `APPLE-HIG` merely because a third-party file says “Apple.” Retrieve the primary page.

## Artifact limits

| Artifact | Can establish | Cannot establish alone |
| --- | --- | --- |
| Idea/requirements | task model, hierarchy, platform premise, privacy risks | rendering or runtime behavior |
| Screenshot | visible hierarchy, density, typography, color, apparent targets, one state | motion, focus/reading order, VoiceOver, Dynamic Type, interaction |
| Source code | component/API choice, semantics intent, state paths, adaptation logic | final rendering and assistive output |
| Simulator/live app | tested tasks, focus, gestures, transitions, rendered states | untested devices, OS versions, inputs, and modes |
| Design system | component contracts, tokens, states, mappings | correct downstream product use |

## Weighted score

| Dimension | Weight |
| --- | ---: |
| Platform fit and information architecture | 15 |
| Layout and visual hierarchy | 15 |
| Controls and interaction | 10 |
| Typography and content | 10 |
| Color, imagery, and materials | 10 |
| Accessibility and inclusion | 20 |
| Motion and perceived performance | 10 |
| Resilience and state completeness | 10 |
| **Total** | **100** |

Rate a verified dimension from 0 to 4, then multiply by `weight / 4`:

- `4`: representative states are verified, coherent, and platform-appropriate.
- `3`: good with limited, non-blocking gaps.
- `2`: mixed; an important state or convention is missing.
- `1`: major problems substantially reduce task quality.
- `0`: required behavior is absent or broken.
- `NV`: not verified; exclude it from earned and possible points.

Report `earned / verified possible`, coverage as `verified possible / 100`, and any normalized value only when the user explicitly needs comparison. Example: `42/60 verified points; 60% coverage`, not an unsupported `70/100`.

Do not double-deduct one root cause. Cap visual-polish praise when task completion or access is broken. Any Critical finding means `not ship-ready` regardless of score.

## Severity

- `Critical`: core task cannot complete; credible data loss, privacy, or safety harm; core action inaccessible.
- `Major`: wrong platform model, broken important state, severe comprehension/input friction, or inaccessible major path.
- `Moderate`: hierarchy, readability, feedback, adaptation, or consistency is materially weakened.
- `Minor`: low-impact polish or edge-state issue.

Severity reflects impact and reach, not how emphatically a third-party rule is worded.

## Finding schema

Report:

- `ID`: stable identifier retained through fix and retest
- `Finding`: observable/reproducible issue and location/state
- `Severity`: Critical, Major, Moderate, Minor
- `Evidence`: one or more labels
- `Source`: primary URL/section, retrieval date, wording strength and conditions, or test/audit rule; write `Heuristic` when appropriate
- `Impact`: concrete consequence
- `Fix`: specific design/code change
- `Verify`: device/window, OS, appearance, input, assistive technology, test, or screenshot proving the fix

Group audit results as `confirmed`, `contextual`, or `false positive`. Keep unverified areas in a separate coverage section, not as invented defects.

## Comparison guardrails

Hold viewport/window, OS, data, appearance, text size, and state constant for before/after comparison. Re-score only re-verified dimensions. Cite current primary sources beside authoritative claims and retain conditional language.

Track fixes and coverage with [review-record-template.md](review-record-template.md). Keep `fixed-pending-verification` separate from `verified-fixed`; preserve pre-existing failures and record changed conditions in comparisons.
