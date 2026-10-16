# EEON 3.11.0 (172) — available in TestFlight

Apple readback on October16,2026 at16:33:40Z confirms build172 VALID, train3.11.0IOS, internalBuildState IN_BETA_TESTING. Existing internal Beta group hasAccessToAllBuilds=true. External beta submission was not requested; externalBuildState is READY_FOR_BETA_SUBMISSION. No App Store review was submitted; live iOS3.10.0 remains READY_FOR_SALE.

## Exact release
- Source: abfdd41a425acf668ef6c3417a472bd1a625a69e on clean pushed main, containing prior appstore/voice-notes/3.10.0-build171 source6f7d7ed.
- Central Fastlane source:77e0572. Canonical beta exited0; upload completed16:30:38Z. Apple indexed build26f26007-ba7a-49db-b7cd-51c8d83822f9.
- IPA SHA256:1dcc0b210b1d9891651fb2bec7641dc7e0f7124ffa9f5fd557a0c3b308fdceef.
- All4 signed bundles are3.11.0/172: main app, Watch, widget and share extension. Strict code signatures pass, get-task-allow=false; main has Production CloudKit and resolved refresh token, Watch has background audio and correct companion ID. The compiled main binary contains the daily_tasks classifier marker. These prove packaging, not spoken-flow or wrist-down behavior.

## Proof files
- apple-preflight.json: prior live3.10.0/build171 and absent Watch registration.
- apple-build172.json: actual Apple processing and internal beta state.
- signed-ipa-proof.json and independent-ipa-receipt.json: separate audits of the exact IPA.
- independent-asc-receipt.json and independent-release-receipt.md: fresh Apple confirmation at16:34:42Z.
- upload-result.json: canonical Fastlane result and source/hash mapping.
- extension-verifier-proof.json: old verifier rejects a real signed extension; bounded PlugIns lookup passes. Independent recheck also passed.

## What changed in release tooling
The beta lane requires precommitted EEON version/build, checks clean main against fresh origin and prior release ancestry before/after archive, registers/reuses Watch signing, and verifies the exact IPA. Use `VOICE_NOTES_ROOT=<clean-main> fastlane beta app:voice-notes version:<new-version> build:<new-build>` after stamping/pushing all targets. The actual Apple beta relationship is `buildBetaDetail` (singular): use builds include=preReleaseVersion,buildBetaDetail. Listing a new TestFlight build does not require an App Store version draft.

## Platform finding and authorization
Unsandboxed checks showed iOS26.2/23C52 already registered, so no iOS reinstall was needed. Installed watchOS26.2/23S303 (3.89GB); both generic archive destinations then passed independent inspection. 48GiB remained after installation. CloudKit production schema matched every stored model field.

Shawn explicitly approved both main pushes and the TestFlight upload after automatic approval review asked for separate push authorization. Local simulator feature testing was waived by Shawn for testing in TestFlight. No production-data mutation, App Store submission, or external tester expansion occurred.

## Next real product proof
In TestFlight, install3.11.0(172), record an ordinary message listing several tasks plus one explicit future-date task. Check each task appears separately, Today excludes the future item, completion survives relaunch, and opted-in MCP get_note receives the updated stored checklist. Full speech/persistence/MCP flow and physical Watch behavior remain unverified here.
