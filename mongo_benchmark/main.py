import os
from datetime import datetime
from db_handler import MongoDBHandler
from data_loader import load_all_json_from_folder
from benchmark import run_benchmark
from utils import save_results_to_csv
from docker_utils import set_active_shards

def main():
    DATA_FOLDER = "json_files"
    CSV_OUTPUT_FOLDER = "csv_output"

    # Chiedi all’utente di scegliere un numero di shard tra 1 e 4
    while True:
        try:
            n_shards = int(input("Inserisci il numero di shard da utilizzare (1-4): "))
            if 1 <= n_shards <= 4:
                break
            else:
                print("Devi inserire un numero tra 1 e 4.")
        except ValueError:
            print("Input non valido, inserisci un numero intero tra 1 e 4.")

    # Attiva/disattiva automaticamente i nodi Docker
    print(f"\nGestione automatica dei nodi Docker per {n_shards} shard")
    set_active_shards(n_shards)

    # Carica tutti i dati JSON dalla cartella
    data_map = load_all_json_from_folder(DATA_FOLDER)

    # Crea cartella output se non esiste
    os.makedirs(CSV_OUTPUT_FOLDER, exist_ok=True)

    db_handler = MongoDBHandler()
    results = []

    for file_name, docs in data_map.items():
        print(f"\nElaborazione file: {file_name} ({len(docs)} documenti)")
        result = run_benchmark(db_handler, docs, n_shards)
        result["file"] = file_name
        results.append(result)

    # Nome file con data, ora e numero shard usati
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(CSV_OUTPUT_FOLDER, f"benchmark_{timestamp}_shards_{n_shards}.csv")

    save_results_to_csv(results, output_file)
    print(f"\nRisultati salvati in '{output_file}'")

if __name__ == "__main__":
    main()
