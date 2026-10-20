# Note overflow menu proof

Status: **draft tests; blocked at test-app CloudKit startup, not a fixed photo-picker bug.**

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
- After owner approval to diagnose/resume, a native build exposed a missing watchOS runtime. Installed the previously verified watchOS26.2 runtime through the Mac runner. The subsequent native build completed and one UI test ran, but the app crashed twice during CloudKit initialization before reaching the menu. Actual signed-artifact inspection is next.
- The app's Add Photo implementation is unchanged. There is no red app reproduction or green app result yet.

## Intended menu coverage

All menu paths below remain **unverified drafts**, not passing coverage. The focused picker test has executed once but failed during app startup before any menu action.

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

Resolve the observed CloudKit startup crash using built-artifact evidence before another UI run; do not blindly retry. The Photos import failure also remains to be diagnosed; the next import initializes the real Photos app and records system logs on failure. Then run the photo regression against unchanged app code, retain the exact red failure, make only the demonstrated fix, rerun green, finish the semantic assertion gaps and run every menu journey. A fresh context must verify the actual result. Successful CloudKit sharing and physical iPhone behavior cannot be claimed from a signed-out simulator. Nothing here ships a build or changes App Store state.
