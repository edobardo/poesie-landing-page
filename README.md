# Poesie — landing statica per GitHub Pages

Il sito usa sei mockup e la grafica 1024×500 dello store, con copie ottimizzate per il web, font locali e contenuti in 11 lingue. `new-images/` contiene i poster aggiornati della scrittura e dello spazio personale. Non richiede backend, Node, API o servizi a pagamento per funzionare.

## Anteprima locale

Dalla cartella `poesie-landing-page`:

```powershell
python -m http.server 8000 --directory docs
```

Apri `http://localhost:8000/` oppure `http://localhost:8000/en/`. La radice `/` mantiene sempre l’italiano e ogni altra lingua ha il proprio URL: il selettore permette di cambiarla esplicitamente, senza reindirizzamenti basati su browser, preferenze salvate o riconoscimento dei bot. `/it/` resta una copia compatibile con i vecchi link, con canonical verso `/`; tutti i nuovi link interni italiani puntano a `/`. Non aprire gli HTML con doppio clic: il sito usa percorsi dalla radice del dominio.

## File da modificare

| Percorso | Contenuto |
|---|---|
| `content/landing.json` | Tutti i testi della landing nelle 11 lingue, FAQ e descrizioni delle immagini |
| `content/landing-template.html` | Struttura HTML della landing |
| `docs/style.css` | Aspetto, responsive e stili delle pagine legali |
| `docs/app.js` | Ingrandimento delle immagini; i link funzionano anche senza JavaScript |
| `docs/language.js` | Scelta esplicita della lingua tramite i suoi URL |
| `content/app-names.json` | Nome localizzato dell’app |
| `content/language-names.json` | Nomi delle lingue nel selettore |
| `content/original-locales/*.json` | Testi del footer e delle pagine legali; non sono più la fonte delle funzioni della landing |
| `content/ui.json` | Etichette condivise di navigazione e pagine legali |
| `content/original-privacy/*.html` | Testo sorgente corrente della Privacy Policy, aggiornato al comportamento dell’app |
| `content/terms.json` | Testo sorgente dei termini |
| `docs/assets/showcase/` | Poster WebP responsive, grafica store WebP e PNG per anteprime social |
| `docs/assets/fonts/` | Font IM Fell English già usati dall’app, serviti localmente |
| `generate.py` | Generatore delle 34 pagine HTML, canonical e metadati social |
| `validate.py` | Verifica traduzioni, link, ancore, varianti immagini, metadati e testi legali |
| `prepare_assets.py` | Prepara gli asset da `new-images/`, `new-screen/` o `../NEWSCREEN/`, conservando le copie pronte se un originale non è disponibile |

Per aggiornare testi o struttura:

```powershell
python -m pip install -r requirements.txt
python -B generate.py
python -B validate.py
```

Per aggiornare anche le immagini, prima di generare esegui `python -B prepare_assets.py`. Il comando cerca i poster in `new-images/`, poi in `new-screen/` e infine in `../NEWSCREEN/`. Se un originale manca, conserva entrambe le varianti già pronte. Se mancano anche quelle, segnala un errore. Lo stesso vale per la grafica store. I font provengono da `../PDF_Poesie_App/Resources/Fonts/` e, se gli originali non sono disponibili, il comando conserva quelli già presenti. Le copie pronte sono incluse in `docs/`: pubblicazione e rigenerazione degli HTML non richiedono gli originali.

Con Node disponibile, controlla la sintassi con `node --check docs/app.js` e `node --check docs/language.js`.

I poster mantengono i testi inglesi originali; la pagina lo indica in tutte le lingue. Le note Premium sono esplicite anche in HTML. Il PNG usato nei metadati Open Graph è la nuova grafica originale 1024×500 dello store.

## Pubblicazione

Il sito è pronto per `https://poesieapp.it/`: sono mantenuti `docs/CNAME`, `.nojekyll` e i token di verifica Google. In GitHub Pages usa il ramo previsto dal repository e la cartella `/docs`. Includi nel commit i sorgenti, gli asset nuovi e tutti gli HTML rigenerati: GitHub Pages pubblica `docs/`, senza eseguire Python.

Non occorrono modifiche DNS per questo aggiornamento. Privacy e Termini sono aggiornati al 12 novembre 2026 nelle 11 lingue, includendo bozze, cestino, limiti dei backup, servizi vocali, copie locali e trattamento tecnico del sito. Le vecchie etichette di bozza non vengono inserite nelle pagine pubblicabili.

## Verifiche dell’aggiornamento

`validate.py` controlla tutte le 34 pagine: 11 landing, 11 privacy, 11 termini e la copia italiana alla radice. Verifica anche i file in `srcset`, i link alle immagini ingrandite, le ancore, i canonical e gli alternate delle lingue. Confronta il testo legale con i sorgenti, su Windows e sugli altri sistemi.

L’analisi iniziale è conservata in `ANALISI-AGGIORNAMENTO.md`; la verifica attuale, le correzioni e i problemi ancora aperti sono in `ANALISI-2026-11-12.md`. Il generatore del sito non modifica il codice Android. In questo aggiornamento sono stati corretti separatamente il riepilogo privacy nell’app e i collegamenti localizzati a Privacy e Termini.

## Segnalazione Search Console del 4 novembre 2026

La verifica più recente è in [SEARCH-CONSOLE-2026-11-12.md](SEARCH-CONSOLE-2026-11-12.md): gli screenshot in `search-contorl-problem/` riguardano `/it/` come alternativa corretta della home e due pagine legali rilevate ma non ancora scansionate. Le richieste HTTPS attuali sono riuscite e non mostrano blocchi di robots, noindex o canonical per queste due URL. Il testo seguente conserva il contesto storico del diverso problema segnalato il 4 novembre.

Gli screenshot in `problem/` segnalano `/en/` come «Pagina duplicata, Google ha scelto una pagina canonica diversa da quella specificata dall’utente». Il dettaglio del Controllo URL mostra che il 23 ottobre Google ha scansionato correttamente `/en/`, con scansione e indicizzazione consentite, ma ha scelto `https://poesieapp.it/` come canonical al posto di `https://poesieapp.it/en/`. Nei file locali `/en/` ha già un canonical verso sé stessa, contenuto inglese e alternate reciproci; sitemap e robots includono e consentono la pagina. Il contenuto acquisito da Google non è disponibile negli screenshot e le richieste di verifica del sito pubblico da questo ambiente hanno ricevuto HTTP 403: il confronto con la versione pubblicata resta da completare.

Sono stati rimossi i reindirizzamenti automatici della home e uniformati i link italiani al canonical `/`. Sono correzioni di coerenza, non la prova della causa della segnalazione. Google raccomanda URL stabili per lingua e una scelta esplicita della lingua: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites.

Dopo la pubblicazione, in Search Console:

1. Controlla `https://poesieapp.it/en/` e confronta la «Pagina canonica selezionata da Google» con quella dichiarata. Nei dati del 23 ottobre la scelta è la home `/`: confronta anche il contenuto acquisito da Google per entrambe le pagine, se disponibile.
2. Esegui il test dell’URL pubblicato e verifica che restituisca la pagina inglese con canonical `https://poesieapp.it/en/`, senza blocchi alla scansione.
3. Richiedi l’indicizzazione di `/en/` e della home aggiornata. Verifica che la sitemap inviata sia `https://poesieapp.it/sitemap.xml`.
4. Avvia «Convalida correzione» dopo le verifiche. Il risultato dipende da una nuova scansione e dalla scelta di Google; il test dell’URL pubblicato non anticipa il canonical che Google selezionerà.

Guida al significato della segnalazione: https://support.google.com/webmasters/answer/7440203?hl=it.
