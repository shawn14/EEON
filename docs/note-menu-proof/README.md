# Note overflow menu proof

**Photo attachment passed in Simulator.** The original no-open failure was reproduced. The presenter fix now passes open→cancel→reopen→actual photo selection→attachment→relaunch, plus actual SwiftData and decoded-image checks. [Photo receipt](photo-green.json). The first complete remaining-menu run passed8of12tests; fixes for its4failures await the final approved run. [Earlier menu receipt](menu-first-complete-run.json). Nothing has been released.

The owner's private note was read through the connected EEON MCP; its contents and identifier are absent from the disposable fixtures and this public repository.

## Observed results

- **Red:** source `efdec38`, job `voice_notes-e2e_note_menu_picker-20261020-111018-pbpc`: Add Photo closed the menu, no picker appeared, one UI test failed. [Receipt](picker-red.json).
- **Presentation green:** source `5d6e0b9`, job `voice_notes-e2e_note_menu_picker-20261020-121522-cshp`: Add Photo opened a loading modal with Cancel. The test tapped Cancel and found Note options. [Receipt](picker-green.json). Independent review confirmed these facts, but the original assertion did not prove dismissal/hittability. The later attachment proof passed those stronger disappearance/hittability/reopen checks.
- **Historical attachment blocker:** job `voice_notes-e2e_note_menu_photo-20261020-122537-aedn`: simulator Photos launch itself timed out after60s, before photo import or EEON build/test. Stopped without retry. [Receipt](photos-launch-blocker.json).
- **Historical menu interruption:** job `voice_notes-e2e_note_menu_remaining-20261020-123805-ptpn`: build setup was terminated by SIGTERM after163.2s. Zero UI tests ran; signal sender unknown. This was not the configured30-minute runner timeout. [Receipt](menu-interrupted.json).
- **Cleanup:** job `voice_notes-cleanup_note_menu-20261020-124652-wcrf` removed the interrupted run's recorded disposable simulator. No native proof process was left running.

The runner's cooldown was honored. Shawn authorized automatic continuation; it resumed in this chat when he said "fix it", and the redundant scheduled wake-up was removed. A later complete remaining-menu run executed12journeys:8passed/4failed. Independent review checked raw runtime evidence and exported files. The fixes for those observed failures await verification.

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
| Add Photo | Passed loaded picker/cancel/reopen/selection/relaunch; actual DB contains1attachment and saved JPEG decodes1800×800 |
| Copy Note / Send to an Agent | Actual Copy/Paste observed; placeholder lookup failed after paste. Selector corrected; agent brief not yet reached |
| Share as Link | Signed-out iCloud error passed. Successful sharing requires a real Apple test account |
| Export As: Markdown/PDF/Recording | All3share sheets passed; independent actual-file inspection confirms readable PDF/Markdown and exact original audio bytes |
| Assign Project | Reproduced selection lost on immediate relaunch. Explicit save prepared, unverified |
| Manage Tags | Create, persist and remove; unrun |
| Clean Up Recording | Real service returned and persisted cleaned text/deadline; clipboard assertion selector failed after actual paste. Corrected check pending |
| Ask About This Note | Passed; actual scoped answer preserves Thursday-night deadline |
| Mind Map | Passed with actual API generation |
| Identify Speakers | Passed with real audio/API and two speakers |
| Favorite / Unfavorite | Passed both directions across relaunch |
| Archive / Unarchive | Passed archive/filter/unarchive round trip |
| Playback Speed | Passed all six choices against actual playback-clock timing |
| Delete Note | Actual confirmation observed; iOS26uses outside-tap cancellation. Corrected check pending, delete/restore not reached |

## Resume

The owner approved up to3additional native verification runs. Preserve the current load8/idle0 setting from the separately authorized removal of the blanket heavy-job restriction. Only raise the failure cap temporarily if needed for an approved EEON run; restore it immediately after that run starts. Keep resource safeguards and the single-job lock. Local allowance receipt: `build/note-menu/approved-extra-runs.json`.

Photo verification passed on the second approved attempt. Run the remaining12menu journeys with the observed project-save and test-selector fixes using the final approved attempt. Preserve receipts and obtain independent runtime review before claiming complete. Physical iPhone behavior and signed-in CloudKit sharing are separate proof requirements. Main pushes, TestFlight and App Store release remain unapproved for this change.
