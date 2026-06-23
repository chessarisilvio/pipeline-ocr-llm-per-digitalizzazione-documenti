# Pipeline OCR+LLM per Digitalizzazione Documenti

## Descrizione
Questo progetto implementa una pipeline end‑to‑end per la digitalizzazione di documenti cartacei. Combina l'OCR per l'estrazione del testo da immagini/scansioni con un modello LLM locale per la strutturazione, la correzione e l'arricchimento dei contenuti.

## Architettura
- **ocr_extractor.py** – utilizza Tesseract (via pytesseract) per convertire le immagini in testo grezzo.
- **run_pipeline.py** – orchestratore che chiama l'OCR, pulisce il testo e lo invia a un modello LLM locale (Qwen‑3.6‑35B) per l'analisi semantica e la generazione di metadati.
- **requirements.txt** – dipendenze Python (pytesseract, pandas, openpyxl, lxml, etc.).
- **.env.example** – file di esempio per configurare variabili d'ambiente (es. `TESSDATA_PREFIX`).

## Installazione
```bash
# Clona il repository
git clone <repo-url>
cd pipeline-ocrllm-per-digitalizzazione-documenti

# Crea un ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate

# Installa le dipendenze
python3 -m pip install --user --break-system-packages -r requirements.txt
```
Assicurati di avere Tesseract installato sul sistema (`sudo apt install tesseract-ocr`).

## Uso
```bash
# Copia il file .env.example in .env e personalizza le variabili se necessario
cp .env.example .env

# Esegui la pipeline su una cartella di immagini
python run_pipeline.py --input ./scansioni --output ./output
```
Il risultato è un file CSV con le colonne `filename`, `raw_text`, `structured_text`, `metadata`.

## Esempi
```bash
# Esempio rapido su una singola immagine
python ocr_extractor.py --image ./esempio.jpg
```

## Stato
- **Fase 1/5** – Struttura progetto ✅
- **Fase 2/5** – Ambiente Python e dipendenze ✅
- **Fase 3/5** – Script di estrazione OCR ✅
- **Fase 4/5** – Pipeline di orchestrazione ✅
- **Fase 5/5** – Documentazione completa ✅

---
*Questo progetto è pubblicato sotto licenza MIT.*