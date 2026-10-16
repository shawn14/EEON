# Independent EEON release check — 2026-10-16

PASS for upload and internal TestFlight availability. Independent live Apple GET at 2026-10-16T16:34:42Z returned build 172 (26f26007-ba7a-49db-b7cd-51c8d83822f9), processing VALID, iOS prerelease version 3.11.0, internalBuildState IN_BETA_TESTING. Internal Beta group grants access to all builds. Its embedded builds listing is capped and was not treated as direct proof of 172; the build's own beta state is direct evidence. External state is READY_FOR_BETA_SUBMISSION, not external tester availability. iOS 3.10.0 remains READY_FOR_SALE. Minimum iOS version is 26.2.

Exact uploaded IPA SHA256: 1dcc0b210b1d9891651fb2bec7641dc7e0f7124ffa9f5fd557a0c3b308fdceef.

All four extracted bundles (main app, share, widget, Watch) independently passed codesign --verify --deep --strict and show 3.11.0 (172), get-task-allow=false, unexpired App Store distribution profiles with no device list. Main signing authority is Apple Distribution: Stock Alarm, LLC (BYRK5RUS4U), rooted in Apple Root CA; signed 2026-10-16 11:29:38 America/Chicago. Main CloudKit entitlement is Production. Watch UIBackgroundModes contains audio and its companion ID matches the main bundle. The daily_tasks marker is present in the signed main executable.

Fastlane log ends with successful upload at 11:30:38 America/Chicago. This check proves the artifact and Apple internal release state, not spoken-task runtime behavior, CloudKit sync, or Watch background behavior on a device. No repository or Apple writes were performed. Independent extraction was deleted after inspection; JSON receipts retained for the parent session.
