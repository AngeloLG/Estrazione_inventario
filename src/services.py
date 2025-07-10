"""
Questo modulo gestisce le interazioni con servizi esterni.

Include la gestione della configurazione, il logging, le chiamate all'LLM
e le operazioni sul file system.
"""
import os
import logging
import pandas as pd
from typing import List, Dict
from dotenv import load_dotenv
import fitz  # PyMuPDF
import base64
import json
from openai import OpenAI


# --- Funzioni di Configurazione e Logging ---

def setup_logger() -> logging.Logger:
    """Configura e restituisce un logger per l'applicazione."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("estrazione_inventario_logger")

def load_api_key() -> str:
    """Carica la chiave API di OpenAI dal file .env."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("La chiave OPENAI_API_KEY non è stata trovata nel file .env.")
    return api_key

# --- Gestore di File ---

def save_to_excel(data: List[Dict[str, str]], output_path: str, logger: logging.Logger):
    """Salva una lista di dati in un file Excel."""
    if not output_path.endswith('.xlsx'):
        raise ValueError("Il percorso di output deve terminare con .xlsx")
    try:
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        logger.info(f"Dati salvati con successo in: {output_path}")
    except Exception as e:
        logger.error(f"Impossibile salvare il file Excel. Errore: {e}")
        raise IOError(f"Errore durante la scrittura del file: {e}") from e

# --- Client LLM ---

class LLMClient:
    """Client per interagire con il modello linguistico (LLM)."""
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("La chiave API non può essere vuota.")
        self.client = OpenAI(api_key=api_key)

    def _pdf_to_base64_images(self, pdf_path: str):
        """Converte le pagine di un PDF in una lista di immagini in formato base64."""
        try:
            pdf_document = fitz.open(pdf_path)
            base64_images = []
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                base64_images.append(base64.b64encode(img_bytes).decode('utf-8'))
            return base64_images
        except Exception as e:
            raise IOError(f"Errore durante la lettura o conversione del file PDF: {e}") from e

    def extract_data_from_pdf(self, pdf_path: str, prompt: str) -> List[Dict[str, str]]:
        """
        Estrae dati strutturati da un PDF inviando le sue pagine come immagini a GPT-4o.
        """
        base64_images = self._pdf_to_base64_images(pdf_path)
        
        messages = [
            {
                "role": "system",
                "content": """
                Sei un assistente esperto nell'estrazione di dati da documenti.
                Analizza le immagini fornite, che rappresentano le pagine di un documento.
                Rispondi SEMPRE E SOLO con un oggetto JSON.
                L'oggetto JSON deve contenere una singola chiave, "records", che è una lista di oggetti.
                Ogni oggetto nella lista rappresenta un record bibliografico estratto.
                Non includere mai testo, spiegazioni o commenti al di fuori dell'oggetto JSON.
                """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    *map(lambda img: {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}, base64_images)
                ]
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
            response_content = response.choices[0].message.content
            # Pulisce la risposta per assicurarsi che sia un JSON valido
            clean_json_str = response_content.strip().replace("```json", "").replace("```", "").strip()
            
            # Parsing del JSON per estrarre la lista di record
            json_data = json.loads(clean_json_str)
            return json_data.get("records", [])

        except Exception as e:
            # Gestisce errori API o di parsing JSON
            raise RuntimeError(f"Errore durante la chiamata all'API di OpenAI o nel parsing della risposta: {e}") from e 