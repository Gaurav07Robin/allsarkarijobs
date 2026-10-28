/**
 * AllSarkariJobs Bilingual Language Switcher (Hindi / English)
 * 100% Clean UX: Completely suppresses Google Translate top banner, iframes & popups.
 * Automatic single-click language switching across the entire website.
 */

(function () {
  const STORAGE_KEY = 'allsarkarijobs_lang';
  const COOKIE_KEY = 'googtrans';

  function getSavedLang() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved === 'hi' || saved === 'en') return saved;
      const match = document.cookie.match(/googtrans=\/en\/([a-z]{2})/i);
      if (match && (match[1] === 'hi' || match[1] === 'en')) return match[1];
    } catch (e) {}
    return 'en';
  }

  function setTranslateCookie(lang) {
    const val = lang === 'hi' ? '/en/hi' : '/en/en';
    const expires = 'expires=' + new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toUTCString();
    
    // Set for root path
    document.cookie = `${COOKIE_KEY}=${val}; path=/; ${expires}`;
    
    const host = window.location.hostname;
    document.cookie = `${COOKIE_KEY}=${val}; path=/; domain=${host}; ${expires}`;
    if (host.includes('.')) {
      const parts = host.split('.');
      if (parts.length >= 2) {
        const rootDomain = '.' + parts.slice(-2).join('.');
        document.cookie = `${COOKIE_KEY}=${val}; path=/; domain=${rootDomain}; ${expires}`;
      }
    }
  }

  function clearTranslateCookies() {
    const expires = 'expires=Thu, 01 Jan 1970 00:00:00 UTC';
    const paths = ['/', '/admission', window.location.pathname];
    const host = window.location.hostname;
    const domains = ['', host, '.' + host];
    if (host.includes('.')) {
      domains.push('.' + host.split('.').slice(-2).join('.'));
    }

    paths.forEach(p => {
      domains.forEach(d => {
        document.cookie = `${COOKIE_KEY}=; path=${p}; ${expires};` + (d ? ` domain=${d};` : '');
        document.cookie = `${COOKIE_KEY}=/en/en; path=${p}; ${expires};` + (d ? ` domain=${d};` : '');
      });
    });
  }

  // Aggressive Suppressor: Kill Google Translate top banner & body shifts instantly
  function killGoogleBanner() {
    // 1. Remove all banner iframes
    const iframes = document.querySelectorAll('.goog-te-banner-frame, iframe[class*="goog-te-banner"], iframe[id*="goog-te-banner"]');
    iframes.forEach(el => {
      el.style.display = 'none';
      el.style.visibility = 'hidden';
      el.style.height = '0px';
      el.style.width = '0px';
      el.remove();
    });

    // 2. Prevent body from being pushed down
    if (document.body) {
      if (document.body.style.top && document.body.style.top !== '0px') {
        document.body.style.setProperty('top', '0px', 'important');
      }
      if (document.body.style.position === 'relative') {
        document.body.style.setProperty('position', 'static', 'important');
      }
    }
    if (document.documentElement) {
      if (document.documentElement.style.top && document.documentElement.style.top !== '0px') {
        document.documentElement.style.setProperty('top', '0px', 'important');
      }
    }
  }

  // Observe and kill banner as soon as it appears
  try {
    const observer = new MutationObserver(killGoogleBanner);
    observer.observe(document.documentElement, { childList: true, subtree: true, attributes: true });
  } catch (e) {}
  setInterval(killGoogleBanner, 150);

  // Inject CSS directly
  function injectStyles() {
    if (document.getElementById('siteLangStyles')) return;
    const style = document.createElement('style');
    style.id = 'siteLangStyles';
    style.textContent = `
      /* Header Navigation Spacing & Logo Separation */
      .hdr-inner, .header-inner {
        display: flex !important;
        align-items: center !important;
        gap: 16px !important;
      }
      .hdr-inner a.logo, .header-inner a.logo, a.logo {
        margin-right: 28px !important;
        flex-shrink: 0 !important;
      }
      .hdr-inner .nav-links, .header-inner .desktop-nav, ul.nav-links {
        margin-right: auto !important;
      }

      /* Top-Right Language Switcher Pill */
      .site-lang-switch {
        display: inline-flex !important;
        align-items: center !important;
        background: rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(15, 23, 42, 0.15) !important;
        border-radius: 20px !important;
        padding: 2px !important;
        gap: 2px !important;
        margin-left: auto !important;
        vertical-align: middle !important;
        box-sizing: border-box !important;
        flex-shrink: 0 !important;
        white-space: nowrap !important;
        z-index: 101 !important;
      }
      .hdr-inner .site-lang-switch,
      .header .hdr-inner .site-lang-switch,
      .header[style*="navy"] .site-lang-switch {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
      }
      .lang-tab-btn {
        background: transparent !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 4px 10px !important;
        font-size: 11.5px !important;
        font-weight: 700 !important;
        color: inherit !important;
        opacity: 0.75 !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
        line-height: 1.2 !important;
        font-family: inherit !important;
        text-decoration: none !important;
      }
      .lang-tab-btn:hover {
        opacity: 1 !important;
      }
      .lang-tab-btn.active {
        background: #9a5b28 !important;
        color: #ffffff !important;
        opacity: 1 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.18) !important;
      }
      .hdr-inner .lang-tab-btn.active {
        background: #059669 !important;
        color: #ffffff !important;
      }

      /* 100% Complete Google Translate Banner & Popup Destruction */
      .goog-te-banner-frame,
      .goog-te-banner-frame.skiptranslate,
      iframe.goog-te-banner-frame,
      iframe.skiptranslate,
      #goog-gt-tt,
      .goog-te-balloon-frame,
      .goog-tooltip,
      .goog-tooltip:hover {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
        opacity: 0 !important;
        pointer-events: none !important;
        border: none !important;
      }
      body {
        top: 0px !important;
        position: static !important;
      }
      html {
        top: 0px !important;
      }
      .goog-text-highlight {
        background: none !important;
        box-shadow: none !important;
      }
      #google_translate_element {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
      }
      font[style] {
        background: none !important;
        box-shadow: none !important;
      }
    `;
    (document.head || document.documentElement).appendChild(style);
  }

  function updateSwitchUI(lang) {
    const btnEn = document.getElementById('btnLangEn');
    const btnHi = document.getElementById('btnLangHi');
    if (btnEn) btnEn.classList.toggle('active', lang === 'en');
    if (btnHi) btnHi.classList.toggle('active', lang === 'hi');
  }

  function triggerGoogleCombo(targetLang) {
    const combo = document.querySelector('.goog-te-combo');
    if (!combo) return false;

    if (targetLang === 'hi') {
      combo.value = 'hi';
      combo.dispatchEvent(new Event('change'));
      return true;
    } else {
      // Revert to English
      combo.value = 'en';
      combo.dispatchEvent(new Event('change'));
      // In some versions, original language is value ''
      setTimeout(() => {
        if (combo.value !== 'en' && combo.value !== '') {
          combo.selectedIndex = 0;
          combo.dispatchEvent(new Event('change'));
        }
      }, 100);
      return true;
    }
  }

  window.switchLanguage = function (lang) {
    if (lang !== 'en' && lang !== 'hi') lang = 'en';

    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {}

    updateSwitchUI(lang);

    if (lang === 'hi') {
      setTranslateCookie('hi');
      const triggered = triggerGoogleCombo('hi');
      if (!triggered) {
        // Poll for combo up to 2 seconds
        let checks = 0;
        const interval = setInterval(() => {
          checks++;
          if (triggerGoogleCombo('hi') || checks > 30) {
            clearInterval(interval);
          }
        }, 60);
      }
    } else {
      // Switching to English
      clearTranslateCookies();
      const triggered = triggerGoogleCombo('en');
      if (!triggered) {
        // Clean fast reload without any popup
        window.location.reload();
      } else {
        setTimeout(() => {
          // If still translated, clean reload
          if (document.cookie.includes('googtrans=/en/hi')) {
            clearTranslateCookies();
            window.location.reload();
          }
        }, 300);
      }
    }

    killGoogleBanner();
  };

  // Mount Switcher HTML into Top Right Header
  function mountSwitcher() {
    if (document.getElementById('siteLangSwitch')) {
      updateSwitchUI(getSavedLang());
      return;
    }

    const target = document.querySelector('.hdr-right') || 
                   document.querySelector('.header-inner') || 
                   document.querySelector('.hdr-inner') || 
                   document.querySelector('.header .container') ||
                   document.querySelector('.header');

    if (!target) return;

    const switcher = document.createElement('div');
    switcher.className = 'site-lang-switch';
    switcher.id = 'siteLangSwitch';
    switcher.setAttribute('role', 'group');
    switcher.setAttribute('aria-label', 'Language Switcher / भाषा चयन');
    switcher.innerHTML = `
      <button type="button" class="lang-tab-btn" id="btnLangEn" onclick="window.switchLanguage('en')" title="Switch to English">English</button>
      <button type="button" class="lang-tab-btn" id="btnLangHi" onclick="window.switchLanguage('hi')" title="हिन्दी में बदलें">हिन्दी</button>
    `;

    const ham = target.querySelector('.hamburger');
    if (ham) {
      target.insertBefore(switcher, ham);
    } else {
      target.appendChild(switcher);
    }

    updateSwitchUI(getSavedLang());
  }

  // Pre-load Google Translate Engine in background
  function initGoogleTranslate() {
    if (!document.getElementById('google_translate_element')) {
      const gdiv = document.createElement('div');
      gdiv.id = 'google_translate_element';
      gdiv.style.display = 'none';
      document.body.appendChild(gdiv);
    }

    window.googleTranslateElementInit = function () {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'hi,en',
        autoDisplay: false
      }, 'google_translate_element');
      killGoogleBanner();
    };

    if (!document.getElementById('googleTranslateScript')) {
      const script = document.createElement('script');
      script.id = 'googleTranslateScript';
      script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      script.async = true;
      document.body.appendChild(script);
    }
  }

  // Initial language setup
  const initialLang = getSavedLang();
  if (initialLang === 'hi') {
    setTranslateCookie('hi');
  } else {
    clearTranslateCookies();
  }

  injectStyles();
  killGoogleBanner();

  function boot() {
    injectStyles();
    mountSwitcher();
    initGoogleTranslate();
    killGoogleBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
