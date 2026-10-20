# Note overflow menu proof

**Incomplete.** The original no-open failure was reproduced, and the minimal presenter change passed the same presentation test. The actual screenshot shows a loading sheet, so this proves modal presentation only. Photo selection/persistence and the other menu journeys are not yet verified. Nothing has been released.

The owner's private note was read through the connected EEON MCP; its contents and identifier are absent from the disposable fixtures and this public repository.

## Observed results

- **Red:** source `efdec38`, job `voice_notes-e2e_note_menu_picker-20261020-111018-pbpc`: Add Photo closed the menu, no picker appeared, one UI test failed. [Receipt](picker-red.json).
- **Presentation green:** source `5d6e0b9`, job `voice_notes-e2e_note_menu_picker-20261020-121522-cshp`: Add Photo opened a loading modal with Cancel. The test tapped Cancel and found Note options. [Receipt](picker-green.json). Independent review confirmed these facts, but the original assertion did not prove dismissal/hittability. The current test additionally checks disappearance and reopens the menu; those stronger assertions have not run yet.
- **Attachment blocked:** job `voice_notes-e2e_note_menu_photo-20261020-122537-aedn`: simulator Photos launch itself timed out after60s, before photo import or EEON build/test. Stopped without retry. [Receipt](photos-launch-blocker.json).
- **Other menu tests blocked:** job `voice_notes-e2e_note_menu_remaining-20261020-123805-ptpn`: build setup was terminated by SIGTERM after163.2s. Zero UI tests ran; signal sender unknown. This was not the configured30-minute runner timeout. [Receipt](menu-interrupted.json).
- **Cleanup:** job `voice_notes-cleanup_note_menu-20261020-124652-wcrf` removed the interrupted run's recorded disposable simulator. No native proof process was left running.

The runner's cooldown was honored. Shawn authorized automatic continuation; it resumed in this chat when he said "fix it", and the redundant scheduled wake-up was removed. Photos failures and the interrupted build have not been retried.

## Standing suite

Run only through the committed Mac runner actions in `docs/os.yaml`:

```sh
mac-run 'voice notes' note_menu_diagnostics
mac-run 'voice notes' e2e_note_menu_picker
mac-run 'voice notes' e2e_note_menu_photo
mac-run 'voice notes' e2e_note_menu
mac-run 'voice notes' e2e_note_menu_remaining
mac-run 'voice notes' cleanup_note_menu
```

`e2e_note_menu_remaining` explicitly excludes Add Photo and does not import a fixture into Photos. Its result cannot be called full-menu proof. `cleanup_note_menu` removes only recorded disposable device IDs whose names carry this proof's prefix.

The suite uses real UI, SwiftData, Photos, files and API services, without mocked services. Real AI calls may incur their normal API cost. It refuses another booted simulator or less than15GiB free, verifies actual built CloudKit/app-group entitlements, preserves the cached build, freezes source during a run, rejects missing test cases, and deletes its own simulator in `finally`. Interrupted processes need the scoped cleanup action. Never use screenshot fixtures against a personal device/account.

| Menu action | Prepared proof; runtime status |
|---|---|
| Add Photo | Presentation passed; loaded picker, selection, persisted DB row, decoded image file and relaunch remain blocked |
| Copy Note / Send to an Agent | Actual clipboard text and note identifier; unrun |
| Share as Link | Actual signed-out iCloud error; unrun. Successful sharing requires a real Apple test account |
| Export As: Markdown/PDF/Recording | Actual share sheets, readable PDF/Markdown and original audio byte comparison; unrun |
| Assign Project | Real project assignment/relaunch/checkmark and removal; unrun |
| Manage Tags | Create, persist and remove; unrun |
| Clean Up Recording | Cancel and actual service completion preserving the known deadline; unrun |
| Ask About This Note | Actual scoped answer preserving the deadline; unrun |
| Mind Map | Real API generation; unrun |
| Identify Speakers | Real audio/API, two speakers; unrun |
| Favorite / Unfavorite | Relaunch persistence round trip; unrun |
| Archive / Unarchive | Archived filter and return to Home; unrun |
| Playback Speed | All six choices against actual playback-clock timing; unrun |
| Delete Note | Cancel, Recently Deleted and restore; unrun |

## Resume

The current Air runner blocks heavy jobs (`heavy_max_load=0`); Shawn has explicitly approved a temporary normal load limit of8 for EEON after the other app releases the single runner slot, followed by restoring the block. Do not start a second simultaneous simulator or alter other guards. The harness now preserves launch-failure runtime logs before cleanup.

First resolve the observed Photos launch failure and unexplained native build termination; do not blindly retry or bypass runner guards. Keep the existing cached build for this unfinished task. Then run the strengthened picker check, actual photo attachment proof, and remaining menu journeys, fixing only observed failures. Preserve receipts and obtain independent runtime review before claiming complete. Physical iPhone behavior and signed-in CloudKit sharing are separate proof requirements. Main pushes, TestFlight and App Store release remain unapproved for this change.
