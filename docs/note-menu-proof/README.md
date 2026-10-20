# Note overflow menu proof

**Photo attachment passed in Simulator.** The original no-open failure was reproduced. The presenter fix now passes open→cancel→reopen→actual photo selection→attachment→relaunch, plus actual SwiftData and decoded-image checks. [Photo receipt](photo-green.json). The latest remaining-menu run passed10of12tests. Independent runtime inspection verified project and tag persistence; the two failures are exact-label test lookups. Corrections are prepared, but tag removal and restore completion still require a run. [Latest receipt](menu-second-complete-run.json) · [Independent review](menu-independent-review.json). Nothing has been released.

The owner's private note was read through the connected EEON MCP; its contents and identifier are absent from the disposable fixtures and this public repository.

## Observed results

- **Red:** source `efdec38`, job `voice_notes-e2e_note_menu_picker-20261020-111018-pbpc`: Add Photo closed the menu, no picker appeared, one UI test failed. [Receipt](picker-red.json).
- **Presentation green:** source `5d6e0b9`, job `voice_notes-e2e_note_menu_picker-20261020-121522-cshp`: Add Photo opened a loading modal with Cancel. The test tapped Cancel and found Note options. [Receipt](picker-green.json). Independent review confirmed these facts, but the original assertion did not prove dismissal/hittability. The later attachment proof passed those stronger disappearance/hittability/reopen checks.
- **Historical attachment blocker:** job `voice_notes-e2e_note_menu_photo-20261020-122537-aedn`: simulator Photos launch itself timed out after60s, before photo import or EEON build/test. Stopped without retry. [Receipt](photos-launch-blocker.json).
- **Historical menu interruption:** job `voice_notes-e2e_note_menu_remaining-20261020-123805-ptpn`: build setup was terminated by SIGTERM after163.2s. Zero UI tests ran; signal sender unknown. This was not the configured30-minute runner timeout. [Receipt](menu-interrupted.json).
- **Cleanup:** job `voice_notes-cleanup_note_menu-20261020-124652-wcrf` removed the interrupted run's recorded disposable simulator. No native proof process was left running.

The runner's cooldown was honored. Shawn authorized automatic continuation; it resumed in this chat when he said "fix it", and the redundant scheduled wake-up was removed. The second complete remaining-menu run executed12journeys:10passed/2failed. Independent review checked raw runtime evidence, the built artifact, live disposable SQLite and exported files. The remaining failures are documented below.

## Standing suite

Run only through the committed Mac runner actions in `docs/os.yaml`:

```sh
mac-run 'voice notes' note_menu_diagnostics
mac-run 'voice notes' e2e_note_menu_picker
mac-run 'voice notes' e2e_note_menu_photo
mac-run 'voice notes' e2e_note_menu
mac-run 'voice notes' e2e_note_menu_remaining
mac-run 'voice notes' e2e_note_menu_organize
mac-run 'voice notes' cleanup_note_menu
```

`e2e_note_menu_remaining` explicitly excludes Add Photo and does not import a fixture into Photos. Its result cannot be called full-menu proof. `e2e_note_menu_organize` is the focused two-journey subset for project/tags and delete/restore; it explicitly lists all excluded tests. The currently prepared run requires fresh authorization because the approved three attempts are exhausted. `cleanup_note_menu` removes only recorded disposable device IDs whose names carry this proof's prefix.

The suite uses real UI, SwiftData, Photos, files and API services, without mocked services. Real AI calls may incur their normal API cost. It refuses another booted simulator or less than15GiB free, verifies actual built CloudKit/app-group entitlements, preserves the cached build, freezes source during a run, rejects missing test cases, and deletes its own simulator in `finally`. Interrupted processes need the scoped cleanup action. Never use screenshot fixtures against a personal device/account.

| Menu action | Prepared proof; runtime status |
|---|---|
| Add Photo | Passed loaded picker/cancel/reopen/selection/relaunch; actual DB contains1attachment and saved JPEG decodes1800×800 |
| Copy Note / Send to an Agent | Passed actual UI paste of note text and agent brief with note identifier |
| Share as Link | Signed-out iCloud error passed. Successful sharing requires a real Apple test account |
| Export As: Markdown/PDF/Recording | All3share sheets passed; independent actual-file inspection confirms readable PDF/Markdown and exact original audio bytes |
| Assign Project | Reproduced lost selection; explicit save now passed selection/removal across relaunch, independently observed in live SQLite |
| Manage Tags | Created and persisted as Menu Proof Tag; test expected different capitalization. Lookup corrected; removal not yet exercised |
| Clean Up Recording | Passed real service cleanup, persisted text and actual pasted deadline content |
| Ask About This Note | Passed; actual scoped answer preserves Thursday-night deadline |
| Mind Map | Passed with actual API generation |
| Identify Speakers | Passed with real audio/API and two speakers |
| Favorite / Unfavorite | Passed both directions across relaunch |
| Archive / Unarchive | Passed archive/filter/unarchive round trip |
| Playback Speed | Passed all six choices against actual playback-clock timing |
| Delete Note | Cancellation and deletion passed. Test missed the compound Recently Deleted button label; lookup corrected, restore completion not yet exercised |

## Resume

All three explicitly approved extra native verification attempts are consumed. The failure-cap setting is back to its normal default3; a fresh idle runner heartbeat followed completion. Preserve load8/idle0 from the separately authorized removal of the blanket heavy-job restriction. The disposable simulator was cleaned up.

The concrete next verification is one `e2e_note_menu_organize` run with the two observed label corrections. It uses the same build cache, real UI/database and resource safeguards, and does not repeat the ten passing service/export journeys. Do not run it under the exhausted allowance or silently use it to bypass a cap; obtain a new bounded approval first. Physical iPhone behavior and successful signed-in CloudKit sharing remain separate proof requirements. Main pushes, TestFlight and App Store release remain unapproved for this change.

## Latest infrastructure stop — 15:00 Chicago

Shawn authorized one focused run after the three-run allowance. Job145923-agan failed in2.7seconds before creating a device, building or executing UI tests: the required watchOS runtime was no longer installed. Actual inventory contained only iOS26.3.1; the cached app/DerivedData and previous ignored result directories were also absent. Removal actor is unknown. Committed sanitized evidence remains. [Failure receipt](organize-preflight-blocker.json) · [Independent inspection](organize-preflight-independent.json).

This supersedes the earlier cache-retained/pending-focused-approval checkpoint. No native retry or download occurred; normal safeguards remain. The concrete recovery is the committed `prepare_note_menu_runtime` action (watchOS26.2,25GiB minimum;44.8GiB observed), then one `e2e_note_menu_organize` run after a new bounded authorization. Tag removal and restore completion remain unverified.
