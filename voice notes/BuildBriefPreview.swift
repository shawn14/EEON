import SwiftUI
import SwiftData
import CryptoKit

/// Captured when the preview opens. The fingerprint prevents saving a brief
/// against a source that changed while the model request or editor was open.
struct BuildBriefSource: Identifiable {
    let id: UUID
    let title: String
    let text: String
    let label: String
    var storageKey: String {
        "build_brief:" + SHA256.hash(data: Data(text.utf8)).map { String(format: "%02x", $0) }.joined()
    }

    init(note: Note) {
        id = note.id
        title = note.title.isEmpty ? "Untitled note" : note.title
        if note.enhancedNoteEdited, let edited = note.enhancedNoteText, !edited.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            text = edited
            label = "Your edited note"
        } else if let transcript = note.transcript, !transcript.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            text = transcript
            label = "Original transcript"
        } else if !note.content.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            text = note.content
            label = "Original note"
        } else {
            text = note.enhancedNoteText ?? ""
            label = "Note text"
        }
    }

    func savedBrief(in note: Note) -> String? {
        guard note.activeRewriteType == storageKey,
              let saved = note.activeRewriteText,
              !saved.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return nil }
        return saved
    }

    func handoff(_ reviewedText: String) -> String {
        """
        # Build brief — \(title)

        \(reviewedText)

        Source note: \(title)
        EEON note ID: \(id.uuidString)
        Source: \(label)
        Using the EEON connector, call get_note with id \(id.uuidString) to read the original context. Resolve open questions before acting. This brief was reviewed in EEON; it does not authorize deployment, purchases, or external messages.
        """
    }
}

struct BuildBriefPreview: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    let note: Note
    let source: BuildBriefSource
    @State private var draft = ""
    @State private var loading = true
    @State private var started = false
    @State private var errorMessage: String?
    @FocusState private var editing: Bool

    private var canSave: Bool {
        !loading && !draft.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 16) {
                Text("Review the brief, adjust it, then copy it to your agent.")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                NavigationLink {
                    ScrollView {
                        VStack(alignment: .leading, spacing: 16) {
                            Text(source.title).font(.headline)
                            Text(source.label).font(.caption).foregroundStyle(.secondary)
                            Text(source.text)
                                .textSelection(.enabled)
                                .accessibilityIdentifier("buildBriefSourceText")
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }.padding()
                    }
                    .navigationTitle("Source note")
                    .navigationBarTitleDisplayMode(.inline)
                } label: {
                    Label("View source", systemImage: "text.quote")
                }
                if loading {
                    ProgressView("Preparing your brief…")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if draft.isEmpty, let errorMessage {
                    Text(errorMessage).foregroundStyle(.secondary)
                    Spacer()
                } else {
                    TextEditor(text: $draft)
                        .focused($editing)
                        .accessibilityIdentifier("buildBriefEditor")
                        .accessibilityLabel("Build brief text")
                    if let errorMessage {
                        Text(errorMessage).font(.footnote).foregroundStyle(.red)
                    }
                }
                Text("Your source note and summary are kept. Copying does not send or run anything.")
                    .font(.caption).foregroundStyle(.secondary)
                Button {
                    guard saveBrief() else { return }
                    UIPasteboard.general.string = source.handoff(draft)
                    dismiss()
                } label: {
                    Label("Copy for agent", systemImage: "doc.on.doc")
                        .frame(maxWidth: .infinity).padding(.vertical, 6)
                }
                .buttonStyle(.borderedProminent)
                .disabled(!canSave)
            }
            .padding()
            .navigationTitle("Build brief")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save brief") {
                        if saveBrief() { dismiss() }
                    }.disabled(!canSave)
                }
                ToolbarItemGroup(placement: .keyboard) {
                    Spacer()
                    Button("Done editing") { editing = false }
                }
            }
            .task { await loadBrief() }
        }
        .tint(Color.eeonAccent)
        .presentationDetents([.large])
        .interactiveDismissDisabled(loading || editing)
    }

    @MainActor
    private func loadBrief() async {
        guard !started else { return }
        started = true
        defer { loading = false }
        if let saved = source.savedBrief(in: note) {
            draft = saved
            return
        }
        do {
            draft = try await RewriteService.rewrite(
                transcript: source.text,
                template: RewriteTemplateCatalog.buildBrief,
                maxTokens: 2200,
                includePersonalContext: false
            )
            try Task.checkCancellation()
        } catch is CancellationError {
            // Leaving the preview cancels the request without modifying the note.
        } catch {
            errorMessage = "Couldn't prepare the brief. Your note is safe. Close this preview and try again."
        }
    }

    @MainActor
    private func saveBrief() -> Bool {
        guard canSave else { return false }
        guard BuildBriefSource(note: note).text == source.text else {
            errorMessage = "The source note changed. Close this preview and reopen Build brief to use the updated note."
            return false
        }
        let previous = (note.activeRewriteText, note.activeRewriteType, note.updatedAt)
        note.activeRewriteText = draft
        note.activeRewriteType = source.storageKey
        note.updatedAt = Date()
        do {
            try modelContext.save()
            return true
        } catch {
            note.activeRewriteText = previous.0
            note.activeRewriteType = previous.1
            note.updatedAt = previous.2
            errorMessage = "Couldn't save the brief. Your edits are still here; please try again."
            return false
        }
    }
}
