# Spoken daily tasks — local candidate

Requested by Shawn, October13: tell EEON tasks for the day, see them on the front page, and allow a connected AI to read them through MCP when asked. This explicitly replaces the older Home decision to show only a quiet task-count line.

## Local source changes

- Home shows Today’s tasks, up to five open task rows, completion controls/source links and All tasks for the rest. Talk through today uses the existing recorder, preserves source speech as Tasks for today and forces the note/task path instead of question answering or agent Order execution.
- Extraction runs directly for daily captures, bypassing title/tag/calendar attachment and optional rewrite/persona/knowledge compilation; its outcome distinguishes preparation failure from no tasks. Undated daily tasks default to the capture day. Resolved daily deadlines are stored so today does not move with later reads; retry uses the same normalization. Explicit future dates are preserved. Today includes due/overdue work; undated daily work remains in All tasks after its day.
- Initial daily note and extracted actions explicitly save. Reminders synchronization is scheduled after successful extraction persistence. Original captures/task source IDs are preserved.
- Existing opted-in agent mirror includes an actual checkbox/due checklist from stored actions in daily-note content, preserving the transcript. MCP recent_notes/search_notes → get_note can read that daily note; this does not add an agent execution trigger or change OAuth/approval. It does not add structured open_loops support for these checklist rows.

## Verification status

Changed Swift files pass frontend parsing and git diff --check. Independent source review found failure reporting, persistence ordering and retry-date issues, corrected in this candidate. This is source review, not runtime refutation.

Unsigned build attempted once with existing SDKs, no package update/clean: exit70 BEFORE compilation. Xcode says iOS26.2 platform is not installed; simulator runtime inventory is empty. Stop on infrastructure failure: no retry/platform download/device creation. build-attempt.log retains the exact result. AppleCharts voice tasks roadmap could not start because its existing local tsx binary/node_modules are absent; no install/retry or market-proof claim.

## Required real proof before release

Restore an installed iOS platform plus usable test device and adequate post-install disk reserve. Compile the candidate, then speak actual tasks with an explicit future-date item: verify exact source transcript and stored task rows, today/future grouping, completion/relaunch persistence, source navigation, cancellation and truthful failed-extraction state. On phone and iPad verify core tasks/mic controls fit above fold. Connect a reserved account through the existing approved flow, read actual daily note via MCP get_note, verify task status update after opt-in mirror sync and deny access after disconnect. No invented AI output or source-only check substitutes for this.

No running-app, physical speech, extraction service, mirror/MCP end-to-end or Release proof obtained here. Existing publication hold remains; no push/deploy/upload/submission. Local main base is a2c0fa2, not a freshly fetched production/main claim.

Independent-source-review.json records its exact review scope; the subsequent optional-processing shortcut passed parsing only. Retry durability remains unverified because existing reprocessNote uses try? save.
