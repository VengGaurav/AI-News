document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.news-card');
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease-in-out';
            card.style.opacity = 1;
        }, index * 150);
    });

    // Theme toggle
    const root = document.documentElement;
    const themeSwitch = document.getElementById('themeSwitch');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) root.setAttribute('data-theme', savedTheme);
    if (themeSwitch) {
        // initialize state
        themeSwitch.checked = root.getAttribute('data-theme') === 'dark';
        themeSwitch.addEventListener('change', () => {
            const current = themeSwitch.checked ? 'dark' : 'light';
            root.setAttribute('data-theme', current);
            localStorage.setItem('theme', current);
        });
    }

    // Relative time for published dates
    const publishedNodes = document.querySelectorAll('.published');
    const toRelative = (iso) => {
        if (!iso) return '';
        const now = new Date();
        const then = new Date(iso);
        const diffMs = now - then;
        if (Number.isNaN(diffMs)) return '';
        const sec = Math.floor(diffMs / 1000);
        const min = Math.floor(sec / 60);
        const hr = Math.floor(min / 60);
        const day = Math.floor(hr / 24);
        if (sec < 60) return 'just now';
        if (min < 60) return `${min} min ago`;
        if (hr < 24) return `${hr} hr${hr > 1 ? 's' : ''} ago`;
        if (day < 7) return `${day} day${day > 1 ? 's' : ''} ago`;
        return then.toISOString().slice(0, 10);
    };
    publishedNodes.forEach(node => {
        const iso = node.getAttribute('data-published');
        const textEl = node.querySelector('.published-text');
        const rel = toRelative(iso);
        if (textEl && rel) textEl.textContent = rel;
    });

    // Image fallback renderer: if onerror fired and we have data-fallback-text, swap to a styled fallback node
    window.handleImgError = (img) => {
        const text = img.getAttribute('data-fallback-text') || 'News';
        const container = document.createElement('div');
        container.className = 'thumb-fallback';
        const span = document.createElement('span');
        span.textContent = text;
        container.appendChild(span);
        img.replaceWith(container);
    };

    // Simulated market ticker (static sample). Replace with API later.
    const sample = [
        { s: 'NIFTY 50', p: '+0.76%' },
        { s: 'SENSEX', p: '+0.42%' },
        { s: 'USD/INR', p: '-0.18%' },
        { s: 'BTC', p: '+1.45%' },
        { s: 'GOLD', p: '-0.21%' },
    ];
    const track = document.getElementById('tickerTrack');
    if (track) {
        const fragment = document.createDocumentFragment();
        // Duplicate items so CSS animation can loop seamlessly
        [...sample, ...sample].forEach(item => {
            const span = document.createElement('span');
            span.className = `ticker-item ${item.p.startsWith('+') ? 'up' : 'down'}`;
            span.textContent = `${item.s} ${item.p}`;
            fragment.appendChild(span);
        });
        track.appendChild(fragment);
    }

    // Trending list (derive from headlines on page)
    const trending = document.getElementById('trendingList');
    if (trending) {
        const titles = Array.from(document.querySelectorAll('.card-title'))
            .slice(0, 8)
            .map(el => el.textContent.trim())
            .filter(Boolean);
        if (titles.length) {
            titles.forEach((t, i) => {
                const li = document.createElement('li');
                li.textContent = t;
                li.setAttribute('aria-posinset', String(i + 1));
                trending.appendChild(li);
            });
        }
    }

    // Search hero: trim, handle empty, and keep category
    const searchForm = document.querySelector('.search-hero__form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            const input = searchForm.querySelector('.search-hero__input');
            const raw = input ? input.value : '';
            const q = (raw || '').trim();
            if (!q) {
                // Remove search param from URL for a clean state
                e.preventDefault();
                const url = new URL(window.location.href);
                url.searchParams.delete('search');
                // Keep category if present via hidden input or current URL
                const hiddenCat = searchForm.querySelector('input[name="category"]');
                if (hiddenCat && hiddenCat.value) {
                    url.searchParams.set('category', hiddenCat.value);
                }
                window.location.assign(url.toString());
                return;
            }
            // Trimmed value back into input to avoid trailing spaces in query
            input.value = q;
        });
    }
});
