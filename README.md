# Poesie — landing statica per GitHub Pages

Aggiornamento del 22 ottobre 2026. Il sito usa i sei mockup e la nuova grafica 1024×500 dello store in `../NEWSCREEN/`, con copie ottimizzate per il web, font locali e contenuti in 11 lingue. Non richiede backend, Node, API o servizi a pagamento per funzionare.

## Anteprima locale

Dalla cartella `poesie-landing-page`:

```powershell
python -m http.server 8000 --directory docs
```

Apri `http://localhost:8000/it/` oppure `http://localhost:8000/en/`. La radice `/` propone la lingua del browser o l’ultima selezionata; `/it/` mantiene sempre l’italiano. Non aprire gli HTML con doppio clic: il sito usa percorsi dalla radice del dominio.

## File da modificare

| Percorso | Contenuto |
|---|---|
| `content/landing.json` | Tutti i testi della landing nelle 11 lingue, FAQ e descrizioni delle immagini |
| `content/landing-template.html` | Struttura HTML della landing |
| `docs/style.css` | Aspetto, responsive e stili delle pagine legali |
| `docs/app.js` | Ingrandimento delle immagini; i link funzionano anche senza JavaScript |
| `docs/language.js` | Scelta e preferenza della lingua |
| `content/app-names.json` | Nome localizzato dell’app |
| `content/language-names.json` | Nomi delle lingue nel selettore |
| `content/original-locales/*.json` | Testi del footer e delle pagine legali; non sono più la fonte delle funzioni della landing |
| `content/ui.json` | Etichette condivise di navigazione e pagine legali |
| `content/original-privacy/*.html` | Testo sorgente della Privacy Policy |
| `content/terms.json` | Testo sorgente dei termini |
| `docs/assets/showcase/` | Poster WebP responsive, grafica store WebP e PNG per anteprime social |
| `docs/assets/fonts/` | Font IM Fell English già usati dall’app, serviti localmente |
| `generate.py` | Generatore delle 34 pagine HTML, canonical e metadati social |
| `validate.py` | Verifica traduzioni, link, ancore, varianti immagini, metadati e testi legali |
| `prepare_assets.py` | Preparazione deterministica degli asset da NEWSCREEN, senza modificare gli originali |

Per aggiornare testi o struttura:

```powershell
python -m pip install -r requirements.txt
python -B generate.py
python -B validate.py
```

Per ricreare anche le immagini, prima di generare esegui `python -B prepare_assets.py`. Questo comando richiede `../NEWSCREEN/` e i due font in `../PDF_Poesie_App/Resources/Fonts/`. Le copie pronte sono già incluse in `docs/`: né la pubblicazione né la rigenerazione degli HTML richiedono queste cartelle esterne.

Con Node disponibile, controlla la sintassi con `node --check docs/app.js` e `node --check docs/language.js`.

I poster mantengono i testi inglesi originali; la pagina lo indica in tutte le lingue. Le note Premium sono esplicite anche in HTML. Il PNG usato nei metadati Open Graph è la nuova grafica originale 1024×500 dello store.

## Pubblicazione

Il sito è pronto per `https://poesieapp.it/`: sono mantenuti `docs/CNAME`, `.nojekyll` e i token di verifica Google. In GitHub Pages usa il ramo previsto dal repository e la cartella `/docs`. Includi nel commit i sorgenti, gli asset nuovi e tutti gli HTML rigenerati: GitHub Pages pubblica `docs/`, senza eseguire Python.

Non occorrono modifiche DNS per questo aggiornamento. I contenuti legali mantengono il testo visibile delle pagine precedenti; le vecchie etichette di bozza dei sorgenti non vengono inserite nelle pagine pubblicabili.

## Verifiche dell’aggiornamento

`validate.py` controlla tutte le 34 pagine: 11 landing, 11 privacy, 11 termini e la copia italiana alla radice. Verifica anche i file in `srcset`, i link alle immagini ingrandite, le ancore, i canonical e gli alternate delle lingue. Confronta il testo legale con i sorgenti, su Windows e sugli altri sistemi.

L’analisi iniziale è conservata in `ANALISI-AGGIORNAMENTO.md`. Il codice dell’app Android non viene modificato dal sito.
