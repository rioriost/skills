# Official Apple source map

Inherited research baseline: 2026-08-01, Asia/Tokyo. Historical examples below are discovery hints, not currently verified claims. Retrieve current pages using [freshness.md](freshness.md); this map does not declare a latest OS generation.

## Contents

- Entry points and updates
- Platform overviews
- Foundations
- Navigation, structure, and windows
- Controls and presentation
- Patterns and state
- Inputs and spatial interaction
- Technologies and branded assets
- DocC JSON fallback

## Entry points and updates

| Need | Official source |
| --- | --- |
| HIG index and current topic taxonomy | `https://developer.apple.com/design/human-interface-guidelines/` |
| Getting started and platform list | `https://developer.apple.com/design/human-interface-guidelines/getting-started` |
| Detailed design principles | `https://developer.apple.com/design/human-interface-guidelines/design-principles` |
| Current design resources and kits | `https://developer.apple.com/design/resources/` |
| Current design sessions | `https://developer.apple.com/videos/design/` |
| WWDC discovery; choose the relevant year/session | `https://developer.apple.com/wwdc/` |
| Public and prerelease OS/SDK announcements | `https://developer.apple.com/news/releases/` |
| Public OS release cross-check | `https://support.apple.com/en-us/100100` |
| Accessibility developer portal | `https://developer.apple.com/accessibility/` |
| Apple framework documentation | `https://developer.apple.com/documentation/` |
| App Review Guidelines | `https://developer.apple.com/app-store/review/guidelines/` |

At the research baseline, Apple listed iOS/iPadOS/macOS 27 design kits and described updated Liquid Glass components. The HIG landing page exposed hierarchy, harmony, and consistency as an immediate lens, while the detailed Design principles page described purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, and delight. Use both at their proper level; neither is a mechanical scorecard.

## Platform overviews

Retrieve exactly the platforms in scope:

- iOS: `designing-for-ios`
- iPadOS: `designing-for-ipados`
- macOS: `designing-for-macos`
- watchOS: `designing-for-watchos`
- tvOS: `designing-for-tvos`
- visionOS: `designing-for-visionos`
- Games: `designing-for-games`

Use the canonical form `https://developer.apple.com/design/human-interface-guidelines/<slug>`.

## Foundations

Start with only the affected topics:

- `accessibility`; add `voiceover` for reading order, labels, values, actions, and runtime behavior.
- `typography` for Dynamic Type, text styles, sizes, legibility, and scaling.
- `color` and `dark-mode` for semantic colors, appearance, contrast, and non-color cues.
- `layout` for safe areas, adaptation, readable regions, window/display contexts, and platform specifications.
- `materials` for Liquid Glass and standard materials. At the research baseline, Apple limited Liquid Glass to a functional controls/navigation layer, recommended sparse custom use, and reserved the clear variant for visually rich backgrounds.
- `motion` for purposeful motion and accessibility response.
- `inclusion`, `privacy`, `writing`, and `right-to-left` when people, data, copy, or localization are affected.
- `icons`, `sf-symbols`, `app-icons`, and `images` only for visual assets.

Accessibility guidance is distributed. Do not stop at the Accessibility overview when Typography, VoiceOver, Motion, Color, or a framework accessibility API owns the exact question.

## Navigation, structure, and windows

Route by actual component:

- `tab-bars`, `sidebars`, `navigation-bars`, `split-views`
- `toolbars`, `the-menu-bar`, `windows`
- `lists-and-tables`, `scroll-views`, `collections`
- `search-fields`, `searching`

Preserve platform sections. For example, the Sidebars page at the research baseline advises avoiding a sidebar on iOS while offering adaptive sidebar/tab-bar patterns on iPadOS; a generic “sidebar is Apple-like” rule loses the decision.

## Controls and presentation

Use the component page plus its framework API:

- `buttons`, `toggles`, `pickers`, `sliders`, `steppers`, `text-fields`
- `menus`, `context-menus`, `pop-up-buttons`
- `alerts`, `sheets`, `popovers`, `modality`
- `progress-indicators`, `status`, `feedback`

Do not detach measurements from context. At the research baseline, the Buttons page described a 44×44 pt hit region as a general rule (60×60 pt in visionOS), while accessibility and specialized control pages can provide different default/minimum or frequency-based guidance.

## Patterns and state

Retrieve based on the flow:

- `onboarding`, `launching`, `loading`, `feedback`, `offering-help`
- `entering-data`, `managing-accounts`, `managing-notifications`
- `drag-and-drop`, `undo-and-redo`, `file-management`
- `privacy` for permission timing and pre-alert constraints

Keep the nuance visible. At the research baseline, the Onboarding page asked for a fast, optional experience but specifies no universal three-page limit. The Privacy page at that baseline preferred contextual requests, permits launch-time requests when required and obvious, and recommends a custom pre-alert only when extra detail is essential.

## Inputs and spatial interaction

- `gestures`, `keyboards`, `pointing-devices`, `focus-and-selection`
- `remotes`, `game-controls`, `apple-pencil-and-scribble`
- `eyes`, `spatial-interactions`, and visionOS accessibility guidance for spatial work

Verify current input and hardware terminology; do not copy touch-only assumptions to iPadOS, macOS, tvOS, or visionOS.

## Technologies and branded assets

For Apple Pay, HealthKit, Sign in with Apple, Wallet, CarPlay, Activity rings, App Clips, or other branded technologies, use the specific HIG page, current developer documentation, and any linked identity guideline. These often contain real mandatory language and asset rules; do not weaken or generalize them.

Before distributing Design Resources, read the current agreement linked from Apple Design Resources. At the research baseline, Apple provided a limited license tied to creating mockups for software on Apple platforms; do not assume unrestricted redistribution.

## DocC JSON fallback

For a HIG slug `<slug>`, Apple publishes machine-readable content at:

`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`

Use `scripts/fetch_apple_hig.py` to retrieve and render this source. Record metadata such as supported platforms and alert/change information when present. Never cache its output inside this skill as a replacement corpus.

For implementation validation, start with [Performing accessibility testing for your app](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app) and follow current tool/API links. Verify the availability of automated accessibility audits in the selected SDK and test destination rather than assuming uniform platform support.
