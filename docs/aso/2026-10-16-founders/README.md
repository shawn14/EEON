# EEON: founders building with AI — ASO pass, October 16, 2026

Shawn identified the intended audience as founders building with AI and authorized using Fastlane to push the ASO changes to App Store Connect. Recommendation: commit the positioning to that audience, with the concrete promise **Think out loud. Give your AI the context.** The store subtitle is **Voice notes for AI builders**. Keep the existing name, EEON: AI Memory & Notes, and Productivity category.

“AI coding management” is too broad for the shipped product. It suggests agent execution, orchestration, repository state, reviews, and completion tracking. EEON currently captures the founder's thinking and makes it available to a connected agent. That is useful on its own. Treat a fuller management product as a separate product decision, not a metadata claim.

## Observed evidence

Fresh AppleCharts runs against Apple's US public endpoints returned **56 results / 55 distinct apps across six searches**. One bounded voice-notes roadmap examined **5 apps, fetched 152 reviews, and included 114 within six months**. Separate Wispr and Replit pages supplied 50 reviews each. Total unique fetched reviews across these seven sampled apps: **252**. The later full Voicenotes page overlaps the roadmap and is not additional demand. One sampled app supplied zero reviews. Coverage is recent RSS, not a complete six-month history: only two of five roadmap apps reached the cutoff. No failed/throttled apps were reported.

These are public listing/search samples, not organic iPhone rankings, keyword search volumes, installs, revenue, or proof of founder willingness to pay. Review authors' statements are unverified customer experiences. Modeled revenue and ranking scores in the full roadmap are excluded from the recommendation.

| Search | Returned / requested | What appeared | ASO implication |
|---|---:|---|---|
| voice notes | 9 / 10 | Voice Memos, Voicenotes, Otter and recorders | Relevant discovery vocabulary; entrenched incumbents |
| vibe coding | 9 / 10 | Vibecode, Claude, Replit, other AI builders | Users may expect actual software generation; avoid as the main EEON promise |
| founder | 10 / 10 | Banking, membership, networking and fundraising | Clear audience label, weak evidence of relevant store search intent |
| AI task manager | 8 / 10 | Tiimo, Google Tasks, Notion, Structured, Motion | Broad planner expectations; many established substitutes |
| voice to prompt | 10 / 10 | Wispr, SpeakApp, dictation and mixed voice tools | Some relevant behavior, mixed results; no volume proof |
| project memory | 10 / 10 | Games, Bible memory, Project Life, Notion | Plausible positioning language, poor discovery evidence |

Ratings below were read October16,2026 through AppleCharts, US storefront. They measure accumulated public ratings, not paying users.

| Product | US ratings | Rating | Role in the decision |
|---|---:|---:|---|
| [Wispr Flow](https://apps.apple.com/us/app/id6497229487) | 17,351 | 4.84 | Voice input, including developer prompts; directly targets founders |
| [Voicenotes](https://apps.apple.com/us/app/id6483293628) | 7,137 | 4.77 | Closest memory/capture/MCP overlap |
| [Otter](https://apps.apple.com/us/app/id1276437113) | 84,898 | 4.79 | Established transcription and meeting expectations |
| [Replit](https://apps.apple.com/us/app/id1614022293) | 21,269 | 4.72 | Actual AI building, different product job |
| [Vibecode](https://apps.apple.com/us/app/id6742912146) | 3,325 | 4.65 | Another actual builder in the vibe-coding sample |
| [Notion](https://apps.apple.com/us/app/id1232780281) | 90,401 | 4.78 | Existing notes/tasks workspace |
| [Vibe Coding Toolkit](https://apps.apple.com/us/app/id6746705587) | 1 | 3.00 | Small planning specialist; not evidence of a large underserved category |
| [EEON](https://apps.apple.com/us/app/id6758273499) | 2 | 5.00 | Early credibility base; download/conversion performance unknown |

EEON public lookup confirms **3.10.0**, released October9, free download. Version3.11.0(172) is in TestFlight; the current release receipts are in [testflight-172](../../spoken-daily-tasks/testflight-172/README.md).

## What the reviews actually support

Manually inspected examples are preserved in full, with Apple IDs, dates and URLs in `evidence/reviews-*.json`.

- **AI access to captured thinking has explicit value.** Voicenotes review14659021206, October12, five stars, praises reliable outdoor capture and its MCP connection letting AI agents access notes. This is the strongest specific evidence for the proposed workflow. It simultaneously disproves any claim EEON is uniquely doing it. One review is a signal, not a market-size estimate.
- **Speaking prompts is already a real use.** Wispr review14663536499, October13, mentions extensive AI prompting;14655084217, October11, praises writing AI prompts accurately;14663340363, October13, identifies as a developer and values dictation accuracy. These support input convenience, not a request for an agent-management dashboard.
- **Capture reliability matters more than extra features.** Wispr14653872801, October11, reports repeated missing output;14661142798, October13, describes retry frustration after long dictation. Voicenotes14113161283, May27, reports lost meeting capture. Other reviews praise reliability, so this is mixed user evidence rather than a universal defect claim. EEON must demonstrate preservation/recovery before making superiority claims.
- **Control and cost are concerns in AI building.** Replit14482172614, August28, describes repeated instructions and expensive debugging;14565718795, September18, praises bringing an idea to life while criticizing unclear costs. These are user reports, not verified billing facts. EEON cannot promise lower coding bills or solve an external agent's execution failures.
- **Readable output and task continuity are useful.** Otter14577265824, September21, praises sorting ideas for clarity. Voicenotes14190814810, June16, values reliable notes and transfer into the existing workspace. This supports making the handoff visible, without adding every possible integration.

AppleCharts' automatic labels are not reliable enough to use as direct demand counts here. The voice-notes roadmap tagged7 pricing complaints and2 reliability complaints, but one reliability example is positive and the MCP praise is misclassified under videos/coaching. No explicit request clusters were detected. Use the reviewed text above; do not pitch “7 users want founder tools.”

## Wider market: occupied, but a focused audience is still useful

[Wispr's own founder page](https://wisprflow.ai/post/ultimate-ai-voice-founders) explicitly markets voice input for founder task management and development. [Its Cursor example](https://wisprflow.ai/post/file-tagging-in-cursor) shows developer-specific input. Voice coding alone is already contested.

[Voicenotes' MCP article](https://voicenotes.com/blog/usecase/voicenotes-mcp/) describes querying captured ideas, decisions, follow-ups, and launch context in another AI tool. The differentiation must be the quality and simplicity of EEON's founder workflow, not the existence of MCP.

[Taskmaster's current first-party site](https://tryhamster.com/research/taskmaster) covers requirements, tasks, dependencies and acceptance criteria, now within Hamster's broader planning offering. “AI coding management” puts EEON against tools that own more of execution.

[Vibe Kanban's April10 shutdown announcement](https://vibekanban.com/blog/shutdown) says the company is closing, its project will continue as community-maintained open source, and most of its thousands of daily users were free. This is a specific counterexample to assuming adoption of agent-management tooling guarantees a business. It does not prove founders will not pay for EEON.

Our inference: **solo founders and small product teams already using coding agents are a sensible initial audience, but the paid value must be demonstrated in repeated use.** No vacant category, search-volume estimate or revenue projection was established.

## The three outcomes to focus on

1. **Capture what I want changed while it is fresh.** Speak an idea, bug, customer insight or constraint; keep the source and a readable note. Evidence: prompt-writing and capture reliability reviews. Existing recording/transcription/enhancement are the starting point. Verify the same real capture survives relaunch and its source remains inspectable. Defer a desktop dictation keyboard.
2. **Give my AI the relevant context without rewriting it.** A connected agent reads the selected note; it can use the decisions and intended next step when the founder asks it to plan work. Evidence: explicit MCP praise and existing competitors. Existing Send to an Agent copies a get_note prompt; it does not launch a job. Verify exact note identity and content in an actual authorized client. Defer orchestration, autonomous dispatch, GitHub write-back and new task-service OAuth.
3. **Pick up the next step with the decision still attached.** Show extracted actions and let the founder ask what they decided before proceeding. The3.11 daily-task work is relevant here, but still needs Shawn's TestFlight walkthrough. Verify separate tasks, explicit future dates, completion/relaunch and opted-in MCP readback. Defer automatic proof that code shipped or tasks completed externally.

Reuse the existing SwiftData notes/actions/projects, extraction pipeline, CloudKit sync, encrypted optional mirror, QR authorization, and read-only MCP. No new database, model provider, pricing or paywall is proposed. The separate `codex/eeon-founder-handoff` experimental branch contains additional unshipped work; it is **not** proof of current App Store functionality and is not merged by this ASO task.

## Listing changes

The current public description opens with generic AI memory, then spans journaling, meetings and personal reflection. Agent access is buried near the bottom. The website also leads with a general personal assistant promise. Promote the founder's use case and make the agent handoff understandable near the top.

| Field | Uploaded draft | Limit |
|---|---|---|
| Name | EEON: AI Memory & Notes | 23 / 30 |
| Subtitle | Voice notes for AI builders | 27 / 30 |
| Primary promise | Think out loud. Give your AI the context. | Positioning line |
| Category | Productivity | Retain |
| Keywords | tasks,dictation,transcribe,reminders,ideas,projects,decisions,brain dump,prompts,founder,mcp | 92 / 100 |

Name remains unchanged; a rename was not requested. The subtitle repeats “AI” and “notes” for human clarity; the hidden keywords do not duplicate title/subtitle terms. Functional discovery terms remain the majority. Founder, prompts and MCP are small exploratory allocations, not high-volume claims. Do not put competing brand names in the keyword field. Compatibility names appear only in factual description text.

Promotional text: **Building with AI? Talk through ideas, bugs, and next steps. Keep the decisions, then let your connected AI agent read the context.**

All six files are in `metadata/en-US`; `metadata-validation.json` checks character limits. The full description makes the optional encrypted server copy explicit. It does not claim offline AI, guaranteed recall, automatic execution, a completed coding-management product, or that notes never leave iCloud. Retained US subscription prices come from the current public listing and are not a price change. Candidate3.11 release notes describe only that build's task changes; the feature still needs the approved on-device test.

[Apple's search guidance](https://developer.apple.com/app-store/search/) supports accurate functional keywords, avoids brand stuffing and duplicate hidden terms, and distinguishes promotional copy from ranking. [Product page guidance](https://developer.apple.com/app-store/product-page/) defines the field limits. Audience positioning and indexed search terms serve different purposes.

## Screenshot plan

No replacement images were fabricated or uploaded by the research phase. Use actual release UI after a real task walkthrough. Suggested example: a founder discusses an onboarding bug, a design decision, a task for today and a separate task due Friday. Captures must show the actual generated result, with clear example labeling where appropriate. Do not build a fake execution dashboard into screenshots.

| Order | Hook | Actual screen | Evidence / verification |
|---|---|---|---|
| 1 | Voice notes for AI builders | Readable product/bug note, source accessible | Immediately identifies audience and output; exact spoken input/result |
| 2 | Keep the decisions and next steps | Note's extracted decisions and actions | Useful continuity; task extraction must match spoken intent |
| 3 | Give your AI the context | Real AI agents setup + current Send to an Agent action | MCP review demand; copy/paste/read behavior accurately shown |
| 4 | Remember why you chose it | Actual sourced answer to an onboarding decision question | Recall and planning benefit, no perfect-memory promise |
| 5 | See what needs doing today | Build172 Home tasks with future item correctly excluded | Publish only after TestFlight proof |
| 6 | Capture the thought as it comes | Current recording/entry screen | Capture convenience; no unverified Watch/background claim |

First three screenshots should carry the story. Calendar and general journaling become secondary. The broader website headline needs the same audience treatment in a separate website edit; this task does not deploy that site.

## Measurement and next work

1. Complete the real TestFlight founder flow and capture its outputs. This is the immediate product proof, using existing work rather than a new feature batch.
2. Metadata is uploaded to the editable iOS draft with exact readback. After the real TestFlight flow passes, use its captures for the screenshot plan and the established review submission path. Existing screenshots remain until real replacements are ready. No App Review submission occurred in this ASO pass.
3. Test the proposition with5–10 actual founders already building with AI, using the same capture→agent-read→next-step example. This is a proposed validation sample, not a claim of statistical significance. Measure first usable note, successful agent read, repeated use in the following week and willingness to pay. No outreach was sent or authorized by the research request.

For store measurement, obtain the previous28 complete days of US iPhone Search impressions, first-time downloads and conversion, separately from Browse/referrals and paid acquisition where possible. Then compare the same sources after publication while keeping price/paywall stable. The earlier October8 reporting-key403 remains an unresolved historical access limitation; this session has no download or conversion baseline and does not claim an ASO lift. Small samples require absolute counts, not impressive percentages. Existing user reviews cannot estimate keyword volume.

## Canonical upload and source boundary

Use the central clean-source Fastlane metadata lane, `fastlane metadata app:voice-notes version:3.11.0`, after observing Apple's actual editable state. The lane uploads metadata only, skips screenshots/binary upload, and does not submit review. The repo's `scripts/asc_push.py --version 3.11.0 --skip-screenshots` is the established recovery if deliver reports success but exact field readback differs; use no repeated blind retries. Confirm source against the reviewed candidate and read back all six fields independently.

Research base mainf9a9dbf contains both uploaded172 sourceabfdd41 and previous App Store171 source6f7d7ed. Nothing in this task rebuilds or changes that binary. Latest Apple upload/readback status is recorded below as work completes.

## Upload result and recovered tooling incident

**October16,17:04:10Z: corrected Fastlane upload completed.** iOS3.11.0 remains PREPARE_FOR_SUBMISSION with VALID build172 attached, release typeMANUAL. The six ASO fields plus marketing, support and privacy URLs match local source exactly. All15 existing iOS screenshots are retained; this pass did not upload new graphics. PubliciOS3.10.0/build171 remains live. This is an Apple draft upload, not public publication, App Review submission, or runtime proof of the task feature.

The initial canonical lane incorrectly inferred macOS from the repo's tracked `voice notes.pkg` and resolved `./apps/.../metadata` against the wrong working directory, creating an empty metadata folder. It reported success and created a new MAC_OS3.11.0 draft at16:54:46Z. The existing recovery script selected the first same-version result without a platform filter, so it populated that Mac draft while iOS remained unchanged. Exact Apple readback and an independent refuter caught both errors before any submission.

Fixed the central lane to pass explicitiOS and an absolute metadata path, validate the six required EEON files, and call the read-only exact-match verifier. Fixed recovery to select IOS+version, reject ambiguity, never create during verify-only, and fail on mismatched local metadata fields. The new guard failed against actual old iOS copy, then passed against the corrected upload. Ruby/Python syntax and diff checks also pass. Do not retry a successful-looking deliver operation blindly; inspect platform and exact values.

Apple rejected deletion of the unintended Mac draft with409STATE_ERROR: only the first platform version may be deleted, and no version can be deleted once a build has been uploaded for that platform. Its version-localized copy was therefore restored from freshly read liveMac3.5.1. It remains an unused PREPARE_FOR_SUBMISSION draft with no build. The shared editable appInfo intentionally keeps the approved iOS subtitle; live appInfo remains unchanged. **The unused Mac draft was not deleted.** Receipts: `evidence/mac-draft-cleanup.json`, `mac-draft-restoration.json`, `asc-final.json`, and `independent-final.json`.

The evidence proves Apple's stored fields, selected build and assets. Founder conversion lift, retention, willingness to pay, on-device task behavior and agent runtime execution remain unproven.

Independent Apple reads at17:07:07–17:07:18Z confirm all nine fields, build172VALID, all15unchanged screenshots, liveiOS3.10/build171 and public appInfo unchanged, and absent submission relationships on both drafts. Current liveMac3.5.1/build138 matches the saved restoration source; no original pre-operation Mac snapshot existed, so this does not assert a broader historical Mac comparison. The unusedMacdraft remains without a build.

## Subsequent authorized review submission
Shawn then explicitly requested AppReview.3.11/build172 is now WAITING_FOR_REVIEW, with the newASO and a realWatchscreenshot added to resolve Apple's required-slot error;16assetscomplete, original15unchanged. Manualreleaseafterapproval remains. [Full submission receipts and command](submission-311/README.md). Earlier draft-only statements above describe the ASO upload phase.
