# Poesie — sito completo per GitHub Pages

Versione esportata il 29 settembre 2026. Il sito è indipendente da ChatGPT e Sites: HTML, CSS, JavaScript e immagini statiche, senza backend, chiavi API o servizi a pagamento necessari al funzionamento. I font sono caricati da Google Fonts; restano disponibili caratteri di sistema di riserva.

## Pubblicazione rapida

1. Estrai lo ZIP. Apri la cartella `poesie-github-pages`.
2. Copia **il suo contenuto** nella radice del repository GitHub destinato alla landing. Non caricare lo ZIP come unico file e non aggiungere un ulteriore livello di cartelle. Il repository deve contenere direttamente `docs/index.html`.
3. Fai commit e push sul ramo `main`. Puoi usare GitHub Desktop o l’interfaccia web di GitHub. Per un nuovo repository con GitHub Free, scegli un repository pubblico.
4. In **Settings → Pages → Build and deployment**, seleziona **Deploy from a branch**, ramo **main**, cartella **/docs**, poi **Save**.
5. In **Custom domain**, inserisci `poesieapp.it` e salva. Il file `docs/CNAME` è già incluso.
6. Controlla il DNS come descritto in `GUIDA-PUBBLICAZIONE.md`. Se il dominio è già collegato allo stesso account GitHub Pages, potrebbe essere già corretto.
7. Quando il certificato è disponibile, abilita **Enforce HTTPS**. Attendi che il deployment Pages sia completato.

La pubblicazione rende visibile il sito sul web. I termini mantengono l’avviso di bozza: verifica i contenuti legali prima del lancio definitivo, come indicato in `NOTE-REVISIONE.md`.

## Cosa contiene

| Percorso | Contenuto |
|---|---|
| `docs/` | Sito pronto da pubblicare, completo di immagini e script |
| `docs/it/`, `docs/en/`, ecc. | Landing nelle 11 lingue |
| `docs/privacy/` | Privacy originali nelle 11 lingue |
| `docs/terms/` | Termini d’uso separati nelle 11 lingue |
| `docs/CNAME` | Dominio `poesieapp.it` |
| `docs/.nojekyll` | Pubblicazione dei file statici senza elaborazione Jekyll |
| `content/` | Testi, traduzioni, template e privacy di origine modificabili |
| `generate.py` | Rigenera tutte le pagine in `docs/` |
| `validate.py` | Controlla lingue, link locali, immagini e pagine legali |
| `requirements.txt` | Dipendenza Python per modificare e rigenerare le pagine |

**Non devi installare Python o Node per pubblicare:** il sito è già generato.

Il sito è configurato per la radice del dominio `https://poesieapp.it/`. I collegamenti iniziano con `/`: l’anteprima sotto `nome.github.io/nome-repository/` non è il percorso previsto. Usa il dominio configurato o un server locale avviato su `docs/`.

## Modifiche future

- Aspetto: `docs/style.css`.
- Interazioni: `docs/app.js` e `docs/language.js`.
- Testi nuovi e selettore: `content/ui.json`.
- Testi recuperati dal vecchio sito: `content/original-locales/*.json`.
- Termini: `content/terms.json`.
- Privacy: `content/original-privacy/*.html`.
- Struttura landing: `content/landing-template.html` e `generate.py`.

Dopo aver cambiato testi o template, esegui dalla radice del progetto:

```bash
python -m pip install -r requirements.txt
python generate.py
python validate.py
```

Su Windows puoi usare `py` al posto di `python`. Per verificare anche la sintassi JavaScript, se Node è installato:

```bash
node --check docs/app.js
node --check docs/language.js
```

Fai commit anche dei file rigenerati in `docs/`: GitHub pubblica questi file, non esegue il generatore Python.

Per vedere il sito in locale:

```bash
python -m http.server 8000 --directory docs
```

Apri `http://localhost:8000/it/`. Evita di aprire `index.html` con doppio clic, perché i percorsi assoluti richiedono un server web.

## Aggiornamento nome dell’app

Il nome completo compare nel titolo della pagina, nei metadati di condivisione e vicino al pulsante Google Play. Il logo mantiene «Poesie». Le traduzioni di «Scrittura Creativa» sono proposte editoriali, non nomi verificati sulle schede Google Play. Per allinearle allo store modifica `content/app-names.json` e rigenera le pagine.

## Anteprima con VS Code Live Server

Apri direttamente la cartella `docs` con File → Apri cartella, poi avvia Live Server su `index.html`. L’indirizzo deve essere `http://127.0.0.1:5500/index.html`, senza `/docs/` nel percorso.

I nomi delle lingue nel selettore sono tradotti nella lingua della pagina. Le 11 tabelle si trovano in `content/language-names.json`.
