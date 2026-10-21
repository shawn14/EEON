# Otter benchmark for EEON — October 21, 2026

Otter's US App Store listing currently shows **4.8/5 from 86K ratings** and **#61 in Productivity**. The useful lesson is its complete path from recording to a usable result. For EEON, prioritize source-linked follow-through on personal and project notes. [Apple listing](https://apps.apple.com/us/app/otter-transcribe-voice-notes/id1276437113).

Scope: official product/help/pricing pages plus EEON source at release merge `91b7515`. This is a documentation and repository audit, not an authenticated Otter trial or a fresh EEON device test. The bounded AppleCharts roadmap command failed before fetching because `tsx`/node_modules were absent. No installation or retry was made. No current review-frequency claims, accuracy ranking, latency comparison, or conversion projections are supported by this audit.

## What Otter is doing well

Otter markets a before/during/after meeting workflow: prepare for a call, capture it, extract takeaways, then follow up. Its current website extends that into enterprise sales and recruiting workflows. The principle worth borrowing is making the next useful action easy to reach. Its meeting-heavy positioning does not establish demand for every feature in an iPhone voice-memory app. [Otter](https://otter.ai/).

Its latest desktop/web AI Chat adds a Work mode that can produce documents and use connectors for Jira, Notion, Drive and Gmail. The documentation describes approval prompts for actions that require permission. This is a gradual rollout, and platform/plan availability varies; it would be misleading to attribute the entire desktop workflow to the iPhone app. [AI Chat overview](https://help.otter.ai/hc/en-us/articles/19682180167575-Otter-AI-Chat-Overview).

**MCP is already table stakes.** Otter documents OAuth-connected access for Claude, ChatGPT, Cursor and Perplexity; its pricing page includes the MCP server on Basic. EEON's advantage must come from the usefulness and trustworthiness of the context it supplies, beyond having a connector. [MCP documentation](https://help.otter.ai/hc/en-us/articles/35287607569687-Otter-MCP-Server), [pricing](https://otter.ai/pricing).

## Comparison against EEON

“Present” below means located in current source unless specifically labeled runtime-proven. It does not mean retested on a physical iPhone today.

| Job | Otter evidence | EEON evidence | Recommendation |
|---|---|---|---|
| Record, transcribe and find something later | Live transcription, speaker labels, searchable recordings, timed playback in Apple listing | AudioRecorder, TranscriptionService, TranscriptTimeline, search | Improve reliability and discoverability; no new subsystem needed |
| Ask across saved conversations | Cross-conversation AI Chat and sources | RAGService and AnswerSheet already provide cross-note answers with note links | Extend source precision |
| Turn speech into work | Work mode and connected outputs | Native rewrite templates, extracted decisions/actions/commitments, Send to Agent | Add a few useful output presets and a reviewable handoff |
| Verify an extracted action | AI-generated action has View in transcript | ExtractedItem stores sourceNoteId; transcript timing already exists separately | Connect each derived item to its actual passage/audio |
| Attach a visual in context | Image inserted beside selected transcript text | Note.imageFileNamesJSON stores note-level attachments | Add optional passage association after core photo reliability |
| Prepare before meeting | Homepage describes pre-call briefs | Calendar, project/person knowledge and retrieval exist; no Prepare flow found in calendar view | On-demand brief on calendar/project detail |
| Capture both sides of a desktop call | Dedicated Mac/Windows system-audio + mic capture | Mic recorder found; equivalent desktop system-audio flow not established | Consider later if usage data shows this is a frequent job |

Otter feature evidence: [conversation/actions](https://help.otter.ai/hc/en-us/articles/5093228433687-Conversation-Page-Overview), [images](https://help.otter.ai/hc/en-us/articles/21557189457303-Add-images-to-your-conversation), [desktop capture](https://help.otter.ai/hc/en-us/articles/35973988280215-Otter-Desktop-App-Mac-Windows).

EEON repository pointers: `voice notes/AudioRecorder.swift`, `TranscriptionService.swift`, `TranscriptTimeline.swift`, `RAGService.swift`, `AnswerSheet.swift`, `ExtractedItem.swift`, `CustomRewriteTemplate.swift`, `RewriteTemplatePickerSheet.swift`, `CalendarMeetingsView.swift`, `Note.swift`, `NoteDetailView.swift`.

## The three outcomes to improve

### 1. Trust and revisit exactly what was said

Add “Hear source” beside generated decisions, commitments, action items and substantive answer claims. It should open the exact transcript passage and play the associated audio, preserving the original separately from any rewrite. If there is no reliable alignment, show a note-level source or explicitly unavailable timestamp rather than inventing one.

Otter already links its generated action items to transcript context. EEON has note-level source IDs and timed transcript playback, so this is a connection between existing capabilities. Durable passage identities need to survive transcript corrections and speaker edits; a raw character offset alone is insufficient.

A related, later improvement: let a photo attach to a selected passage. For Shawn's internet-evolution note, the image could sit beside the part of the explanation it illustrates. Current EEON OCR runs when a note has no text; adding an image to an existing transcript is not automatically equivalent to giving its contents to every AI answer. Do not present photo upload as full visual understanding without a separate real proof.

### 2. Turn a spoken idea into a brief another person or agent can use

Add three presets using the existing native template editor: **Build brief**, **Decision memo**, and **Customer interview**. Keep them editable. A Build brief should contain the stated problem, intended behavior, constraints, acceptance checks and unresolved questions, with links to source passages. Unknown owners/deadlines/requirements must stay unknown.

Current Send to Agent copies an instruction to call get_note and act on the note. It does not preview a structured plan. Upgrade that handoff to a reviewable brief plus stable source references, then reuse the existing copy/share/connector path. This matches Shawn's actual voice-note-to-agent workflow without introducing another agent runtime or third-party task OAuth.

Otter offers custom meeting templates, but documents that mobile can apply them while creation/management happens in a browser. EEON already has a native custom-template editor in source. Make that capability easier to discover and validate on device. [Custom templates](https://help.otter.ai/hc/en-us/articles/31402572907415-Custom-Meeting-Type-Templates).

### 3. Resume a project or arrive at a meeting prepared

Add an explicit **Prepare** action to a meeting or project. Show the latest relevant decisions, outstanding commitments and unanswered questions with dates and sources. Use the existing calendar, people/projects and retrieval structures; compute it on demand.

Respect the existing simplified Home decision: Calendar → Tasks → Notes. Do not restore an automatic briefing hero or introduce a notification/cron service for this slice. A project/person match must be visible and correctable; similarly named people should not silently mix contexts. Unavailable notes should produce an honest empty result.

## What to keep, change and defer

**Keep:** quick Apple capture, local note ownership, explicit AI access, the simplified Home, native templates, Apple Reminders, existing MCP and exports. The September 25 task-sync decision explicitly keeps task integrations Apple-only because OAuth adds credential/privacy/review burden. A competitor comparison does not override it.

**Change:** precise citations, the quality of the Send to Agent brief, and access to meeting/project context. Prioritize menu reliability before making the menu longer. Earlier real menu proof covered Add Photo attachment/persistence and ten other journeys, while tag removal and restore completion still lack a completed focused rerun after the simulator failure.

**Defer:** meeting bots, sales coaching, CRM writes, team channels, more platforms and a proprietary autonomous agent platform. These expand the product and its ongoing support burden. Desktop system-audio capture is a legitimate later candidate, contingent on actual customer usage and a device-level permissions/lifecycle proof.

## Pricing and privacy implications

Otter Basic includes 300 transcription minutes/month but limits conversations to 30 minutes, file imports to three lifetime, and accessible history to the latest 25 conversations. Pro lists $16.99/month or $8.33/month billed annually. Business's “unlimited” meeting/in-app transcription does not mean unlimited imported-file minutes: the listed allowance is 6,000. These are current published base terms, not a reason by themselves to change EEON's pricing. [Pricing](https://otter.ai/pricing).

EEON should explain capture, cloud transcription, AI processing and connector sharing separately. Its final transcription path uploads audio to an external transcription API, so “everything stays on device” would be inaccurate. Otter says de-identified user data trains its own technology, while its AI service providers do not train on customer data; those are different statements. Clear controls and accurate wording are a credible distinction, without making unverified privacy claims. [Otter security/privacy](https://otter.ai/privacy-security).

## First implementation slice, if approved

Start with one **Build brief** preset and preview using the existing rewrite/handoff flow. Require source note references immediately; add precise passage links only after the transcript alignment path is proven. This is smaller and more reviewable than launching all three outcomes together.

The proof must use consented real notes and real service responses: a spoken idea with constraints, one with missing details, one with multiple speakers, and one with a photo. Confirm that the brief preserves constraints, marks unknowns, opens each cited source, survives relaunch, and hands off through the actual connector/copy path. Inspect audio links against the recording on a physical device. No synthetic production content or mocked “it works” claim.

No product features were implemented as part of this benchmark. Ranking above is product judgment grounded in documented workflows and current EEON implementation, not measured retention lift.
