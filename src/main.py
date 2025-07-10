"""
Questo modulo definisce l'interfaccia a riga di comando (CLI)
e funge da entry point per l'applicazione.
"""
import click
import os
from .services import setup_logger, load_api_key, LLMClient
from .logic import DataProcessor

@click.command()
@click.option(
    '--file-path',
    'pdf_path',
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Percorso del file PDF da analizzare."
)
@click.option(
    '--prompt',
    required=True,
    type=str,
    help="Prompt da utilizzare per l'estrazione dei dati."
)
@click.option(
    '--output-dir',
    type=click.Path(file_okay=False, writable=True),
    default=None,
    help="Directory dove salvare il file Excel. Default: stessa directory del PDF."
)
def run(pdf_path, prompt, output_dir):
    """Esegue il processo di estrazione dei metadati da un file PDF."""
    logger = setup_logger()
    logger.info("--- Avvio Applicazione ---")

    try:
        # 1. Composizione delle dipendenze
        api_key = load_api_key()
        llm_client = LLMClient(api_key=api_key)
        processor = DataProcessor(llm_client=llm_client, logger=logger)

        # 2. Calcolo del percorso di output
        if output_dir:
            base_name = os.path.basename(pdf_path)
            file_name, _ = os.path.splitext(base_name)
            output_path = os.path.join(output_dir, f"{file_name}.xlsx")
        else:
            dir_name = os.path.dirname(pdf_path)
            file_name, _ = os.path.splitext(os.path.basename(pdf_path))
            output_path = os.path.join(dir_name, f"{file_name}.xlsx")

        # 3. Esecuzione del processo
        processor.process(pdf_path, prompt, output_path)
        click.echo(f"Successo! File di output creato in: {output_path}")

    except Exception as e:
        logger.error(f"Esecuzione fallita: {e}")
        click.echo(f"ERRORE: {e}. Controlla i log per maggiori dettagli.", err=True)
    finally:
        logger.info("--- Chiusura Applicazione ---") 