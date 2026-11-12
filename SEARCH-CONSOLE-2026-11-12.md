# Segnalazioni di indicizzazione — verifica del 12 novembre 2026

Gli screenshot in `search-contorl-problem/` mostrano **due stati distinti e tre URL**, non un blocco generale del sito. Le verifiche HTTPS attuali non hanno rilevato ostacoli tecnici all’indicizzazione delle due pagine legali. Non occorre cambiare il canonical italiano per eliminare la segnalazione di `/it/`.

| URL nello screenshot | Stato di Search Console | Interpretazione e intervento |
|---|---|---|
| `https://poesieapp.it/it/` | Pagina alternativa con tag canonical appropriato; ultima scansione 24 ottobre 2026 | La copia italiana dichiara correttamente `/` come pagina principale. La sua esclusione separata è voluta: mantenere il canonical e usare `/` nei link e nella sitemap. |
| `https://poesieapp.it/privacy/en.html` | Rilevata, ma attualmente non indicizzata; ultima scansione N/D | Google conosce la URL, ma nello stato mostrato non l’ha ancora scansionata. Verificare la pagina pubblicata in Controllo URL e richiedere l’indicizzazione. |
| `https://poesieapp.it/terms/ja.html` | Rilevata, ma attualmente non indicizzata; ultima scansione N/D | Stesso stato della privacy inglese; eseguire il controllo della pagina pubblicata e la richiesta sulla URL giapponese. |

La [documentazione Google sul report](https://support.google.com/webmasters/answer/7440203?hl=it) spiega che “Rilevata” significa conosciuta ma non ancora scansionata, mentre l’alternativa con canonical appropriato non richiede una correzione. Dagli screenshot non si può stabilire il motivo specifico per cui Google abbia rinviato queste due scansioni: non costituiscono la prova di un errore del sito, di una penalizzazione, di un problema di traduzione o di un server sovraccarico.

**Verifica sul sito pubblico**

Eseguita il 12 novembre 2026 alle 10:17 UTC. Risposte e risultati strutturati sono conservati in `../artifacts/landing-audit/search-console/`, inclusi gli HTML acquisiti e `results.json`.

- Tutte le 11 richieste della verifica hanno restituito HTTP 200: home, `/it/`, home inglese e giapponese, quattro pagine legali, sitemap, robots.txt e script della lingua.
- Le due pagine segnalate hanno il contenuto nella lingua corretta, un canonical verso sé stesse, nessun meta `noindex` e nessun header `X-Robots-Tag` o `Link` restrittivo/conflittuale nelle risposte esaminate.
- `robots.txt` consente l’accesso a Googlebot a entrambe le pagine. La sitemap pubblica contiene 33 URL canoniche, comprese entrambe le URL segnalate; esclude correttamente `/it/`.
- La home inglese contiene un normale link HTML alla privacy inglese nel footer; la home giapponese contiene quello ai Termini giapponesi. La scoperta di questi link non richiede l’esecuzione di JavaScript.
- `/it/` dichiara `https://poesieapp.it/` come canonical e il suo testo principale coincide con quello della home. La home inglese mantiene invece il proprio canonical `/en/`: il caso mostrato qui è diverso dalla vecchia segnalazione del 4 novembre, in cui Google preferiva la home italiana alla pagina inglese.
- Le richieste delle due URL con User-Agent `Googlebot` hanno restituito anch’esse HTTP 200. Questo controlla solo la risposta al nome del client: non autentica un vero Googlebot e non dimostra che Google possa accedere da ogni sua infrastruttura. Il test autenticato in Search Console resta il riferimento per il suo accesso effettivo.

Nel codice locale è stato rafforzato `validate.py`: ora controlla anche che robots.txt consenta Googlebot e che nessuna delle pagine generate abbia meta `robots`/`googlebot` con `noindex` o `none`. Il controllo previene blocchi accidentali futuri; non è un meccanismo per forzare l’inclusione nell’indice.

**Passaggi in Search Console**

1. Pubblicare gli aggiornamenti locali della landing e dei documenti legali preparati nella verifica precedente, se si vuole far indicizzare direttamente il contenuto aggiornato. Verificare che la pubblicazione sia completata prima della richiesta.
2. Aprire **Controllo URL** per `https://poesieapp.it/privacy/en.html`, eseguire **Testa URL pubblicato** e controllare risposta, scansione consentita e possibilità di indicizzazione. Se il test non segnala impedimenti, usare **Richiedi indicizzazione**.
3. Ripetere per `https://poesieapp.it/terms/ja.html`. Non richiedere l’indicizzazione separata di `/it/`, che deve restare un’alternativa della home.
4. Nella sezione **Sitemap**, verificare che sia stata inviata `https://poesieapp.it/sitemap.xml` e che lo stato sia riuscito. La presenza del file online non prova che sia già stato inviato o elaborato nella proprietà Search Console.
5. Monitorare l’esito in Controllo URL e nel report. Per lo stato “Rilevata” il passaggio utile è la richiesta di scansione delle due URL; il pulsante “Convalida correzione” non sostituisce questo controllo e non c’è un difetto di canonical dimostrato da correggere in questo caso.

Google indica che una nuova scansione può richiedere giorni o settimane, che richieste ripetute non la accelerano e che la richiesta non garantisce l’indicizzazione. Fonte: [richiedere una nuova scansione](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=it).

Non sono state inviate richieste a Search Console da questo ambiente e non è stata eseguita una pubblicazione. La configurazione corrente di canonical, lingue e sitemap è stata mantenuta perché coerente con il comportamento desiderato.
