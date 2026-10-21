# Build brief native proof — in progress

User-approved scope: built-in Build brief preset, editable source-linked preview, explicit save/copy handoff, and standing real end-to-end coverage. Preserve the original transcript and enhanced note; keep the existing Pro generation gate. No Apple release authorized for this feature.

## Current evidence (2026-10-21)

- Feature branch `codex/eeon-build-brief` starts at main `9e3ba51a03596fe1aac9e95baf664548ff8b4409`.
- Test-first source `1ae0d81465a52102d0a7e93a235be20e1fd31a7d` adds two actual XCTest flows and `mac-run 'voice notes' e2e_build_brief` using the existing signed disposable-simulator pipeline.
- Tests cover generation, the five sections and source facts, exact source viewing, editing, save/relaunch, reopening from More formats, cancel, real foreground clipboard paste, unchanged original note, and the Pro gate. They are written but **zero tests have run**. This is not a failing feature reproduction or a passing proof.
- Baseline job `voice_notes-e2e_build_brief-20261021-103104-umnh` failed 10:34:16 CDT after188.7s. `simctl bootstatus` exceeded120s. No app build, API request or UI test occurred. Both runtimes were available (iOS26.3.1, watchOS26.2),27.4GiB free, no pre-existing booted device. Root cause remains unverified.
- Runner cleanup completed; the disposable device directory `EEAF1607-D3F4-43DD-826E-46A4F76056CA` is absent. No retry or resource-policy override. No feature implementation yet.

## Superseded stop / current authorization

At18:18CDT Shawn instructed: “just push to apple and i'll test on test flight.” Proceed with implementation and signed TestFlight3.11.2/174 through the existing beta pipeline. Simulator proof is waived for this candidate. Preserve the earlier zero-test failure as evidence; do not describe the new UI as E2E-proven. The older App Review submission remains3.11.1/173.

## Historical resume instruction

Rule3 requires authorization to diagnose/repair startup and resume after this infrastructure failure; requested in the chat. Do not confuse the new feature proof with the exhausted older menu-test allowances. Once startup is repaired, run this test against the missing feature and observe the real expected failure before implementation. Then implement using the existing template compiler/RewriteService and note storage, run green with a real model response, independently inspect the actual SwiftData store and clipboard receipt, and request a fresh refuter before claiming it works. Preserve physical-device/CloudKit limits honestly.
