// Inspect files produced by the real app UI, never substitute export logic.
import Foundation
import PDFKit

func require(_ condition: Bool, _ message: String) throws {
    if !condition { throw NSError(domain: "EEONMenuProof", code: 1, userInfo: [NSLocalizedDescriptionKey: message]) }
}

do {
    guard CommandLine.arguments.count == 3 else {
        throw NSError(domain: "EEONMenuProof", code: 2, userInfo: [NSLocalizedDescriptionKey: "Expected app container and original audio fixture paths"])
    }
    let container = URL(fileURLWithPath: CommandLine.arguments[1])
    let exports = container.appendingPathComponent("tmp/note-exports")
    let base = exports.appendingPathComponent("Paywall launch call")
    let markdown = try String(contentsOf: base.appendingPathExtension("md"), encoding: .utf8)
    try require(markdown.contains("# Paywall launch call") && markdown.contains("Thursday night"), "Markdown export lost title or actual transcript")
    let pdfURL = base.appendingPathExtension("pdf")
    guard let pdf = PDFDocument(url: pdfURL) else {
        throw NSError(domain: "EEONMenuProof", code: 3, userInfo: [NSLocalizedDescriptionKey: "Export is not a readable PDF"])
    }
    let pdfText = pdf.string ?? ""
    try require(pdf.pageCount > 0 && pdfText.contains("Paywall launch call") && pdfText.contains("Thursday night"), "PDF export is empty or lost actual note text")
    let audio = try Data(contentsOf: base.appendingPathExtension("m4a"))
    let original = try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[2]))
    try require(!audio.isEmpty && audio == original, "Recording export differs from the actual original audio")
    let receipt: [String: Any] = ["markdown_note_text": true, "pdf_note_text": true, "pdf_pages": pdf.pageCount, "recording_matches_original": true, "recording_bytes": audio.count]
    let json = try JSONSerialization.data(withJSONObject: receipt, options: [.prettyPrinted, .sortedKeys])
    print(String(decoding: json, as: UTF8.self))
} catch {
    fputs("File proof failed: \(error.localizedDescription)\n", stderr)
    exit(1)
}
