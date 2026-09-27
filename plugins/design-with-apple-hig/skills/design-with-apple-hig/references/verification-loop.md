# Verification loop

Use this file after implementation or when reviewing a runnable artifact. Match effort to risk and report omitted checks with their confidence impact. Use [review-record-template.md](review-record-template.md) for substantial reviews; every check is pass, fail, blocked, not-run, or not-applicable with evidence or a reason. A screenshot review can finish with runtime checks not-run; it cannot claim runtime validation.

## 1. Establish baseline and evidence

- Record revision, platform, OS and SDK range, framework, build configuration, representative device/window, input, appearance, locale, text size, data, and state. Use [freshness.md](freshness.md) to separate current release information from the actual tested environment.
- Preserve pre-existing failures and unrelated user changes.
- Capture equivalent pre-change rendering or behavior when comparison matters.
- Retrieve current HIG pages for disputed or exact claims. Record URLs and dates.
- Run static audit before edits when available and relevant; keep raw versioned output.

When Apple HTML extraction fails, use:

```bash
python scripts/fetch_apple_hig.py <topic-slug> --metadata-only
python scripts/fetch_apple_hig.py <topic-slug>
```

Do not save the fetched page as a bundled corpus.

## 2. Run repository-native checks

Use existing formatter, linter, type checker, unit tests, UI/snapshot tests, and target-platform build. Prefer project-pinned commands and versions. Inspect existing CI and project instructions before inventing commands.

If a command cannot run, report the command, concise reason, and affected coverage. Compilation establishes buildability, not design quality. Record the exact command, toolchain, target/scheme, destination, exit result, and log location. Use a discovered simulator/device destination, not an invented model/OS. Respect project signing settings; report signing or missing-SDK blockers without changing credentials or deployment targets merely to force a pass.

## 3. Render representative states

Select risk-based states from the platform matrix:

- Compact/regular or minimum/normal/maximum window
- Light/Dark, normal/increased contrast, reduced transparency where applicable
- Default and large accessibility text; long localization and RTL if relevant
- Standard and Reduced Motion
- Loading, populated, empty, error, offline, and partial success
- Focused, selected, disabled, pressed, validation, and destructive states

Inspect hierarchy, clipping, overlap, unintended scrolling, safe areas, target separation, focus visibility, material contrast, density, and state continuity. A screenshot-only input leaves runtime dimensions unverified. Open and inspect the captured images; generating screenshot files is not visual review. Link before/after images to revision and configuration. If no rendering environment is available, mark visual verification blocked and give the precise state to capture later; do not claim a visual fix from code alone.

## 4. Test interaction and accessibility

Verify as applicable:

- Semantic role, accessible name, value, state, actions, hints, and announcements
- Focus and reading order
- Completion using keyboard, remote, pointer, Crown, eyes/hands, touch, voice, or switch alternatives
- Text scaling without loss of content or action
- Contrast and non-color state cues
- Reduce Motion, Reduce Transparency, Increase Contrast, Bold Text, and Differentiate Without Color behavior supported by the platform
- Validation, progress, cancel, interruption, error recovery, and partial failure
- Destructive confirmation, undo, or recovery
- Permission requests in a context that explains value without coercion

Use Accessibility Inspector and real assistive technology when available. Consult current [Apple accessibility testing documentation](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app) and check SDK/destination support before adding automated audits. Do not infer VoiceOver behavior from modifiers or labels alone.

### Distinguish four kinds of accessibility evidence

- **Source inspection:** intended roles, labels, values, grouping, adjustable/custom actions and scaling logic. This does not establish the runtime tree.
- **Runtime tree / Inspector / automated audit:** the semantics and detectable issues in the tested state. A clean audit does not establish reading experience or task completion.
- **Visual text/contrast testing:** actual rendered adaptation under the recorded settings. Pixel measurements alone may be insufficient for translucent or moving backgrounds.
- **Assistive-technology task execution:** actual navigation, speech/announcements and activation with VoiceOver or the relevant alternative. Record device/OS, mode, flow, expected versus observed behavior and limits.

For VoiceOver, traverse the core flow in reading order; check useful names/roles/values, grouping, custom or adjustable actions, state announcements, modal focus and return to the trigger. If VoiceOver is unavailable, mark this check blocked or not-run and specify the manual flow. Do not use an automated audit pass as a substitute.

### Text scaling

For platforms supporting Dynamic Type, render default and representative large accessibility sizes, including the largest supported size when material to the flow. Record the actual content-size category. Check wrapped text, truncation, control height, scrolling, focus visibility, and whether the primary action remains reachable. Re-run the task, not only a screenshot. On platforms/frameworks with different text-size behavior, test the supported equivalent and state why Dynamic Type categories are not applicable. Test long localization or RTL when the affected layout warrants it.

### Keyboard and focus

Where supported, complete the core flow using keyboard navigation under recorded system settings. Check forward/backward traversal, visible focus, activation, standard shortcuts, default/cancel behavior, traps, and focus return after dismissing a sheet, closing a window, or completing a destructive action. Distinguish keyboard focus from VoiceOver reading order. For watchOS/tvOS/visionOS, use the supported Crown/remote/spatial input and assistive alternatives; do not impose desktop Tab behavior on every platform.

### Reduced motion

Run the same transition with Reduce Motion off and on (or the host equivalent). Observe a recording or live transition: verify reduced nonessential motion, clear state changes, equal access to information and actions, and completion/cancellation without dependence on animation callbacks. Inspect loading, navigation and interruption, not just an isolated animation. A static screenshot or a read of the preference in source cannot establish this result. Exact motion timings remain heuristics unless scoped current Apple evidence specifies them.

## 5. Use HIG Doctor as a bounded analyzer

Prefer the project-pinned package. Otherwise, when network execution is authorized and useful:

```bash
npx -y hig-doctor <project-or-file> --stdout
```

At the 2026-08-01 audit baseline, HIG Doctor advertised 431 rules but its bundled HIG content was a frozen 2025-02-02 snapshot. Confirm the installed version and source date; do not present scan results as current HIG certification.

Use `--json` or SARIF for structured follow-up, baselines for new-issue gates, and `--fail-on` only under project policy. For each finding, retain tool version, rule ID, engine, and location, then classify:

- `confirmed`: source/runtime evidence supports an actionable issue
- `contextual`: validity depends on product, platform, or code context
- `false positive`: analyzer assumption does not apply

Watch for code-quality opinions labeled as HIG concerns, regex matches without semantic context, valid brand colors, intentional custom fonts, justified safe-area backgrounds, and framework/version changes. Use `--fix` only for authorized implementation; inspect every diff and rerun affected checks.

## 6. Re-verify

1. Re-run every failed or affected check.
2. Re-render the same window, OS, data, appearance, text size, and state.
3. Re-test Critical and Major paths first.
4. Check for regressions across another relevant platform, state, or input.
5. Re-fetch primary evidence if the fix depends on a disputed or current API.
6. Re-score only verified dimensions.
7. List untested platforms, OS versions, devices, inputs, states, and accessibility modes.
8. Preserve stable finding IDs and record whether each fix is verified or pending runtime verification. Add a focused regression test to the existing suite when it protects meaningful behavior; avoid brittle tests that merely mirror the implementation or require an unrelated framework.

## Completion standard

Call the task complete only when requested changes are implemented, proportionate project checks pass, runtime or rendered evidence supports UI claims, authoritative claims link to current sources, and remaining limits are explicit. A clean scan, successful build, or attractive screenshot alone does not establish HIG alignment or ship readiness.
