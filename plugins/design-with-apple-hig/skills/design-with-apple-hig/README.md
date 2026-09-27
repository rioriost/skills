<div align="center">
  <img src="assets/mark.svg" width="112" alt="Apple HIG Design Skill mark">
  <h1>Apple HIG Design Skill</h1>
  <p><code>design-with-apple-hig</code></p>
  <p>An evidence-first Codex skill for designing, implementing, reviewing, and auditing Apple-platform interfaces.</p>

  [![Validate](https://github.com/rioriost/design-with-apple-hig/actions/workflows/validate.yml/badge.svg)](https://github.com/rioriost/design-with-apple-hig/actions/workflows/validate.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg)](LICENSE)

  [日本語](README.ja.md)
</div>

Fork of [Sunwood-ai-labs/design-with-apple-hig](https://github.com/Sunwood-ai-labs/design-with-apple-hig), preserving its evidence-first architecture and MIT license. This fork adds version/freshness checks, separate policy evidence, platform validation probes, reusable review records, and tested source extraction.

## ✨ Overview

`design-with-apple-hig` coordinates current Apple primary guidance, framework facts, accessibility evidence, rendered observations, specialist heuristics, and static audit signals without treating them as equally authoritative.

It supports:

- iOS, iPadOS, macOS, watchOS, tvOS, and visionOS
- SwiftUI, UIKit, and AppKit implementation work
- design, build, review, scoring, refactoring, and audit workflows
- Dynamic Type, VoiceOver, semantic colors, adaptive layouts, Reduce Motion, and representative UI states
- Apple-inspired Web and cross-platform work while preserving host-platform conventions

## 🧭 Why this skill exists

Many community HIG skills mix official requirements, old snapshots, personal heuristics, fixed numbers, and cross-platform generalizations. This skill uses a stricter model:

1. Current Apple HIG and official design resources arbitrate Apple design claims.
2. Current SDK documentation arbitrates API and framework behavior.
3. Accessibility standards and platform features support accessibility claims.
4. Third-party skills are narrow specialists, not authorities.
5. Static audit results are evidence to inspect, not proof of HIG compliance.

## 🚀 Install

Clone the repository into your Codex skills directory. On macOS/Linux:

```bash
git clone https://github.com/rioriost/design-with-apple-hig.git "${CODEX_HOME:-$HOME/.codex}/skills/design-with-apple-hig"
```

On Windows:

```powershell
git clone https://github.com/rioriost/design-with-apple-hig.git "$env:USERPROFILE\.codex\skills\design-with-apple-hig"
```

If a skill with this name is already installed, inspect that checkout before replacing it. The repository also works as a reference without installation.

## 💬 Use

Invoke the skill explicitly:

```text
Use $design-with-apple-hig to review and refactor this SwiftUI screen.
```

For an evidence-separated review:

```text
Use $design-with-apple-hig to review this interface. Separate Apple guidance,
framework facts, accessibility evidence, visible observations, audit signals,
and heuristics. Score only verified dimensions.
```

## 🏗️ Architecture

```text
SKILL.md
├── classify task, platform, framework, artifact, and input model
├── retrieve the smallest current primary-source bundle
├── preserve source scope and wording strength
├── route only relevant specialist capabilities
└── verify implementation, rendering, accessibility, and findings

references/
├── official-source-map.md   Apple primary-source routing
├── source-routing.md        authority and conflict resolution
├── freshness.md             release channels, source dates and drift
├── codex-workflows.md       design review versus implementation review
├── platform-routing.md      Apple-native, Web, and cross-platform boundaries
├── review-rubric.md         evidence-based severity and scoring
├── verification-loop.md     build, render, interaction, and re-test loop
├── review-record-template.md source ledger, findings and validation results
├── regression-scenarios.md  behavioral evaluation cases for maintainers
└── bibliography.md          historical source audits and incorporation policy
```

## 🔎 Evidence model

Material recommendations are separated into these classes:

| Evidence | Meaning |
| --- | --- |
| `APPLE-HIG` | Current scoped Apple design guidance |
| `APPLE-SDK` | Documented API contracts and availability |
| `APPLE-POLICY` | App Review or program/distribution rules, with applicability |
| `APPLE-RESOURCE` | Official design kit or asset guidance |
| `ACCESSIBILITY` | Supported by an applicable accessibility standard or feature |
| `OBSERVATION` | Visible in supplied code, screenshots, prototypes, or a running UI |
| `AUDIT` | Reported by a static analyzer and still requiring contextual review |
| `HEURISTIC` | A reasoned design recommendation, not an Apple requirement |

## ✅ Validate

Python 3.10+ is required; the helper and tests use only the standard library. Run from the repository root:

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/fetch_apple_hig.py scripts/validate_repository.py
```

Read a current official HIG topic through Apple's DocC JSON fallback:

```bash
python3 scripts/fetch_apple_hig.py materials --metadata-only
```

GitHub Actions runs structural/local-link validation, compilation, CLI smoke checks, and offline regression tests on Python 3.10, 3.12, and 3.13 for main pushes and pull requests. Tests cover extraction, scope boundaries, drift metadata, retrieval failures, and broken local references without network access. They do not establish Apple source freshness or agent behavior. Use [behavioral scenarios](references/regression-scenarios.md) for skill evaluation.

## Live documentation and review evidence

Bundled references are original routing/workflow guidance, not a HIG snapshot. Fetch live Apple pages for material design claims, exact numbers, wording, API availability, release channels and applicable App Review policy. Reuse a scoped source ledger within a task unless evidence changes; offline work must disclose freshness limits. See [freshness.md](references/freshness.md).

The reader can compare `--metadata-only` JSON against a previous task-local file with `--compare-metadata PATH`. It records retrieval time, Apple alert metadata when present, a payload digest and extraction warnings. A changed digest requires inspection; an unchanged digest does not certify correctness, current OS coverage or complete extraction. Read actual content before citing a claim, and inspect the official page for media or complex tables.

Use [Codex workflows](references/codex-workflows.md) to choose design or implementation review, and the [review record](references/review-record-template.md) for source ledgers, stable finding IDs, screenshots and explicit check outcomes. Build, rendered UI, automated accessibility audits, actual VoiceOver use, keyboard/focus and Reduce Motion are separate evidence. Unavailable device or accessibility checks remain visible gaps.

## 📚 Sources and provenance

The skill includes an audited [bibliography](references/bibliography.md) covering Apple primary sources and the community skills or tools that informed limited specialist roles. Third-party HIG corpora and Apple documentation are linked rather than copied.

See the [official source map](references/official-source-map.md) for runtime routing. Exact values, current APIs, OS-specific behavior, and normative claims must be rechecked against current Apple sources when the skill runs.

## ⚖️ License

Original project code and documentation are available under the [MIT License](LICENSE). Linked Apple materials, trademarks, design resources, and third-party projects remain subject to their respective terms and licenses.

## ℹ️ Disclaimer

This is an independent community project. It is not affiliated with, endorsed by, or sponsored by Apple Inc. “Apple,” platform names, and related marks are trademarks of Apple Inc. A review produced by this skill is evidence-backed guidance, not an Apple certification.
