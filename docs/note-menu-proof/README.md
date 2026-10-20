# Note overflow menu proof

Status: **photo-picker failure reproduced; minimal fix applied, verification pending the Mac runner cooldown.**

Owner report (October20,2026): Add Photo from the note menu never opens Photos. The actual note was found through the connected EEON MCP. Its private contents and identifier are deliberately absent from the test fixtures and this public repository.

## Run

Use the committed Mac runner actions:

```sh
mac-run 'voice notes' note_menu_diagnostics
mac-run 'voice notes' e2e_note_menu_photo
mac-run 'voice notes' e2e_note_menu
```

The script creates one disposable, signed-out simulator, imports the existing whiteboard image, and uses actual Photos UI, SwiftData persistence, files and API services. It refuses another running simulator or less than15GiB free. It shuts down/deletes its own simulator in `finally`. No existing account or personal note is edited. No mock services. The full suite uses real AI calls and may incur their normal API cost. No retry loop is configured.

## Current evidence

- Live Mac runner preflight passed: Xcode26.2, available iOS26.3.1 runtime,39.3GiB free at latest UI attempt.
- First run rejected an incompatible iPod model: simulator metadata's iPhone productFamily also includes iPod touch. The selection now checks actual model name and runtime compatibility.
- Second run created/booted an iPhone17e, then Photos fixture import timed out after60seconds. **No EEON build or UI test ran.** Stopped on the infrastructure failure under Shawn's rule3. See [sanitized receipt](2026-10-20.json).
- After owner approval to diagnose/resume, a native build exposed a missing watchOS runtime. Installed the previously verified watchOS26.2 runtime through the Mac runner. The subsequent native build completed and one UI test ran, but the app crashed twice during CloudKit initialization before reaching the menu. Built artifact inspection proved missing entitlements. Corrected test signing; the next built-artifact check passed and the app reached the real note/menu.
- Signed source `efdec38` reproduced the owner failure: tapping Add Photo closed the menu and left the note visible, with no system picker. [Exact red receipt](picker-red.json).
- Candidate `839bfa9` changes only the photo presenter: a menu button toggles state and the stable note view hosts `.photosPicker`. The same verification action was refused by the runner after three failures; next eligible time is approximately12:16PM Chicago. No green result yet; do not rename this a verified fix.

## Intended menu coverage

All menu paths below remain **unverified drafts**, not passing coverage. The focused picker test reached the real menu after signing was corrected and reproduced the reported failure. The candidate fix has not run yet.

| Menu action | Prepared journey / remaining assertion |
|---|---|
| Add Photo | Real picker, select image, attachment visible after relaunch |
| Copy Note / Send to an Agent | Actual clipboard text and note identifier |
| Share as Link | Real signed-out iCloud error only; successful share still needs an Apple test account |
| Export As: Markdown/PDF/Recording | Actual share sheets plus Markdown/PDF text and original audio byte comparison |
| Assign Project | Real project fixture, assignment/relaunch/checkmark and No Project path |
| Manage Tags | Create, persist, remove tag |
| Clean Up Recording | Cancel and actual service completion with known deadline |
| Ask About This Note | Actual scoped response preserving the note's deadline |
| Mind Map | Existing actual API generation journey |
| Identify Speakers | Existing real audio/API journey, two speakers |
| Favorite / Unfavorite | Relaunch persistence round trip |
| Archive / Unarchive | Archived filter visibility and return to Home |
| Playback Speed | Six menu choices plus actual playback-clock timing |
| Delete Note | Cancel, delete to Recently Deleted, restore |

## Resume

Honor the runner cooldown: do not reset its counters, rename the action to bypass it, or weaken its limits. After approximately12:16PM Chicago on October20, run `mac-run 'voice notes' e2e_note_menu_picker` against the committed candidate. Keep the source unchanged until it finishes. If green, run attachment persistence with `e2e_note_menu_photo`, then every menu journey with `e2e_note_menu`. The next Photos import initializes the real Photos app and records system logs on failure. Fix only observed failures, preserve all receipts, and obtain independent runtime verification before claiming the owner bug fixed. Successful CloudKit sharing and physical iPhone behavior cannot be claimed from a signed-out simulator. Nothing here ships a build or changes App Store state.

Shawn authorized automatic resumption after the cooldown. A single chat follow-up (`resume-eeon-menu-tests`) is scheduled for October20,2026 at12:20PM America/Chicago. Independent checkpoint review confirmed the failing runtime trace and cleanup; the candidate remains unverified until the scheduled tests pass.
