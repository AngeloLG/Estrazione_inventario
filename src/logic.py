"""
Questo modulo contiene la logica di business (core) dell'applicazione.

Include sia i modelli di dati che la classe che orchestra il flusso di lavoro.
"""
import logging
from dataclasses import dataclass
from typing import Optional, List, Dict
from .services import LLMClient, save_to_excel

# --- Modello dei Dati ---

@dataclass
class BibliographicRecord:
    """Rappresenta un singolo record bibliografico strutturato."""
    Titolo: str
    Autore: str
    Anno: Optional[int] = None
    Editore: Optional[str] = None
    Descrizione_fisica: Optional[str] = None
    Note: Optional[str] = None

# --- Processore di Dati ---

class DataProcessor:
    """Orchestra il processo di estrazione e salvataggio dei dati."""
    def __init__(self, llm_client: LLMClient, logger: logging.Logger):
        self.llm_client = llm_client
        self.logger = logger

    def process(self, pdf_path: str, prompt: str, output_path: str):
        """Esegue l'intero flusso di lavoro: estrae i dati e li salva."""
        self.logger.info(f"Avvio del processo per il file '{pdf_path}'.")
        try:
            # 1. Estrazione dati tramite LLM
            extracted_data = self.llm_client.extract_data_from_pdf(pdf_path, prompt)
            if not extracted_data:
                self.logger.warning("L'LLM non ha restituito alcun dato.")
                return

            self.logger.info(f"Dati estratti con successo: {len(extracted_data)} record.")
            
            # Qui si potrebbero validare i dati usando BibliographicRecord

            # 2. Salvataggio su file Excel
            save_to_excel(extracted_data, output_path, self.logger)
            self.logger.info("Processo completato con successo.")
        except Exception as e:
            self.logger.error(f"Il processo si è interrotto: {e}", exc_info=True)
            raise 