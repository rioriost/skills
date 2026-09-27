# Bibliography and source audit

This file records what informed the skill and which ideas were accepted. It is not runtime authority. Apple primary sources must still be retrieved for each material claim.

Audit date: 2026-08-01 (Asia/Tokyo).

## Apple primary sources

- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) — canonical topic index and current landing guidance.
- [Getting started](https://developer.apple.com/design/human-interface-guidelines/getting-started) — current platform-routing entry point.
- [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) — detailed purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, and delight framework; reintroduced June 8, 2026.
- [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) — current overview, audit guidance, supported accessibility features, and routing to Typography and VoiceOver.
- [Typography](https://developer.apple.com/design/human-interface-guidelines/typography) — legibility, system styles, Dynamic Type, and platform text guidance.
- [Layout](https://developer.apple.com/design/human-interface-guidelines/layout) — safe areas, adaptation, display contexts, and platform specifications.
- [Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — current Liquid Glass and standard-material roles, variants, accessibility adaptation, and linked APIs.
- [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) — system button behavior, styles, press state, and scoped hit-region guidance.
- [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) and [Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars) — current navigation roles and platform-specific adaptation.
- [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding) — fast, contextual, and optional learning without a fixed page-count rule.
- [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) — permission timing, purpose strings, and conditional pre-alert guidance.
- [Apple Design Resources](https://developer.apple.com/design/resources/) — current UI kits, SF Symbols, fonts, Icon Composer, templates, and linked resource terms.
- [WWDC26 Design guide](https://developer.apple.com/wwdc26/guides/design/) and [Principles of great design](https://developer.apple.com/videos/play/wwdc2026/250/) — current design updates and explanatory session.
- [Design kits for iOS, iPadOS, and macOS 27](https://developer.apple.com/news/?id=e2lxw9l1) — June 23, 2026 resource update.
- [Apple Design Resources License Agreement](https://developer.apple.com/support/downloads/terms/apple-design-resources/Apple-Design-Resources-License-20230621-English.pdf) — usage limits for official resources; verify the current linked agreement before distribution.

## Third-party skills and tools inspected

### HIGAgentSkills

- Repository: [justinwetch/HIGAgentSkills](https://github.com/justinwetch/HIGAgentSkills)
- Inspected commit: [`701151a7b39609b71a58d54de6d86e3500c0c316`](https://github.com/justinwetch/HIGAgentSkills/tree/701151a7b39609b71a58d54de6d86e3500c0c316), dated 2026-06-09.
- Inspected: `SKILL.md`, `README.md`, routing index, and samples from the 156-file distilled corpus.
- Accepted: topic taxonomy, keyword routing, one-hop related-topic expansion, and the discipline of retaining platform scope.
- Rejected: loading 16 foundations on every request; calling a distilled snapshot authoritative; treating exact snapshot values as current without primary verification; broad activation for unrelated digital interfaces.
- Rights note: no top-level license was present in the inspected commit. The repository states that it distills Apple HIG content. Do not copy or redistribute its corpus.

### HIG Doctor

- Repository: [raintree-technology/hig-doctor](https://github.com/raintree-technology/hig-doctor)
- Inspected commit: [`0fe0684f3d080c8572a8f9bc590b3e32ea378afb`](https://github.com/raintree-technology/hig-doctor/tree/0fe0684f3d080c8572a8f9bc590b3e32ea378afb), dated 2026-07-30.
- Inspected: 14 skill entry files, README, rule catalog, drift script, license, and representative references.
- Accepted: project-context intake, topical skill split, stable rule IDs, JSON/SARIF, baselines, suppressions, finding classification, and official DocC JSON drift detection.
- Rejected: using the frozen `2025-02-02` reference snapshot as current; describing regex/structural findings as HIG compliance; treating code-style signals such as all hardcoded values or state visibility as automatic UX violations.
- Rights note: MIT covers structure and tooling. The repository explicitly states that Apple HIG text in references remains Apple intellectual property.

### platform-design-skills

- Repository: [ehmo/platform-design-skills](https://github.com/ehmo/platform-design-skills)
- Inspected commit: [`dc2be825d8b439caea78e9eaa8fb3ac23b0ff3e9`](https://github.com/ehmo/platform-design-skills/tree/dc2be825d8b439caea78e9eaa8fb3ac23b0ff3e9), dated 2026-03-18.
- Inspected: README, license, all platform skill inventories, the full iOS rule structure, and absolute-language scans across Apple-platform files.
- Accepted: separate platform roles, concrete implementation examples, impact grouping, and checklist generation.
- Rejected as universal Apple requirements: mandatory 8-point grid; all primary actions in a thumb zone; blanket hamburger-menu prohibition; fixed screen-width inventory; three-page onboarding maximum; mandatory pre-permission screen; every menu action needing a shortcut; blanket modal, spinner, density, and tab-count rules.
- Official comparison: Apple uses context-sensitive wording such as “tends to,” “prefer,” “consider,” and platform sections. Current Onboarding has no three-page maximum, Privacy makes pre-alerts conditional, and Layout does not establish a universal 8-point grid.
- Rights note: repository code is MIT; its README says Apple HIG was scraped and includes a compiled HIG PDF. Do not copy bundled Apple material.

### apple-design-skill

- Repository: [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill)
- Inspected commit: [`d0bac1e765a27a696839e62962e36330ce72f0b7`](https://github.com/dickwu/apple-design-skill/tree/d0bac1e765a27a696839e62962e36330ce72f0b7), dated 2026-02-27.
- Inspected: `SKILL.md`, README, routing table, license statement, and representative references from its 54-file corpus.
- Accepted: context intake, loading only 3–8 relevant files, artifact-aware review, and framework vocabulary translation.
- Rejected: treating Apple-derived principles as universally equivalent across mobile and desktop; mapping Apple navigation directly to non-Apple hosts; fixed cross-platform target sizes; citing repackaged text as authoritative.
- Rights note: no standard top-level license was present. The README says the package derives and generalizes Apple HIG content. Do not copy the reference corpus.

### Emil Kowalski skills — apple-design

- Repository: [emilkowalski/skills](https://github.com/emilkowalski/skills)
- Inspected commit: [`70744e3816f1d93eafb697161a8b880a7384c5ff`](https://github.com/emilkowalski/skills/tree/70744e3816f1d93eafb697161a8b880a7384c5ff), dated 2026-07-27.
- Inspected: `skills/apple-design/SKILL.md` and MIT license.
- Accepted: immediate response, 1:1 tracking, interruptibility, velocity continuity, spatial consistency, Reduced Motion, and interactive prototyping as high-value design-engineering heuristics.
- Rejected as current HIG requirements: copied numeric spring presets, projection formulas, CSS recipes, material stacking rules, and universal physics claims. These are useful implementation starting points but require target-framework and browser verification.
- Rights note: repository content is MIT. Retain attribution when copying substantial original material; this skill references concepts without copying the source text.

### apple-hig-codex-skill

- Repository: [Ksanbal/apple-hig-codex-skill](https://github.com/Ksanbal/apple-hig-codex-skill)
- Inspected commit: [`8c3b0dd8de10cdd7d35b0dd55f7eeba92d64dc06`](https://github.com/Ksanbal/apple-hig-codex-skill/tree/8c3b0dd8de10cdd7d35b0dd55f7eeba92d64dc06), dated 2026-04-28.
- Inspected: plugin structure, single skill file, README, and CC BY 4.0 license.
- Accepted: portable plugin packaging, broad trigger vocabulary, native-first implementation checklist, cross-device adaptation, and explicit warning to consult current official docs.
- Revised: the HIG landing principles of hierarchy, harmony, and consistency remain useful, but the current detailed Design principles page adds eight decision principles; use both. Treat “one primary action,” “three-second clarity,” and thumb-reach checks as heuristics, not universal HIG requirements.
- Rights note: original material is CC BY 4.0 with attribution; Apple materials and trademarks remain Apple's.

## Incorporation policy

The refreshed skill incorporates procedures, routing ideas, and independently worded synthesis. It does not include third-party HIG corpora, Apple page copies, rule files, code examples, motion tables, or branded assets. When a third-party idea materially affects an answer, cite the primary Apple source for Apple claims and label remaining advice as `HEURISTIC` or `AUDIT`.
