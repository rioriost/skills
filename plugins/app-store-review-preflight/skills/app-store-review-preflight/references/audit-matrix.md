# Full-scope audit matrix

This matrix routes the audit. Confirm current numbering and wording against Apple's live App Review Guidelines before reporting.

## Global pre-submit checks

| Topic | Evidence to inspect | Typical result when missing |
|---|---|---|
| Stability and completeness | Device test, crashes, placeholders, functional URLs/backends | BLOCKER |
| Review access | Demo account/mode, credentials, QR codes, hardware, server availability | BLOCKER |
| Review notes | Non-obvious features, purchases, setup, region differences | WARNING/BLOCKER |
| Metadata accuracy | Name, description, screenshots, previews, privacy, pricing | BLOCKER |
| Contact and support | Review contact, support URL, privacy policy | BLOCKER |
| Build identity | Platform, version, build, bundle ID, selected binary | BLOCKER |

## 1. Safety

| Area | Apply when | Inspect |
|---|---|---|
| 1.1 Objectionable content | App displays, generates, or links to user-facing content | Violence, hate, sexual content, harassment, illegal content, moderation boundaries |
| 1.2 User-generated content | Posting, chat, comments, profiles, shared media, creator content | Filtering, reporting, blocking, contact path, timely moderation, terms |
| 1.3 Kids | Kids category or children are a target audience | Age band, parental gates, ads/analytics, external links, data collection |
| 1.4 Physical harm | Medical, health, fitness, dosing, diagnosis, hardware control, dangerous activity | Evidence, disclaimers, measurement claims, emergency limitations, regulatory status |
| 1.5 Developer information | Every app | Accurate support/contact identity and reachable support |
| 1.6 Data security | Accounts, personal or sensitive data, networking, cloud storage | Transport, storage, authentication, access control, breach-prone behavior |

## 2. Performance

| Area | Apply when | Inspect |
|---|---|---|
| 2.1 App completeness | Every submission | Final build, test results, live backend, credentials/demo mode, complete IAPs |
| 2.2 Beta testing | App is a demo, beta, trial, or unfinished service | Use TestFlight; remove beta/placeholder behavior from production submission |
| 2.3 Accurate metadata | Every submission | Core experience, screenshots, previews, hidden/dormant features, purchase disclosures |
| 2.4 Hardware compatibility | Device-specific features or external hardware | Supported devices, resource use, hardware demonstration, graceful failure |
| 2.5 Software requirements | Every submission | Public APIs, background modes, IPv6/networking, self-contained bundle, sandbox/entitlements, downloaded code |

## 3. Business

| Area | Apply when | Inspect |
|---|---|---|
| 3.1.1 In-App Purchase | Digital features/content/currency/subscriptions unlock in the app | StoreKit, product visibility, restoration, metadata, first-IAP association, purchase disclosure |
| 3.1.2 Subscriptions | Recurring access | Ongoing value, period/price, trial terms, cancellation, subscription group, review notes |
| 3.1.3 Other purchase methods | Reader, multiplatform, enterprise, person-to-person, physical goods/services | Current eligibility and regional storefront rules; do not generalize exceptions |
| 3.2 Other business issues | Ads, lead generation, insurance, finance, crypto, gifts, raffles | Business model clarity, prohibited manipulation, licenses, ad behavior, regional restrictions |

## 4. Design

| Area | Apply when | Inspect |
|---|---|---|
| 4.1 Copycats | Similar branding, UI, name, icon, or service | Originality, authorization, misleading association |
| 4.2 Minimum functionality | Thin client, website wrapper, catalog, link collection, single-purpose content | Native/app-like utility and lasting value |
| 4.3 Spam | Templates, many similar apps, saturated category | Differentiation, duplicate bundle IDs, repeated submissions |
| Extensions and embedded experiences | Extensions, widgets, keyboards, mini apps/games, plug-ins, emulators, chatbots | Host-app utility, privacy, moderation, downloaded content/code rules |
| Apple sites and services | Apple Music, Maps, Wallet, Apple Pay, Game Center, system UI or marks | API/brand rules and faithful platform behavior |
| Alternate icons and platform UI | Alternate icons or system-like behavior | User choice, accurate appearance, no deceptive system impersonation |

## 5. Legal

| Area | Apply when | Inspect |
|---|---|---|
| 5.1 Privacy | Every app | Privacy policy, minimization, consent, purpose strings, tracking, SDKs, disclosure consistency, account deletion |
| 5.2 Intellectual property | Third-party content, trademarks, APIs, hardware, media, scraping | Ownership/license, service terms, content rights declaration, metadata and UI references |
| 5.3 Gaming/gambling/lotteries | Contests, sweepstakes, real-money gaming, lottery, loot mechanics | Official rules, licenses, geofencing, age restrictions, Apple non-sponsorship disclosure |
| 5.4 VPN | VPN service | Approved APIs, organization/account requirements, data-use limitations, local law |
| 5.5 Device management | MDM or configuration profiles | Eligible organization, declared purpose, data handling, user disclosure |
| 5.6 Developer conduct | Every submission and communication | Honest metadata, respectful communication, no manipulation, fraud, review gaming, or forced data sharing |

## Cross-evidence consistency

Always compare:

- App behavior versus screenshots and description.
- Source/bundle permissions versus purpose strings and privacy answers.
- SDK behavior versus Privacy Manifest and App Privacy declarations.
- Product identifiers and purchase UI versus IAPs included in the submission.
- Login/account behavior versus demo access and account-deletion support.
- Third-party content/brands versus content-rights answers and authorization evidence.
- External hardware requirements versus Review Notes and attached video.
- Region availability versus export, trader, licensing, and regulated-service declarations.

An inconsistency is at least a `WARNING`; make it a `BLOCKER` when it prevents review access, violates a clear requirement, or makes required metadata false.
