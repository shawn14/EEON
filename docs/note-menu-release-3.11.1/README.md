# EEON 3.11.1 (173) release in progress

Shawn requested another Apple push on October 21 and explicitly selected App Store review. Scope: photo-picker presentation and immediate project-assignment persistence, already proved in Simulator. Tag removal and restore completion remain unverified because the last focused run stopped at simulator startup. No new native UI attempt is implied by this release.

Apple read-only preflight at 13:49 UTC: 3.11.0 (172) READY_FOR_SALE, build VALID, prior review COMPLETE, both subscriptions APPROVED. Preparing 3.11.1 (173); no upload or submission yet.

Canonical phases, all through the Mac runner:

- `mac-run 'voice notes' apple_preflight`: read Apple state using the existing Milepost ASC client; validate its actual receipt because that client can exit zero on an API failure.
- `mac-run 'voice notes' beta`: require clean current main and both release ancestors, read committed version/build, then central Fastlane beta with exact artifact guards. Outputs remain under ignored build/apple-release.
- `mac-run 'voice notes' apple_metadata`: existing Fastlane iOS metadata lane for the committed version. Preserve existing listing/screenshots apart from this release's What's New.
- `mac-run 'voice notes' release`: submit the already uploaded exact VALID build through canonical PHASE=submit, after rejecting any active review. Does not rebuild or increment source.

The native actions require the runner's normal owner approval and resource gates. Stop on the first infrastructure failure. Successful upload/submission and independent artifact/Apple readback remain pending.
