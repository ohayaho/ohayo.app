import SwiftUI
import WebKit
import UIKit
import StoreKit

// Single non-consumable unlock for all premium editing features.
let kPremiumProductID = "app.ohayo.ohayo.premium"
// The card-back / clear images may each be set this many times for free;
// further changes need premium. Keep the two counts aligned (product decision).
let kFreeCardBackChanges = 2
let kFreeClearChanges = 2

#if DEBUG
// TESTING ONLY: force premium unlocked in Debug builds so paid features can be
// checked on-device without a real purchase. Release/Archive builds ignore this.
let kDebugForcePremium = true
#endif

struct ContentView: UIViewRepresentable {
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")

        // Bridge: JS calls window.webkit.messageHandlers.haptic.postMessage("light" | "medium" | "success")
        config.userContentController.add(context.coordinator, name: "haptic")
        // Bridge: JS calls window.webkit.messageHandlers.store.postMessage({cmd:"getStatus"|"purchase"|"restore"|"consumeCardBack"})
        config.userContentController.add(context.coordinator, name: "store")

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.scrollView.bounces = false
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        // Only allow Safari Web Inspector in debug builds; release WebView stays non-inspectable
        // so the premium gate can't be tampered with via devtools on shipped builds.
        #if DEBUG
        if #available(iOS 16.4, *) { webView.isInspectable = true }
        #endif

        context.coordinator.webView = webView
        webView.navigationDelegate = context.coordinator

        if let htmlURL = Bundle.main.url(forResource: "index", withExtension: "html") {
            webView.loadFileURL(htmlURL, allowingReadAccessTo: htmlURL.deletingLastPathComponent())
        }

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    // Receives haptic + store requests from the web layer.
    final class Coordinator: NSObject, WKScriptMessageHandler, WKNavigationDelegate {
        weak var webView: WKWebView?
        private let store = Store.shared
        private let impactLight = UIImpactFeedbackGenerator(style: .light)
        private let impactMedium = UIImpactFeedbackGenerator(style: .medium)
        private let notify = UINotificationFeedbackGenerator()

        func userContentController(_ userContentController: WKUserContentController,
                                   didReceive message: WKScriptMessage) {
            switch message.name {
            case "haptic":
                guard let type = message.body as? String else { return }
                handleHaptic(type)
            case "store":
                let cmd = (message.body as? [String: Any])?["cmd"] as? String ?? ""
                handleStore(cmd)
            default:
                break
            }
        }

        // The app itself is a local file:// page. Anything that would leave it
        // (mailto:, tel:, http(s) links like the privacy policy / terms) opens
        // in the system (Mail / Safari) instead of navigating the WebView away.
        func webView(_ webView: WKWebView,
                     decidePolicyFor navigationAction: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if let url = navigationAction.request.url,
               let scheme = url.scheme?.lowercased(),
               ["mailto", "tel", "http", "https"].contains(scheme) {
                UIApplication.shared.open(url)
                decisionHandler(.cancel)
                return
            }
            decisionHandler(.allow)
        }

        private func handleHaptic(_ type: String) {
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

        private func handleStore(_ cmd: String) {
            Task { @MainActor in
                switch cmd {
                case "getStatus":
                    await store.load()
                    pushState()
                case "purchase":
                    let ok = await store.purchase()
                    pushState(extra: ["purchaseResult": ok ? "success" : "failed"])
                case "restore":
                    await store.restore()
                    pushState(extra: ["restoreResult": "done"])
                case "consumeCardBack":
                    store.consumeCardBackChange()
                    pushState()
                case "consumeClear":
                    store.consumeClearChange()
                    pushState()
                default:
                    break
                }
            }
        }

        // Push the authoritative store state down to JS (window.OhayoStore.onState).
        @MainActor private func pushState(extra: [String: Any] = [:]) {
            var dict: [String: Any] = [
                "premium": store.isPremium,
                "available": store.product != nil,
                "canChangeCardBack": store.canChangeCardBack(),
                "cardBackChangesUsed": store.cardBackChangesUsed,
                "freeCardBackChanges": kFreeCardBackChanges,
                "canChangeClear": store.canChangeClear(),
                "clearChangesUsed": store.clearChangesUsed,
                "freeClearChanges": kFreeClearChanges,
            ]
            if let price = store.product?.displayPrice { dict["price"] = price }
            extra.forEach { dict[$0] = $1 }
            guard let data = try? JSONSerialization.data(withJSONObject: dict),
                  let json = String(data: data, encoding: .utf8) else { return }
            webView?.evaluateJavaScript("window.OhayoStore && window.OhayoStore.onState(\(json))",
                                        completionHandler: nil)
        }
    }
}

// MARK: - StoreKit 2 manager (authoritative source of truth for premium)

@MainActor
final class Store: ObservableObject {
    static let shared = Store()

    @Published private(set) var isPremium = false
    private(set) var product: Product?
    private var updatesTask: Task<Void, Never>?

    private let cardBackKey = "cardBackChangesUsed"
    private let clearKey    = "clearChangesUsed"

    init() {
        updatesTask = observeTransactionUpdates()
    }

    deinit { updatesTask?.cancel() }

    /// Fetch the product (once) and refresh ownership.
    func load() async {
        if product == nil { await fetchProducts() }
        await refreshEntitlements()
    }

    func fetchProducts() async {
        do {
            let products = try await Product.products(for: [kPremiumProductID])
            product = products.first
        } catch {
            // leave product nil; JS shows "一時的に購入できません" state
        }
    }

    func refreshEntitlements() async {
        var owned = false
        for await result in Transaction.currentEntitlements {
            guard case .verified(let transaction) = result else { continue }
            if transaction.productID == kPremiumProductID, transaction.revocationDate == nil {
                owned = true
            }
        }
        #if DEBUG
        if kDebugForcePremium { owned = true }   // debug-only override; never in Release
        #endif
        isPremium = owned
    }

    func purchase() async -> Bool {
        guard let product else { return false }
        do {
            let result = try await product.purchase()
            switch result {
            case .success(let verification):
                if case .verified(let transaction) = verification {
                    await transaction.finish()
                    await refreshEntitlements()
                    return isPremium
                }
                return false
            case .userCancelled, .pending:
                return false
            @unknown default:
                return false
            }
        } catch {
            return false
        }
    }

    func restore() async {
        try? await AppStore.sync()
        await refreshEntitlements()
    }

    private func observeTransactionUpdates() -> Task<Void, Never> {
        Task(priority: .background) { [weak self] in
            for await _ in Transaction.updates {
                await self?.refreshEntitlements()
            }
        }
    }

    // MARK: Free-change counters (native-owned; not reachable from JS/localStorage)

    var cardBackChangesUsed: Int { UserDefaults.standard.integer(forKey: cardBackKey) }

    func canChangeCardBack() -> Bool {
        isPremium || cardBackChangesUsed < kFreeCardBackChanges
    }

    func consumeCardBackChange() {
        guard !isPremium else { return }
        UserDefaults.standard.set(cardBackChangesUsed + 1, forKey: cardBackKey)
    }

    var clearChangesUsed: Int { UserDefaults.standard.integer(forKey: clearKey) }

    func canChangeClear() -> Bool {
        isPremium || clearChangesUsed < kFreeClearChanges
    }

    func consumeClearChange() {
        guard !isPremium else { return }
        UserDefaults.standard.set(clearChangesUsed + 1, forKey: clearKey)
    }
}
