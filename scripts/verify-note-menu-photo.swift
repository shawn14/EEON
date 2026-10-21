// Decode the actual image saved by the app, after its relaunch persistence check.
import Foundation
import ImageIO

func image(_ path: String) throws -> CGImage {
    let options = [kCGImageSourceShouldCacheImmediately: true] as CFDictionary
    guard let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, options) else {
        throw NSError(domain: "EEONPhotoProof", code: 1, userInfo: [NSLocalizedDescriptionKey: "Actual image does not decode"])
    }
    return image
}

do {
    guard CommandLine.arguments.count == 3 else {
        throw NSError(domain: "EEONPhotoProof", code: 2)
    }
    let saved = try image(CommandLine.arguments[1])
    let fixture = try image(CommandLine.arguments[2])
    guard saved.width == fixture.width, saved.height == fixture.height else {
        throw NSError(domain: "EEONPhotoProof", code: 3, userInfo: [NSLocalizedDescriptionKey: "Saved image dimensions differ from selected fixture"])
    }
    let receipt: [String: Any] = ["saved_image_decodes": true, "width": saved.width, "height": saved.height]
    print(String(decoding: try JSONSerialization.data(withJSONObject: receipt, options: [.sortedKeys]), as: UTF8.self))
} catch {
    fputs("Photo proof failed: \(error.localizedDescription)\n", stderr)
    exit(1)
}
