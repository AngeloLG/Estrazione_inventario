# Descrizione del Progetto: `Estrazione_inventario`

## 1. Obiettivo

L'applicazione `Estrazione_inventario` è uno strumento a riga di comando (CLI) progettato per automatizzare l'estrazione di informazioni bibliografiche da file PDF e consolidarle in un file Excel. Sfrutta la potenza del modello multimodale **GPT-4o di OpenAI** per interpretare sia il testo che la struttura visiva dei documenti, consentendo un'estrazione dati precisa guidata da un prompt dell'utente.

## 2. Funzionalità Chiave

- **Analisi Multimodale di PDF**: Invece di limitarsi a estrarre testo grezzo, lo strumento converte ogni pagina del PDF in un'immagine. Queste immagini vengono inviate a GPT-4o, permettendo al modello di analizzare layout complessi, tabelle, figure e note manoscritte che i metodi tradizionali potrebbero non cogliere.
- **Estrazione Guidata da Prompt**: L'utente specifica esattamente quali dati estrarre tramite un prompt testuale. Questa flessibilità permette di adattare l'estrazione a diversi tipi di documenti e requisiti (es. "estrai titolo e autore", "trova tutti gli articoli pubblicati dopo il 2020 con il loro abstract").
- **Output Strutturato**: I dati estratti vengono automaticamente organizzati e salvati in un file Excel (`.xlsx`), pronto per ulteriori analisi o archiviazione. Il nome del file di output è derivato dal nome del PDF di input per una facile associazione.
- **Configurazione Semplice**: La configurazione richiede solo di inserire una chiave API di OpenAI in un file `.env`, rendendo l'avvio rapido e sicuro.
- **Interfaccia a Riga di Comando (CLI)**: Tutte le operazioni vengono gestite tramite comandi semplici e chiari, con argomenti per specificare il file di input, il prompt e la directory di output opzionale.

## 3. Flusso di Lavoro Tecnico

1.  **Avvio**: L'utente esegue lo script `run.py` fornendo il percorso del PDF e un prompt.
2.  **Caricamento Configurazione**: L'applicazione carica in modo sicuro la chiave API di OpenAI dal file `.env`.
3.  **Elaborazione PDF**: Il servizio `LLMClient` apre il file PDF specificato.
4.  **Conversione in Immagini**: Ogni pagina del PDF viene renderizzata come un'immagine e codificata in formato base64.
5.  **Chiamata all'API di OpenAI**: Viene costruita una richiesta all'API di GPT-4o, includendo:
    - Un **prompt di sistema** che istruisce il modello a restituire sempre e solo un oggetto JSON.
    - Il **prompt dell'utente**.
    - La sequenza di **immagini** delle pagine.
6.  **Parsing della Risposta**: La risposta JSON del modello, contenente i record estratti, viene analizzata.
7.  **Salvataggio su File**: La logica di business (`DataProcessor`) riceve i dati e utilizza il gestore di file (`FileHandler`) per salvarli in un file Excel nella directory specificata (o predefinita).
8.  **Logging**: Durante tutto il processo, vengono registrati log informativi per monitorare l'esecuzione e diagnosticare eventuali problemi.

## 4. Struttura del Codice

Il codice è organizzato in modo modulare per garantire manutenibilità e chiarezza:

- `run.py`: Entry point dell'applicazione.
- `src/main.py`: Definisce l'interfaccia a riga di comando (CLI) usando `click`.
- `src/logic.py`: Contiene la classe `DataProcessor` che orchestra il flusso di lavoro principale.
- `src/services.py`: Contiene le classi e le funzioni per le interazioni esterne:
  - `LLMClient`: Gestisce tutta la logica di comunicazione con l'API di OpenAI.
  - Funzioni per il salvataggio su Excel.
  - Funzioni per il caricamento della configurazione e il logging.
