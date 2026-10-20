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

`e2e_note_menu_remaining` explicitly excludes Add Photo and does not import a fixture into Photos. Its result cannot be called full-menu proof. `e2e_note_menu_organize` is the focused two-journey subset for project/tags and delete/restore; it explicitly lists all excluded tests. Subsequent bounded approvals were used; the latest attempt stopped at simulator boot readiness before either test ran. No further native attempt is authorized. `cleanup_note_menu` removes only recorded disposable device IDs whose names carry this proof's prefix.

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

## Current stop — 15:57 Chicago

Shawn approved **“Restore the runtime and run once.”** The guarded `prepare_note_menu_runtime` action restored watchOS 26.2 successfully at 15:51:52 (264.1 seconds). Actual post-restoration inventory contained available iOS 26.3.1 and watchOS 26.2, with 35.5 GiB free and zero booted simulators.

The one approved `e2e_note_menu_organize` attempt then failed before building or testing: `simctl bootstatus` for its disposable iPhone 17e timed out after 120 seconds. Job `voice_notes-e2e_note_menu_organize-20261020-155208-qqht` ended at 15:57:07 with exit 1 after 294.8 seconds including cleanup. **Zero native builds and zero UI tests ran.** Independent inspection confirmed no built app, test log, UI attachments or database observations. The disposable simulator directory is gone and no owned native test processes remain. [Restoration/failure receipt](organize-runtime-recovery.json) · [Independent inspection](organize-boot-independent.json).

The boot timeout's root cause is unverified. The subprocess wrapper did not retain partial bootstatus stdout/stderr. Do not infer an app failure, lengthen timeouts or retry from this receipt. The bounded approval is consumed and Rule 3 stops further native attempts. The next work is simulator startup diagnosis before any separately authorized focused test.

The earlier 15:00 focused attempt had stopped because watchOS and the previous build cache were absent; the removal actor remains unknown. That missing-runtime prerequisite is now resolved. Earlier receipts remain historical evidence: [preflight failure](organize-preflight-blocker.json) · [independent inspection](organize-preflight-independent.json). This current section supersedes pending-restoration and retained-build-cache instructions from earlier checkpoints.

## Remaining proof and safeguards

Tag removal and restore completion remain unverified; their observed label corrections are in `9fdf351`. Photo attachment and the ten other passing menu journeys retain their earlier evidence. Successful signed-in CloudKit sharing and physical iPhone behavior need separate proof.

Normal runner settings remain unchanged: default failure cap 3, load 8, idle 0, normal resource gates and one-job lock. Preserve load 8 from the separately authorized removal of the blanket heavy-job restriction. Do not reuse exhausted approvals, rename actions or clear counters to obtain another attempt. Main pushes, TestFlight and App Store release remain unapproved for this change.
