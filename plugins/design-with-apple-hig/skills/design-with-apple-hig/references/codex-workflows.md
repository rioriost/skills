# Codex design and implementation reviews

Use only the mode requested. These workflows use repository files, ordinary build tools, and available browser/device tools; no named MCP, specialist skill, or simulator is required. Locate this skill's helpers from its installed directory. Follow project instructions and preserve unrelated edits.

## Design review (requirements, mockup, screenshot, prototype)

1. Identify the user's task, platform, target OS range, input, and artifact. Infer clear context; ask only for missing information that changes the result.
2. Read the applicable platform route and fetch the smallest relevant evidence bundle using [freshness.md](freshness.md).
3. Review task completion, hierarchy, platform conventions, readability, state communication, and apparent accessibility risks. Separate observations from hypotheses. Image pixels alone cannot establish a point-sized hit region without scale metadata, or any invisible tappable extension.
4. Use [review-rubric.md](review-rubric.md) for findings. Give each a stable ID, scoped source/strength, impact, proposed change, and verification method. Only score if requested. Leave runtime dimensions unverified.
5. Deliver a concise prioritized review and coverage limits. Review requests do not themselves authorize implementation or a redesign beyond the requested scope.

Example request:

```text
Use $design-with-apple-hig to review this iPad settings mockup for resizable
windows and keyboard use. Give evidence-backed findings and runtime checks
that remain unverified. Do not edit the app.
```

## Implementation review (code, diff, runnable app)

1. Read project instructions, working-tree status, the scoped diff, build/test configuration, deployment targets, and existing UI conventions. Record a baseline; do not overwrite unrelated work.
2. Trace changed states and controls. Check API availability against the selected SDK and minimum OS separately from the HIG rationale. A source-code label is intent, not verified VoiceOver output.
3. Capture existing rendering/runtime behavior when available. Use [verification-loop.md](verification-loop.md) and the relevant platform's validation probes. Static scans are optional supporting evidence.
4. For a review-only request, return findings and tests performed. For an authorized implementation/refactor request, make focused fixes, run proportionate checks, and inspect the resulting UI. A design contract can be a short paragraph for small changes.
5. Re-test the failing path and adjacent affected states, then report addressed IDs, remaining issues, source freshness, and verification limits. Do not claim runtime checks that tools or devices could not perform.

Example request:

```text
Use $design-with-apple-hig to review and fix this macOS preferences diff.
Preserve the deployment target and existing architecture. Verify build,
resizing, keyboard focus and accessibility where the environment permits;
report actual results and checks requiring a device or human tester.
```

## Evidence handoff

For substantial work, adapt [review-record-template.md](review-record-template.md) into the application's existing review/test documentation. For a small review, include the relevant fields inline instead. Keep screenshots/logs at project-appropriate paths, omit sensitive test data, and link artifacts to the revision tested. Do not introduce a new test framework solely to satisfy this template.

An unavailable check does not block all useful work: finish authorized edits and available verification, then state the concrete remaining check, environment, and acceptance criterion. Do not equate this handoff with complete validation or App Review approval. Publishing, submission, and distribution require authorization from the user's task; the skill grants none.
