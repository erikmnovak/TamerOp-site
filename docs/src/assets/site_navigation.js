/* Progressive enhancement of native catalog links/disclosures and Documenter search. */
(() => {
    "use strict";
    const start = () => {
        const sidebar = document.getElementById("site-navigation");
        const trigger = document.getElementById("documenter-sidebar-button");
        const main = document.querySelector("#documenter > .docs-main");
        const source = document.getElementById("site-catalog");
        if (!sidebar || !trigger || !main || !source) return;
        const catalog = JSON.parse(source.textContent);
        const siteRoot = new URL(catalog.root, document.baseURI);
        const menu = sidebar.querySelector(".site-collections");
        const branches = [...menu.querySelectorAll("details")];
        const storageKey = "tamerop-navigation-v1:" + siteRoot.pathname;
        const branchKey = node => {
            const collection = node.closest("[data-collection]").dataset.collection;
            return node.dataset.topic ? collection + "/" + node.dataset.topic : collection;
        };
        let saved = null;
        try { saved = JSON.parse(sessionStorage.getItem(storageKey)); } catch (_) { /* Storage is optional. */ }
        // Native HTML already opens the current path without JavaScript. Restore
        // other choices too; never let a saved closed branch hide this page.
        for (const branch of branches) {
            const context = branch.matches('.site-topic') ? branch.parentElement : branch;
            branch.open = Boolean(context.querySelector('[aria-current="page"]')) ||
                (typeof saved?.branches?.[branchKey(branch)] === "boolean"
                    ? saved.branches[branchKey(branch)] : branch.open);
        }
        for (const entry of menu.querySelectorAll('.site-topic-entry')) {
            const branch = entry.querySelector('.site-topic');
            const button = entry.querySelector('.site-topic-toggle');
            function syncTopicButton() {
                button.setAttribute('aria-expanded', String(branch.open));
                button.setAttribute('aria-label',
                    `${branch.open ? 'Collapse' : 'Expand'} articles under ${button.dataset.title}`);
            }
            button.addEventListener('click', () => {
                branch.open = !branch.open;
                syncTopicButton();
                rememberNavigation();
            });
            branch.addEventListener('toggle', syncTopicButton);
            syncTopicButton();
            button.hidden = false;
            entry.dataset.enhanced = 'true';
        }
        function rememberNavigation() {
            try {
                sessionStorage.setItem(storageKey, JSON.stringify({
                    branches: Object.fromEntries(branches.map(node => [branchKey(node), node.open])),
                    scroll: menu.scrollTop, sidebarScroll: sidebar.scrollTop,
                    page: location.pathname
                }));
            } catch (_) { /* Private browsing or blocked storage must not break navigation. */ }
        }
        // Restore after layout, including the short-screen sidebar scroll area.
        // On a new page, move only as far as needed to reveal its active link.
        requestAnimationFrame(() => {
            if (Number.isFinite(saved?.scroll)) menu.scrollTop = Math.max(0, saved.scroll);
            if (Number.isFinite(saved?.sidebarScroll)) sidebar.scrollTop = Math.max(0, saved.sidebarScroll);
            const active = menu.querySelector('[aria-current="page"]');
            if (active && saved?.page !== location.pathname) {
                const scroller = getComputedStyle(menu).overflowY === "auto" ? menu : sidebar;
                const bounds = scroller.getBoundingClientRect(), item = active.getBoundingClientRect();
                if (item.bottom > bounds.bottom) scroller.scrollTop += item.bottom - bounds.bottom + 8;
                else if (item.top < bounds.top) scroller.scrollTop -= bounds.top - item.top + 8;
            }
            for (const branch of branches) branch.addEventListener("toggle", rememberNavigation);
        });
        // Capture before the mobile drawer closes and page navigation begins.
        sidebar.addEventListener("click", event => {
            if (event.target.closest("a[href]")) rememberNavigation();
        }, true);
        window.addEventListener("pagehide", rememberNavigation);
        document.body.classList.add("site-js");
        const narrow = window.matchMedia("(max-width: 1055px)");
        const wideOutline = window.matchMedia("(min-width: 1440px)");
        const closeButton = sidebar.querySelector(".site-nav-close");
        const backdrop = document.createElement("button");
        backdrop.type = "button";
        backdrop.className = "site-nav-backdrop";
        backdrop.tabIndex = -1;
        backdrop.setAttribute("aria-label", "Close navigation");
        sidebar.after(backdrop);
        let previousFocus = trigger;

        function setOpen(open, restore = true) {
            open = narrow.matches && open;
            sidebar.classList.toggle("visible", open);
            document.body.classList.toggle("site-nav-open", open);
            trigger.setAttribute("aria-expanded", String(open));
            trigger.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
            sidebar.inert = narrow.matches && !open;
            main.inert = open;
            if (open) {
                previousFocus = document.activeElement;
                closeButton.focus();
            } else if (restore && narrow.matches) {
                (previousFocus && previousFocus.isConnected ? previousFocus : trigger).focus();
            }
        }
        // Capture prevents Documenter's own jQuery handler from toggling twice.
        trigger.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopImmediatePropagation();
            setOpen(!sidebar.classList.contains("visible"));
        }, true);
        closeButton.addEventListener("click", () => setOpen(false));
        backdrop.addEventListener("click", () => setOpen(false));
        narrow.addEventListener("change", () => setOpen(false, false));
        setOpen(false, false);
        document.addEventListener("keydown", (event) => {
            if (!narrow.matches || !sidebar.classList.contains("visible")) return;
            // Documenter's search modal owns its own keyboard/focus while open.
            if (document.getElementById("search-modal")?.classList.contains("is-active")) return;
            if (event.key === "Escape") {
                event.preventDefault();
                setOpen(false);
            } else if (event.key === "Tab") {
                const focusable = [...sidebar.querySelectorAll("a[href], button, summary, select")]
                    .filter(node => !node.disabled && node.getClientRects().length > 0);
                const first = focusable[0], last = focusable[focusable.length - 1];
                if (event.shiftKey && document.activeElement === first) {
                    event.preventDefault(); last?.focus();
                } else if (!event.shiftKey && document.activeElement === last) {
                    event.preventDefault(); first?.focus();
                }
            }
        });
        sidebar.addEventListener("click", (event) => {
            if (event.target.closest("a[href]") && narrow.matches) setOpen(false, false);
        });
        // Opening search from a drawer releases the article before the modal opens.
        const searchButton = document.getElementById("documenter-search-query");
        let searchOrigin = searchButton;
        let searchWasOpen = false;
        searchButton.addEventListener("click", () => {
            searchOrigin = searchButton;
            if (narrow.matches) setOpen(false, false);
        }, true);
        document.addEventListener("keydown", (event) => {
            if ((event.ctrlKey || event.metaKey) && event.key === "/") {
                searchOrigin = document.activeElement;
                if (narrow.matches) setOpen(false, false);
            }
        }, true);
        function syncSearchFocus() {
            const open = Boolean(document.getElementById("search-modal")?.classList.contains("is-active"));
            if (searchWasOpen && !open) {
                const destination = narrow.matches ? trigger : searchOrigin;
                if (destination?.isConnected) destination.focus();
            }
            searchWasOpen = open;
        }

        const outline = document.querySelector(".site-outline-disclosure");
        if (outline) {
            const adjustOutline = () => { outline.open = wideOutline.matches; };
            adjustOutline();
            wideOutline.addEventListener("change", adjustOutline);
            outline.querySelector("summary").addEventListener("click", (event) => {
                if (wideOutline.matches) event.preventDefault();
            });
        }

        function annotateSearch() {
            for (const result of document.querySelectorAll(".search-result-link")) {
                if (result.querySelector(".site-result-context")) continue;
                const url = new URL(result.href, document.baseURI);
                if (url.origin !== siteRoot.origin || !url.pathname.startsWith(siteRoot.pathname)) continue;
                const path = decodeURIComponent(url.pathname.slice(siteRoot.pathname.length));
                const record = catalog.pages[path];
                if (!record) continue;
                const context = document.createElement("div");
                context.className = "site-result-context site-search-meta";
                const type = document.createElement("span");
                type.className = "site-result-type";
                type.textContent = record.type_label;
                context.append(type);
                const topics = (record.topics || []).map(id => catalog.topics[id]).filter(Boolean);
                if (topics.length) {
                    const subject = document.createElement("span");
                    subject.className = "site-result-topics";
                    subject.textContent = topics.join(" · ");
                    context.append(subject);
                }
                result.insertBefore(context, result.children[1] || null);
            }
        }
        // Documenter 1.19 replaces .search-modal-card-body after every query/filter.
        // Observe inserted results, including results rendered after lazy search setup.
        let queued = false;
        new MutationObserver((changes) => {
            if (changes.some(change => change.target.id === "search-modal" ||
                [...change.addedNodes].some(node => node.id === "search-modal"))) syncSearchFocus();
            if (queued || !changes.some(change => [...change.addedNodes].some(node =>
                node.nodeType === Node.ELEMENT_NODE &&
                (node.matches(".search-result-link") || node.querySelector(".search-result-link"))))) return;
            queued = true;
            queueMicrotask(() => { queued = false; annotateSearch(); });
        }).observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ["class"]});
        syncSearchFocus();
        annotateSearch();
    };
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
    else start();
})();
