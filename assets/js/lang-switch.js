// Mappa dei file privacy nella cartella dedicata
const PRIVACY_PAGES = {
  'it': 'privacy/it.html',
  'en': 'privacy/en.html',
  'de': 'privacy/de.html',
  'es': 'privacy/es.html',
  'fr': 'privacy/fr.html',
  'ja': 'privacy/ja.html',
  'ko': 'privacy/ko.html',
  'pt': 'privacy/pt.html',
  'ru': 'privacy/ru.html',
  'ar': 'privacy/ar.html',
  'zh': 'privacy/zh.html',
};

function getPreferredLanguage(supportedLangs) {
  const saved = localStorage.getItem('preferred_lang');
  if (saved && supportedLangs.includes(saved)) return saved;

  const browserLang = navigator.language.slice(0, 2);
  return supportedLangs.includes(browserLang) ? browserLang : 'en';
}

document.addEventListener('DOMContentLoaded', function() {
  const langSelect = document.getElementById('langSelect');
  if (!langSelect) return;

  const supportedLangs = Array.from(langSelect.options).map(o => o.value);
  const currentLang = getPreferredLanguage(supportedLangs);

  // Imposta il valore iniziale del selettore
  langSelect.value = currentLang;

  // Determina se siamo su una delle pagine privacy
  const currentPath = window.location.pathname;
  const isPrivacyPage = Object.values(PRIVACY_PAGES).some(file => currentPath.endsWith(file));

  // Funzione per aggiornare i link alla privacy presenti nella pagina (es. footer)
  function updatePrivacyLinks(lang) {
    const privacyFile = PRIVACY_PAGES[lang] || PRIVACY_PAGES['en'];
    document.querySelectorAll('a[href*="privacy"]').forEach(link => {
      link.href = privacyFile;
    });
  }

  // Se siamo nella Landing Page (index.html), applichiamo la traduzione dinamica iniziale
  if (!isPrivacyPage && typeof setLanguage === 'function') {
    setLanguage(currentLang);
  }

  // Aggiorna subito i link della privacy nel footer
  updatePrivacyLinks(currentLang);

  // Evento di cambio lingua
  langSelect.addEventListener('change', function(e) {
    const selectedLang = e.target.value;
    localStorage.setItem('preferred_lang', selectedLang);

    if (isPrivacyPage) {
      // Se siamo su una pagina privacy, reindirizza al file HTML della nuova lingua
      const targetFile = PRIVACY_PAGES[selectedLang] || PRIVACY_PAGES['en'];
      window.location.href = targetFile;
    } else {
      // Se siamo in index.html, traduci via JSON e aggiorna il footer
      if (typeof setLanguage === 'function') {
        setLanguage(selectedLang);
      }
      updatePrivacyLinks(selectedLang);
    }
  });
});