# Platform routing and design contract

Read only the platform sections in scope. Retrieve the linked HIG slug at task time; this file provides routing, not a substitute for current guidance.

## Contents

- Classify the product
- iOS, iPadOS, macOS, watchOS, tvOS, and visionOS
- Apple-inspired Web and cross-platform products
- Design contract
- Representative states

## Classify the product

Record:

- Task and intended outcome
- Apple-native, cross-platform, or Apple-inspired Web
- Platform, minimum OS, target SDK, framework, current public release and relevant beta, each with its own evidence from [freshness.md](freshness.md)
- Artifact: requirements, code, screenshot, prototype, or live app
- Inputs: touch, pointer, keyboard, remote, Digital Crown, eyes, hands, voice, or assistive technology
- Window/display contexts and representative states
- Evidence that can actually be collected

Apply two official lenses without collapsing them:

- Use the HIG landing lens — hierarchy, harmony, consistency — to assess content/chrome relationships and platform adaptation.
- Use the detailed Design principles — purpose, agency, responsibility, familiarity, flexibility, simplicity, craft, delight — to reason about tradeoffs and intent.

Neither lens creates automatic numeric requirements.

## iOS

Validation probes: exercise the main touch flow with keyboard shown/hidden, supported orientations and interruptions; render default and large accessibility Dynamic Type; verify VoiceOver names, order and actions in a running app. Record safe-area and keyboard occlusion at the tested device size.

Retrieve `designing-for-ios`, then the actual navigation, component, and pattern pages. Optimize for focused tasks, touch, safe areas, frequent interruption, Dynamic Type, VoiceOver, semantic colors, contextual permissions, and recovery.

As a historical routing example, Apple guidance describes controls in the middle or bottom of the display tend to be easier to reach; preserve `tends to`. Do not turn this into “every primary action must be at the bottom.” Consider content, keyboard, navigation, scrolling, handedness, and system placement.

Test compact and regular environments supported by the project rather than a hardcoded marketing-device list. Use a tab bar when its top-level navigation role fits; do not derive a universal hamburger-menu ban or fixed tab count without the current component context.

## iPadOS

Validation probes: resize through supported narrow and wide windows without losing selection or navigation state; exercise touch, pointer and external keyboard; inspect tab/sidebar adaptation, visible focus, shortcut discovery and focus restoration after sheets. Multiwindow and Pencil checks apply only when supported by the product.

Retrieve `designing-for-ipados` plus `multitasking`, `sidebars`, `tab-bars`, `split-views`, `keyboards`, and `pointing-devices` as applicable. Design for resizable scenes, multitasking, orientation, touch, keyboard, trackpad, Pencil, drag and drop, and multiple windows.

Do not stretch an iPhone layout. Let navigation adapt to width and information structure. Verify current convertible tab/sidebar behavior before specifying an API or appearance.

## macOS

Validation probes: exercise minimum/normal window sizes, menu commands and standard shortcuts, keyboard-only traversal, default/cancel actions, focus return after dialogs, and selection after window changes. Use the text-size/accessibility behavior actually supported by the app and OS; do not impose iOS Dynamic Type categories on AppKit. Record keyboard-navigation settings so a skipped control is interpreted in context.

Retrieve `designing-for-macos`, then `the-menu-bar`, `windows`, `toolbars`, `sidebars`, `keyboards`, `pointing-devices`, and `focus-and-selection` as needed. Support resizable windows, menu discoverability, precise input, keyboard-only work, focus, selection, density, state restoration, and multiwindow behavior appropriate to the product.

Apple asks apps to use the menu bar for commands and handle shortcuts that accelerate work. Do not infer that every action requires a custom shortcut or that every app must expose identical document menus. Preserve standard system commands and choose additional shortcuts by frequency, importance, conflict, and accessibility.

## watchOS

Validation probes: check small supported displays and large supported text, Digital Crown interaction where used, task resumption and interruption, and VoiceOver on an available runtime/device. Exercise Always On/privacy and complications only when in scope. Simulator results do not establish wrist readability, physical Crown feel or haptic quality.

Retrieve `designing-for-watchos` plus the exact complication, Live Activity, Always On, Crown, notification, or workout pages. Optimize for glanceability, short interactions, clear state, minimal entry, wrist context, and privacy when the display is visible to others.

Do not invent universal maximum hierarchy depth, tab count, or update interval from a third-party checklist. Verify the current API and use case.

## tvOS

Retrieve `designing-for-tvos`, `focus-and-selection`, `remotes`, and media/navigation topics in scope. Design for distance, remote input, predictable focus movement, strong focus visibility, readable scale, and recovery from focus loss.

Verify current remote terminology and behavior. Do not assume old Siri Remote button mappings or screen distances remain current.

## visionOS

Validation probes: test the actual window/volume/immersive presentation, focus feedback, supported input alternatives and transitions back to a recoverable state. Review supported text scaling and Reduce Motion. Simulator evidence covers only tested rendering/logic; eye/hand targeting, physical comfort, depth and assistive use requiring hardware remain unverified without that hardware.

Retrieve `designing-for-visionos`, `spatial-layout`, `spatial-interactions`, `eyes`, `accessibility`, and relevant immersive-experience pages. Prioritize comfort, safety, field of view, indirect input, depth, legibility, immersion control, and alternatives to eyes-and-hands input.

Treat “keep content in a comfortable field of view” as contextual spatial guidance, not a simplistic hemisphere rule. Verify current target sizes and framework behavior for each control and input mode.

## Apple-inspired Web

Use Web standards as normative: semantic HTML, keyboard operation, visible focus, zoom/reflow, WCAG, high contrast, Reduced Motion, and browser compatibility. Apply compatible Apple principles to hierarchy, feedback, direct manipulation, restraint, and polish.

- Do not use Apple mobile measurements as Web conformance thresholds.
- Do not represent CSS blur or glassmorphism as Liquid Glass implementation.
- Verify `prefers-*` media-query browser support before promising behavior.
- Use content-driven responsive constraints instead of copying iPhone widths.
- Check font and asset distribution rights.

Call the result Apple-inspired, never HIG-compliant.

## Cross-platform products

Share purpose, data model, domain logic, content terminology, and brand tokens. Create an explicit mapping for each platform's navigation, windows, commands, density, input, materials, and accessibility semantics. Use the host platform's primary guidance outside Apple platforms.

Do not translate an iOS tab bar into macOS, Android, or Web chrome merely to maintain pixel similarity.

## Build the design contract

Before substantial work, define:

- Purpose and core user outcome
- Information hierarchy and navigation model
- Primary, secondary, and destructive actions
- Input and focus model
- Density and adaptive behavior
- Light, Dark, contrast, and material behavior
- Accessibility semantics and text scaling
- Motion, interruption, and Reduced Motion
- Loading, populated, empty, error, offline, disabled, selected, and focused states
- Privacy, permission timing, data recovery, localization, and RTL

Revise the contract when evidence or testing disproves an assumption.

## Select representative states

Choose risk-based combinations instead of an impractical Cartesian product:

| Dimension | Representative states |
| --- | --- |
| Layout | compact/regular or minimum/normal/maximum window |
| Appearance | Light/Dark, normal/increased contrast, reduced transparency where supported |
| Text | default and large accessibility sizes; long localization and RTL where relevant |
| Motion | standard and Reduced Motion |
| Data | loading, populated, empty, error, offline, partial success |
| Control | focused, selected, disabled, pressed, validation error |
| Safety | destructive confirmation, undo, retry, and recovery |
| Input | primary input plus keyboard/assistive alternative where applicable |
