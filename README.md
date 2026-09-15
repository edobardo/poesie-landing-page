# Poesie landing page

Landing page statica e pagine privacy multilingua per l'app Poesie.

## Struttura

- `index.html`: landing page principale
- `privacy/`: privacy policy, una pagina HTML per lingua
- `assets/`: immagini, badge e JavaScript condiviso
- `locales/`: traduzioni dell'interfaccia della landing
- `archive/`: vecchie versioni non utilizzate

## Avvio locale

Per evitare limitazioni del browser sui file JSON, avvia un server statico dalla root del progetto:

```bash
python -m http.server 8000
```

Apri quindi <http://localhost:8000>.
