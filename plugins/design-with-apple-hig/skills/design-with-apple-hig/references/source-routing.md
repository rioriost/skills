# Source and specialist routing

Use this file to assemble evidence without loading an entire HIG corpus or confusing discovery aids with authority.

## Build an evidence bundle

For a normal task, retrieve:

1. One current Apple platform overview.
2. One to four current HIG pages for the exact components, patterns, inputs, or foundations involved.
3. One current framework/API page when implementation behavior matters.
4. One focused accessibility page or standard when access is affected.
5. Establish relevant OS release channels using [freshness.md](freshness.md); add Design updates or WWDC for new-OS, beta, Liquid Glass, or changed-component decisions.

Expand only when evidence conflicts or the artifact spans multiple platforms. Record page title, URL, retrieval date, supported platforms, relevant section, and guidance strength. Use [review-record-template.md](review-record-template.md) for a reusable source ledger.

## Retrieve Apple HIG reliably

Prefer an official Apple page opened through Web search or browser tooling. Apple HIG HTML can require JavaScript; when text extraction fails, use the bundled DocC reader:

```bash
python scripts/fetch_apple_hig.py materials
python scripts/fetch_apple_hig.py accessibility --metadata-only
python scripts/fetch_apple_hig.py https://developer.apple.com/design/human-interface-guidelines/tab-bars --format json
```

The script accepts only Apple HIG slugs or matching `developer.apple.com` HIG URLs and reads Apple's official DocC JSON. Treat its output as retrieved source text, not as a local canonical snapshot. Re-run it for future tasks.

## Apply authority by claim type

| Claim | Primary authority | Do not substitute |
| --- | --- | --- |
| Design recommendation | Current platform/topic HIG page | Community checklist |
| API name, availability, behavior | Current Apple SDK docs and target SDK | Old sample code |
| New OS visual system | Current HIG, Design Resources, release notes, WWDC | Prior-year screenshot |
| App distribution or entitlement rule | App Review Guidelines or program docs | HIG paraphrase |
| Web accessibility conformance | Current W3C WCAG and Web platform docs | Apple mobile measurements |
| Observed UI behavior | Reproducible runtime test | Static analyzer inference |

Label distribution claims `APPLE-POLICY`, documented API claims `APPLE-SDK`, and runtime measurements `OBSERVATION`. Accessibility evidence can cite HIG, SDK, a standard, or a runtime test; retain that underlying authority rather than letting the label erase it.

Maintain Apple modal verbs. `Consider` is not a requirement. `Avoid` can have exceptions. `In general` is not universal. Copy exact numbers only with their scope. Preserve default versus minimum, visible size versus hit region, units, conditions and exceptions. “Must” is mandatory only within the cited source’s domain and applicability; project release gates and heuristics remain separately named.

Split mixed claims: a HIG preference for a system control, SDK availability for that control, and an observed clipping bug need separate evidence. A newer WWDC demonstration does not silently override an API availability contract or a distribution policy. If two current sources disagree, record both scopes and the unresolved conflict.

## Route third-party specialists

### Distilled HIG corpora

Use HIGAgentSkills or HIG Doctor references to discover topic names, related pages, and search terms. Do not load all foundations, cite a frozen snapshot as current, or copy its text. Re-fetch the matching Apple pages before using exact language, measurements, or APIs.

### Platform implementation packs

Use platform-design-skills for candidate code patterns and test ideas. Downgrade all unverified absolutes to hypotheses. Specifically re-check universal grids, thumb-zone mandates, blanket navigation bans, fixed page/tab counts, mandatory pre-permission screens, device-width inventories, and claims that every command needs a shortcut.

### Cross-framework review

Use dickwu/apple-design-skill for its context intake, selective 3–8-file loading, and framework vocabulary. Do not universalize Apple components or substitute Apple requirements for Android, Web, Flutter, Electron, or Tauri norms.

### Motion and direct manipulation

Use Emil Kowalski's apple-design skill for immediate feedback, 1:1 tracking, interruptibility, velocity continuity, and prototyping ideas. Treat numeric spring values, projection formulas, CSS material recipes, and generalized physical claims as implementation heuristics unless the current Apple source and target framework support them.

### Static audit

Use HIG Doctor only after understanding the project and preferably before edits:

```bash
npx -y hig-doctor <project-or-file> --stdout
```

Prefer a project-pinned version. Use JSON or SARIF for structured processing. Classify findings as `confirmed`, `contextual`, or `false positive`; note rules that are code-quality opinions rather than HIG requirements. Use `--fix` only for an authorized implementation task, review every diff, and re-run tests.

### Rendering and interaction

Use installed browser, Chrome, computer-use, or Playwright skills for visible and runtime evidence. Use frontend-design or site-building for Web implementation. This skill retains evidence arbitration and platform naming.

## Resolve conflict

1. Match platform, OS, component, state, and input scope.
2. Prefer current Apple primary guidance over third-party snapshots.
3. Prefer current SDK behavior over stale examples.
4. Preserve accessibility and system behavior over decorative imitation.
5. Keep qualitative guidance qualitative.
6. On non-Apple platforms, apply the host platform's normative sources first.
7. If current Apple sources disagree or remain ambiguous, report the ambiguity instead of manufacturing certainty.

## Control provenance and rights

Do not embed third-party HIG reference corpora. A repository's MIT or CC license may cover original structure and commentary without relicensing Apple text. Link to sources and keep substantial Apple content out of the skill. See [bibliography.md](bibliography.md) for the inspected sources and decisions.
