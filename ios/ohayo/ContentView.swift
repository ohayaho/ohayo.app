import SwiftUI
import WebKit
import UIKit

struct ContentView: UIViewRepresentable {
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")

        // Bridge: JS calls window.webkit.messageHandlers.haptic.postMessage("light" | "medium" | "success")
        config.userContentController.add(context.coordinator, name: "haptic")

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.scrollView.bounces = false
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.contentInsetAdjustmentBehavior = .never

        if let htmlURL = Bundle.main.url(forResource: "index", withExtension: "html") {
            webView.loadFileURL(htmlURL, allowingReadAccessTo: htmlURL.deletingLastPathComponent())
        }

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    // Receives haptic requests from the web layer and plays native feedback.
    final class Coordinator: NSObject, WKScriptMessageHandler {
        private let impactLight = UIImpactFeedbackGenerator(style: .light)
        private let impactMedium = UIImpactFeedbackGenerator(style: .medium)
        private let notify = UINotificationFeedbackGenerator()

        func userContentController(_ userContentController: WKUserContentController,
                                   didReceive message: WKScriptMessage) {
            guard message.name == "haptic", let type = message.body as? String else { return }
            switch type {
            case "light":
                impactLight.prepare()
                impactLight.impactOccurred()
            case "medium":
                impactMedium.prepare()
                impactMedium.impactOccurred()
            case "success":
                notify.prepare()
                notify.notificationOccurred(.success)
            default:
                break
            }
        }
    }
}
