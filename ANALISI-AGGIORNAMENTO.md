# Poesie — analisi della landing e proposta di aggiornamento

**Aggiornamento realizzato.** La proposta descritta sotto è stata applicata al sito locale. Sono stati integrati i sei poster e la nuova immagine `NEWSCREEN/poesie_feature_graphic_en_1024x500.png`: quest’ultima compare nella chiusura della pagina e, nella versione PNG originale, nei metadati di condivisione. La landing ha ora fondo carta, accenti verde bosco, sezioni per immagini e video e un confronto gratuito/Premium nelle 11 lingue. Gli originali delle immagini e il codice Android sono rimasti intatti. Le copie WebP dei sei poster a 480 px occupano insieme circa 146 KiB; tutte le varianti WebP, inclusa la grafica orizzontale, circa 566 KiB. I problemi del generatore e del validatore descritti nell’analisi iniziale sono stati corretti. Le istruzioni aggiornate sono in `README.md`.

Analisi del 22 ottobre 2026. Materiali: sito locale in `poesie-landing-page/`, sei immagini in `NEWSCREEN/`, codice dell’app Android in `PDF_Poesie_App/`. La versione dichiarata nel progetto è 2.2.2, build 52. Le conclusioni sulle funzioni derivano dal codice locale: non attestano quale build sia attualmente distribuita su Google Play.

**La direzione proposta**

Poesie ha già una buona identità letteraria. La landing attuale comunica soprattutto intimità e conservazione; i nuovi mockup mostrano anche risultati concreti: una poesia diventa un’immagine, un video, un’antologia. Proporrei di costruire il percorso intorno a questa trasformazione, mantenendo la riservatezza come elemento di fiducia.

Messaggio centrale: **«Dai forma ai tuoi versi.»**

Sottotitolo: «Scrivi le tue poesie, raccoglile in uno spazio personale e trasformale in immagini, video o un’antologia PDF.»

Pulsante: **«Scarica per Android»**. Collegamento secondario: «Scopri cosa puoi creare».

Nota vicina al pulsante: «Inizia gratis, anche senza account. Funzioni aggiuntive con Premium.» Il riferimento all’account riguarda l’avvio in modalità Solo Locale; il cloud richiede di collegare Google o Microsoft.

**Valutazione della pagina attuale**

La combinazione di verde scuro, oro e caratteri serif è riconoscibile e coerente con l’app. La struttura è già completa: presentazione, funzioni, privacy, galleria, FAQ e download. Il sito statico, con 11 lingue e pagine legali separate, è una base adatta da conservare.

La verifica con Chromium su viewport 1440 × 1000 e 390 × 844 non ha rilevato sbordamenti orizzontali o risposte HTTP di errore durante il percorso provato. Il cambio delle quattro funzioni e l’apertura della prima immagine nella finestra di anteprima funzionano. Non è una verifica esaustiva di tutti i dispositivi e browser.

I punti da migliorare sono concreti:

- La prima schermata usa soprattutto atmosfera e un vecchio menu dell’app. Fa capire meno rapidamente cosa si può creare rispetto ai nuovi mockup.
- Il titolo è evocativo, ma non identifica subito l’app come strumento per scrivere e presentare poesie. Su mobile occupa molto spazio; nel primo schermo si vede solo l’inizio del visual.
- I video non hanno una sezione dedicata, benché siano una delle novità più dimostrabili.
- Esportazioni, raccolte e statistiche ricompaiono con testi simili nelle sezioni successive. La pagina può essere più breve e mostrare più risultati.
- Le FAQ pubblicate parlano soprattutto di riservatezza e account; non spiegano chiaramente cosa è gratuito e cosa richiede Premium.
- Le immagini informative sono scure e i contenuti dell’interfaccia diventano piccoli nella galleria. Le nuove composizioni rendono più evidente il risultato finale.

Riferimenti visivi dell’attuale pagina: [desktop](../artifacts/landing-analysis/desktop-hero.png), [mobile](../artifacts/landing-analysis/mobile-hero.png), [galleria desktop](../artifacts/landing-analysis/desktop-gallery.png).

**Come usare le sei nuove immagini**

Tutte le immagini misurano 1536 × 2752 px, rapporto circa 0,558. Insieme pesano 11,79 MiB. Hanno già composizione editoriale, titoli inglesi e, in alcuni casi, note Premium. Sono materiali promozionali completi: inserirli come semplici screenshot richiede attenzione a dimensioni, tagli e lingua.

| Immagine | Utilizzo proposto | Testo della sezione |
|---|---|---|
| `01_give_shape_to_your_verses.jpg` | Visual principale: mostra sia lo strumento sia una poesia impaginata | «Dai forma ai tuoi versi.» |
| `02_every_emotion_finds_its_words.jpg` | Sezione scrittura, dopo la presentazione | «Ogni emozione trova le sue parole.» |
| `03_your_poetry,_your_style.jpg` | Sezione immagini e stili | «La tua poesia, il tuo stile.» |
| `04_your_verses_come_to_life.jpg` | Sezione dedicata ai video | «I tuoi versi prendono vita.» |
| `05_your_poems_become_a_book.jpg` | Sezione antologia, con indicazione Premium in HTML | «Le tue poesie diventano un libro.» |
| `06_a_space_all_yours.jpg` | Sezione raccolte e protezione | «Uno spazio tutto tuo.» |

L’ordine narrativo consigliato è **01 → 02 → 03 → 04 → 05 → 06**. Gli stessi materiali possono essere raccolti in una galleria finale, ma eviterei di duplicare tutti e sei i poster dopo averli già mostrati grandi nelle sezioni.

Nel mockup 03 la card chiamata «Sakura» è beige e oro. In `Services/ShareImageTemplate.cs`, Sakura ha fondo `#FFF1F6` e accenti rosa; la palette beige è più vicina agli stili Pergamena. Verificare nome o immagine prima del riuso. Anche «Noir» e «Night» andrebbero uniformati alla nomenclatura effettiva dell’app nelle varie lingue.

Il mockup 06 mostra i controlli di blocco e screenshot in posizione apparentemente disattivata: documenta la disponibilità delle impostazioni, non l’attivazione della protezione. Eviterei didascalie che suggeriscano che queste opzioni siano già attive per tutti.

Per la landing italiana, i testi inglesi incorporati restano visibili anche traducendo le didascalie. Si possono usare subito come anteprime in inglese, dichiarandolo vicino alla galleria; la soluzione editoriale migliore è disporre di versioni italiane e inglesi coerenti, con titoli e descrizioni principali scritti in HTML. Le altre lingue possono usare il visual inglese con una nota localizzata finché non esistono asset dedicati.

**Aspetto e composizione**

Consiglio una base carta avorio, testo quasi nero, verde bosco per pulsanti e marchio, oro per dettagli. È una scelta visiva derivata dai nuovi materiali. Mantiene il carattere letterario e integra meglio i poster chiari.

Palette di partenza: carta `#F5EBDD`, testo `#201E1B`, verde `#263C30`, oro scuro `#8A6938`. I contrasti effettivi vanno verificati quando si applicano colori e dimensioni. La sezione sulla riservatezza può riprendere un fondo verde scuro.

Su desktop: testo e visual affiancati, alternando il lato delle immagini nelle sezioni. Su mobile: titolo breve, beneficio, pulsante di download e visual, poi una sequenza lineare. Il poster non deve diventare una miniatura illeggibile per farlo entrare a forza nel primo schermo.

I poster devono mantenere il rapporto originale. L’attuale galleria impone `aspect-ratio: 9/14` e `object-fit: cover`: con le nuove immagini taglierebbe parte del contenuto. Anche hero e immagine delle funzioni usano contenitori con ritaglio. Servono dimensioni naturali oppure `object-fit: contain`, senza sfumature scure sopra titoli e note incorporati. Non basta cambiare i nomi dei file.

**Struttura e testi proposti**

| Posizione | Contenuto | Indicazioni |
|---|---|---|
| 1. Apertura | «Dai forma ai tuoi versi.» + sottotitolo + download | Mockup 01; Android e disponibilità Premium chiari |
| 2. Scrittura | «Ogni emozione trova le sue parole.» | «Cattura un pensiero, trova la concentrazione e torna sui tuoi testi quando vuoi.» Mockup 02; eventuale nota sui modelli guidati Premium |
| 3. Immagini | «La tua poesia, il tuo stile.» | «Scegli un’impaginazione e crea immagini quadrate o verticali da condividere.» Mockup 03; stili aggiuntivi e rimozione watermark con Premium |
| 4. Video | «I tuoi versi prendono vita.» | «Crea video con effetto macchina da scrivere, scegli il ritmo e aggiungi un sottofondo.» Mockup 04; un vero breve MP4 dimostrativo sarebbe un’evoluzione utile |
| 5. Antologia | «Le tue poesie diventano un libro.» | «Riunisci la tua raccolta in un’antologia PDF con copertina e impaginazione dedicata.» Mockup 05 e badge Premium; chiarire che è un file PDF, senza promettere stampa o pubblicazione |
| 6. Spazio personale | «Uno spazio tutto tuo.» | «Organizza raccolte, tag e preferiti. Scegli il salvataggio locale o collega Google Drive o OneDrive. Attiva il blocco dell’app e la protezione degli screenshot.» Mockup 06 |
| 7. Premium | Piccolo confronto gratuito / Premium | Acquisto singolo; prezzo consultabile nell’app, senza inventare un importo fisso |
| 8. FAQ e chiusura | Risposte pratiche e secondo invito al download | «Il prossimo verso comincia da te.» |

Statistiche, streak, revisioni e Poetry Wrapped possono stare in una fascia compatta di approfondimento. Aiutano a descrivere la ricchezza dell’app, ma non dovrebbero interrompere il percorso principale verso i risultati mostrati dai mockup.

FAQ consigliate: «Posso iniziare senza account?», «Dove vengono salvate le poesie?», «Cosa posso creare gratuitamente?», «Cosa include Premium?», «Su quali dispositivi funziona?». Le risposte devono riflettere i requisiti verificati nel codice.

**Cosa conferma il codice dell’app**

| Area | Evidenza locale | Conseguenza per la landing |
|---|---|---|
| Piattaforma | `PDF_Poesie_App.csproj`: target `net10.0-android` | Promuovere Android; le cartelle di altre piattaforme non bastano a prometterne la disponibilità |
| Avvio senza account | `Pages/WelcomePage.xaml.cs`: il pulsante di scrittura sceglie `LocalOnly` | «Inizia anche senza account» è coerente con il percorso implementato |
| Salvataggio | `Services/CloudSyncManager.cs`: Google Drive, OneDrive e Solo Locale | Presentare tre scelte; il mirroring simultaneo dei due cloud è disattivato |
| Scrittura | `Pages/AddPoesiaPage.xaml.cs`: spunti locali, timer, Focus e modelli | Descrivere strumenti di scrittura; non attribuire gli spunti a un assistente AI |
| Organizzazione | Raccolte, tag, preferiti, cartelle intelligenti e ricerca hanno componenti dedicati | Conservare il valore del quaderno personale, senza ridurre l’app a un generatore di card |
| Immagini | `Services/ShareImageTemplate.cs`: 7 stili, formati 1:1 e 9:16 | Distinguere gli stili di esportazione dai temi dell’interfaccia |
| Video | `Services/PoetryVideoService.cs` e implementazione Android: MP4, velocità, cursore, pausa e sottofondi | Il mockup 04 merita una funzione visibile nella pagina |
| Esportazione | `Pages/MainPage.xaml.cs`: PDF standard, PDF antologia, TXT, MD, HTML ed EPUB | Distinguere PDF standard e antologia Premium |
| Protezione | `LockService`, `BiometricAuthService`, `BlockScreenshotService`, `FileEncryptionService` | Descrivere controlli attivabili e cifratura locale; evitare promesse assolute o «cifratura end-to-end» non dimostrate da questa analisi |
| Temi dell’app | `Services/ThemeService.cs`: Dark, Light, Pergamena Antica, Sakura e Noir Parigino | Sono 5 temi dell’interfaccia, distinti dai 7 stili delle immagini |
| Premium | `PremiumService.cs`: prodotto `InAppPurchase`, non abbonamento | Presentare uno sblocco con acquisto singolo tramite Google Play |

Distinzioni gratuite / Premium verificate nei punti di accesso alle funzioni:

- Immagini e video con stile gratuito e watermark sono consentiti senza Premium. Il controllo in `PremiumOffer.RequiresPremiumExport` richiede Premium per stili aggiuntivi, rimozione del watermark o audio personalizzato nei video.
- Pergamena Antica, Sakura e Noir Parigino sono stili Premium; le loro anteprime sono visibili anche prima dell’acquisto.
- L’antologia PDF richiede Premium; il PDF standard segue un percorso distinto.
- I modelli poetici diversi dal verso libero richiedono Premium nell’editor.
- I temi diversi da Dark e Light richiedono Premium.
- L’esportazione del backup ZIP è protetta da un controllo Premium. La landing attuale ne parla senza esplicitare questo requisito.

Il mockup 05 è corretto nell’esplicitare Premium. Per il 04 non bisogna introdurre un generico badge «video Premium»: sarebbe più restrittivo del comportamento presente nel codice.

**Osservazioni sul codice e sulla manutenzione**

L’app ha servizi dedicati per esportazione, sincronizzazione, sicurezza e acquisti; esistono anche progetti di verifica mirati per Premium, onboarding, antologie, autore Word e selezione tag. Sono elementi utili per mantenere allineate le promesse della pagina con il prodotto.

Molte decisioni restano però nei file associati alle pagine: circa 1.418 righe per MainPage, 1.363 per AddPoesiaPage e 2.089 per SettingsPage. Anche i controlli Premium sono distribuiti tra pagine e servizi. Per la manutenzione futura sarebbe utile estrarre progressivamente operazioni e requisiti condivisi in servizi testabili. Questo lavoro non è un prerequisito per aggiornare la landing.

`ShareImageTemplate.cs` fa riferimento a font Playfair Display ed EB Garamond; nella cartella `Resources/Fonts` esaminata non risultano presenti quei file. Il renderer prevede un ripiego su IM Fell English. È un punto da verificare se si vuole promettere una differenza tipografica precisa tra gli stili: questa lettura non ha ispezionato le risorse di un APK compilato.

Il documento `ToDo.txt` contiene idee e osservazioni che non descrivono sempre lo stato corrente: ad esempio include ancora l’antologia e l’analisi dei modelli tra le evoluzioni. Per i testi pubblici bisogna usare le funzioni implementate e i loro controlli di accesso come riferimento.

Questa è una lettura tecnica orientata al prodotto e alla comunicazione. Non sono stati eseguiti una build Android, un acquisto reale, una sincronizzazione cloud o un audit di sicurezza completo.

**Correzioni tecniche da includere nell’aggiornamento**

La prova di rigenerazione è stata eseguita su una copia temporanea, senza modificare il sito originale. Ha mostrato differenze in 23 pagine HTML.

1. **Allineare generatore e pagine pubblicabili.** `generate.py` e il template usano `Collection`, mentre l’asset disponibile e gli HTML attuali usano `Collections`. Dopo la rigenerazione la configurazione della galleria punta a un file inesistente. Il generatore perde inoltre i canonical presenti negli HTML attuali; nella pagina italiana rigenerata non rimane alcun canonical. Ripristinare nel generatore anche le annotazioni linguistiche necessarie, compreso `x-default`.
2. **Modificare le vere fonti dei testi.** Il generatore sovrascrive gran parte del template con `content/ui.json` e `content/original-locales/*.json`. Per esempio i tre blocchi su temi, ascolto e revisioni del template vengono sostituiti da testi diversi negli HTML generati. Cambiare solo il template o solo `docs/it/index.html` non produce un aggiornamento durevole.
3. **Verificare anche le immagini dinamiche.** `validate.py` controlla gli attributi HTML `src` e `href`, ma non verifica i file nominati in `window.POESIE.gallery` o `data-image`. La discrepanza Collection/Collections può quindi sfuggire al controllo. Su Windows anche le condizioni che cercano `/privacy/` e `/terms/` in `str(file)` vanno rese indipendenti dal separatore del percorso, per eseguire realmente quei controlli specifici.
4. **Rendere la galleria disponibile nell’HTML.** Oggi con JavaScript disattivato contiene zero immagini. Generare figure e didascalie statiche; lasciare a JavaScript ingrandimento e navigazione. Mantenere descrizioni accessibili specifiche per ogni visual.
5. **Preparare asset per il web.** Conservare gli originali in NEWSCREEN e produrre versioni WebP/AVIF con larghezze adeguate a mobile e desktop, `srcset`, `sizes` e dimensioni esplicite. Stabilire il peso finale dopo un confronto visivo: l’estensione WebP da sola non garantisce leggerezza, dato che tre asset attuali superano già 2 MiB ciascuno. Caricamento prioritario solo per il visual iniziale, differito per i successivi.
6. **Completare la condivisione social.** Nella landing italiana esaminata ci sono titolo e descrizione Open Graph, ma manca `og:image`. Preparare una composizione orizzontale adatta all’anteprima, invece di affidarsi a un poster verticale.

Il testo «sette temi, dal Bosco all’Universo» è nel template sorgente, non nei tre blocchi effettivamente pubblicati della pagina italiana esaminata. Va corretto come fonte potenzialmente fuorviante, senza presentarlo come un errore oggi visibile in quella pagina.

**Ordine di lavoro consigliato**

Prima allineare generatore, nomi degli asset e controlli. Poi applicare impaginazione e testi alla versione italiana e inglese, verificando soprattutto mobile, leggibilità dei poster e distinzione Premium. Infine estendere gli stessi contenuti alle 11 lingue e rigenerare tutte le pagine. Il sito può restare statico e continuare a usare la pubblicazione attuale.

Controlli già eseguiti: `python -B validate.py` passa sulle 34 pagine attuali; la sintassi di `docs/app.js` e `docs/language.js` è valida. Le limitazioni del validatore descritte sopra ridimensionano ciò che quel risultato garantisce. I risultati delle prove sono in [browser-audit.json](../artifacts/landing-analysis/browser-audit.json) e [generator-audit.json](../artifacts/landing-analysis/generator-audit.json).
