# EEON 3.11.1 (173) — submitted October 21, 2026

Apple readback at **14:18:03 UTC** confirms **WAITING_FOR_REVIEW**, exact build **173** attached, **MANUAL** release. Submission `03326f9e-8660-4dcb-b967-3bc07c2c2253` was submitted at 14:16:33 UTC. Existing 3.11.0 (172) remains READY_FOR_SALE. No public release performed.

Shawn approved App Store submission and both main merges: EEON PR3 and fastlane-configs PR2. Archive source `91b7515` includes both prior live-store sources (3.10.0/171 tag and `abfdd41` for 3.11.0/172). Central Fastlane source `4f49c5c` contains the matching release notes. Later EEON commits add documentation, evidence and read-only inventory only; app/project source is unchanged from the archive.

## Observed proof

- Canonical beta job `voice_notes-beta-20261021-085707-swgb` passed in 853.6 seconds. Production CloudKit/schema/source and exact-IPA guards passed; archive/export/upload completed. See [upload record](uploaded-artifact.json) for exact IPA SHA256 and source SHA.
- [Independent actual IPA inspection](independent-artifact.json): iPhone, Watch, widget and share extension all 3.11.1/173; ZIP integrity, all 1,557 code-page hashes and embedded entitlement hashes match. Production CloudKit, Apple sign-in, app group and Watch audio prerequisites present. This portable inspection does not claim independent CMS certificate-trust validation or physical-device behavior.
- Metadata job `voice_notes-apple_metadata-20261021-091248-wuwk` passed with exact Apple readback of all nine listing fields.
- All 16 screenshot filenames, checksums and sequence within each display type match live 3.11.0; all COMPLETE, including the Watch screenshot. Both subscriptions APPROVED. All 175 returned download-price rows Free.
- Canonical submission job `voice_notes-release-20261021-091544-iglk` passed. No active review was canceled. Approved subscriptions already had no pending version; their expected no-op responses did not prevent app submission.
- [Fresh Apple response](apple-after-submit.json) and [independent final checks](independent-apple-final.json) establish the final state. All 16 independent final checks passed.

## Product scope and limits

This release contains the stable photo-picker presenter and immediate project-assignment persistence. Add Photo attachment/persistence and ten other menu journeys were previously exercised in Simulator. Tag removal and restore completion remain unverified because the last focused run stopped at simulator startup. No new UI retry or physical-iPhone test was performed in this release session. The owner's original note was not modified.

## Canonical next release

Use committed Mac-run actions: `apple_preflight` → `beta` → `apple_metadata` → `release`. The wrapper derives committed version/build, requires clean current main and prior source ancestry, and reuses the central Fastlane pipeline. Preflight inventories Apple build/review/subscription/pricing and current/live screenshots; review its actual receipt before submission. Never infer API success from the underlying Milepost client exit code; its receipt.ok and freshness are checked explicitly.

A target must have the exact VALID iOS build, editable version, correct metadata, complete retained assets, and no active review. Preserve manual release. Native actions retain normal runner approval/resource gates. Do not repeat beta for an already uploaded build.

Next: Apple review decision. The Otter benchmark is [here](../aso/2026-10-21-otter-benchmark.md); it is a recommendation, with no new product features implemented.
