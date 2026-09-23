var langCache = {};

async function setLanguage(lang) {
  try {
    if (!langCache[lang]) {
      var response = await fetch('locales/' + lang + '.json');
      if (!response.ok) throw new Error('Language file not found: ' + lang);
      langCache[lang] = await response.json();
    }

    var translations = langCache[lang];
    document.documentElement.lang = lang;

    if (lang === 'ar') {
      document.documentElement.setAttribute('dir', 'rtl');
    } else {
      document.documentElement.removeAttribute('dir');
    }

    var applyTranslations = function () {
      document.querySelectorAll('[data-i18n]').forEach(function (element) {
        var key = element.getAttribute('data-i18n');
        if (translations[key] !== undefined) {
          element.innerHTML = translations[key];
        }
      });
    };

    if (typeof window.refreshAnimations === 'function') {
      window.refreshAnimations(applyTranslations);
    } else {
      applyTranslations();
    }
  } catch (error) {
    console.error('Error loading language:', error);
  }
}
