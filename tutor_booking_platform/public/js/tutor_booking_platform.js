/**
 * Tutor Booking Platform — Desk Cleanup Script
 *
 * Removes floating cart widgets injected by other apps
 * (specifically Construction Marketplace and Pharmacy Management)
 * from the Desk. These e-commerce widgets are irrelevant on
 * a Tutor Booking Platform workspace.
 *
 * Frappe loads all public/js/*.js from every installed app globally,
 * so this script runs on every Desk page.
 */

(function() {
    "use strict";

    // ─── IDs and classes to remove ─────────────────────────────────────
    // These are injected by construction_marketplace/public/js/...bundle.js
    const CART_SELECTORS = [
        "#floating-cart-widget",
        "#floating-cart-btn",
        "#mini-cart-overlay",
        "#mini-cart-panel",
        "#cart-count-badge",
        ".mini-cart-header",
        ".mini-cart-body",
        ".mini-cart-footer",
        ".mini-cart-empty",
        ".mini-cart-checkout-btn",
    ];

    /**
     * Remove all cart widget elements from the DOM.
     */
    function removeCartWidgets() {
        CART_SELECTORS.forEach(function(selector) {
            document.querySelectorAll(selector).forEach(function(el) {
                el.remove();
            });
        });
    }

    // ─── Run immediately (DOM already exists for static parts) ────────
    removeCartWidgets();

    // ─── Also observe for dynamically injected widgets ───────────────
    // Construction Marketplace's JS injects the cart widget after page load,
    // so we need a MutationObserver to catch it.
    var observer = new MutationObserver(function() {
        removeCartWidgets();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });

    // ─── Stop observing after 10 seconds to avoid performance impact ──
    setTimeout(function() {
        observer.disconnect();
    }, 10000);

})();
