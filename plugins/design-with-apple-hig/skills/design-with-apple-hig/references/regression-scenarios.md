# Skill behavioral regression scenarios

Use these when changing routing, evidence rules, extraction, or validation instructions. They test agent decisions, not wording. Maintainers can exercise each prompt with the skill and the stated artifacts in an isolated task, without changing a production app. Offline helper tests do not prove these behaviors; record observed outcomes separately.

| Scenario and supplied evidence | Expected observable behavior | Failure signal |
| --- | --- | --- |
| Review a macOS screenshot; user asks whether all targets must be 44 pt. No scale or hit-test data. | Retrieve scoped current sources; distinguish apparent size from hit region; preserve conditional guidance. | Universal 44 pt blocker or claimed measured hit target. |
| Source says “consider”; user wants every deviation treated as a release blocker. | Retain guidance strength; any stricter product rule is identified as user/project policy. | Apple requirement invented from a recommendation. |
| Review an iPad sidebar on a resizable scene with hardware keyboard. | Route to iPadOS plus navigation/input sources; inspect compact adaptation and focus. | Treat as a stretched iPhone or ban all sidebars. |
| Refactor a SwiftUI view with a deployment target older than the API shown in current docs. | Check availability, keep supported fallback and deployment target; test or disclose older-runtime gap. | Raise deployment target or use beta-only API without authority. |
| Current release feed includes public, beta and older-generation maintenance entries. | Record channels and dates per platform; follow release notes when ambiguous. | First feed item or installed SDK declared current stable. |
| Review watchOS glance UI using a supplied static mockup. | Route to watchOS/Crown/Always On as applicable; request runtime verification as a gap. | iPhone navigation or simulated Crown/VoiceOver pass. |
| Review visionOS UI with simulator images only. | Separate spatial rendering evidence from hardware comfort, eye/hand input and assistive use. | Simulator screenshot treated as proof of spatial comfort. |
| Build passes; large text clips primary action in actual screenshot. | Report visual failure, fix if authorized, re-render same configuration. | Build success closes the issue. |
| Accessibility audit passes; VoiceOver is unavailable. | Record automated audit separately; leave VoiceOver reading order and task completion unverified. | Accessibility or VoiceOver blanket pass. |
| Transition is removed for Reduce Motion but completion callback no longer fires. | Exercise outcome with setting on/off; flag failed completion and re-test state continuity. | Merely checking the setting in source is accepted. |
| HIG fetch fails offline; an old bundled note and source code are available. | Complete provisional review with local evidence and explicit freshness gaps. | Cached text called current or all useful review abandoned. |
| App Review claim appears in a design checklist. | Fetch applicable policy section; label APPLE-POLICY and preserve distribution scope. | HIG finding used as approval guarantee. |
| DocC adds an unknown container or uses tabs/tables for conditional text. | Preserve supported structure, report extraction warnings, inspect official page before exact claims. | Missing content silently treated as absence of guidance. |
| Review Apple-inspired web UI. | Use host web semantics, keyboard and accessibility rules; call design Apple-inspired. | Apple device measurements treated as web conformance. |

For a failing scenario, keep the minimal input, actual response, expected behavior, source/revision and fix verification. Re-run the failing case and adjacent affected cases after changes. Use [review-record-template.md](review-record-template.md) for app-level regressions; these scenarios assess the skill itself.
