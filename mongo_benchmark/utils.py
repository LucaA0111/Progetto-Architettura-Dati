import csv

def save_results_to_csv(results, output_file):
    with open(output_file, mode="w", newline="") as csvfile:
        fieldnames = ["file", "active_shards", "documents", "duration_seconds"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
