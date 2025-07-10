# Estrazione Inventario

`Estrazione_inventario` è un'applicazione a riga di comando (CLI) sviluppata in Python che automatizza l'estrazione di record bibliografici da file PDF. Utilizzando il modello multimodale **GPT-4o** di OpenAI, lo strumento analizza il contenuto del PDF basandosi su un prompt fornito dall'utente e struttura i dati estratti in un file Excel (`.xlsx`).

Questo strumento è stato progettato per essere semplice, efficiente e facilmente manutenibile.

---

## Requisiti

- Python 3.8 o superiore
- Una **chiave API di OpenAI** valida, con accesso al modello `gpt-4o`.
- Gestore di pacchetti `pip`.

---

## Installazione

Per installare e configurare l'applicazione, segui questi passaggi:

1.  **Clona il repository**

    ```bash
    git clone <URL_DEL_TUO_REPOSITORY>
    cd estrazione_inventario
    ```

2.  **Crea e attiva un ambiente virtuale**

    ```bash
    # Su Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Su macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installa le dipendenze**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura la chiave API**
    L'applicazione richiede una chiave API di OpenAI. Copia il file di esempio `.env.example` in un nuovo file `.env` e inserisci la tua chiave API.
    ```
    OPENAI_API_KEY="la_tua_chiave_api_qui"
    ```

---

## Utilizzo

Esegui lo script `run.py` per lanciare l'applicazione. L'operazione contatterà le API di OpenAI e potrebbe avere un costo associato.

### Comando Base

```bash
python run.py --file-path <PERCORSO_PDF> --prompt "<TESTO_PROMPT>"
```

### Argomenti

- `--file-path` (obbligatorio): Il percorso del file PDF da cui estrarre i dati.
- `--prompt` (obbligatorio): La richiesta testuale che guida l'LLM (es. "Estrai tutti i libri con titolo, autore e anno, includendo anche le note manoscritte").
- `--output-dir` (opzionale): La directory in cui salvare il file Excel. Se omesso, verrà salvato nella stessa directory del PDF.

### Esempi di Utilizzo

**1. Esempio base**

```bash
python run.py --file-path ./documenti/inventario.pdf --prompt "Estrai titolo, autore e anno di pubblicazione per ogni libro"
```

_Questo comando analizza `inventario.pdf` e salva l'output come `inventario.xlsx` nella stessa cartella._

**2. Esempio con directory di output**

```bash
python run.py --file-path ./lista_libri.pdf --prompt "Estrai tutti i record bibliografici" --output-dir ./output
```

_Questo comando analizza `lista_libri.pdf` e salva l'output in `output/lista_libri.xlsx`._

---

## Struttura del Progetto

Il progetto ha una struttura semplificata per favorire la leggibilità:

- `run.py`: Entry point per l'utente.
- `src/`: Cartella per tutto il codice sorgente Python.
  - `main.py`: Contiene la definizione della CLI.
  - `logic.py`: Contiene la logica di business e i modelli dei dati.
  - `services.py`: Gestisce le interazioni con l'esterno (LLM, file system, config).
- `requirements.txt`: Elenco delle dipendenze.
- `.env.example`: File di esempio per le variabili d'ambiente.
