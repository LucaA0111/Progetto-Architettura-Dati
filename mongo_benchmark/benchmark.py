import time

def run_benchmark(db_handler, docs, active_shards):
    print(f"\nAvvio test con {active_shards} shard attivi...")

    db_handler.clear_collection()

    start = time.time()
    db_handler.insert_documents(docs)
    end = time.time()

    duration = end - start
    print(f" Inseriti {len(docs)} documenti in {duration:.2f} secondi")

    return {
        "active_shards": active_shards,
        "documents": len(docs),
        "duration_seconds": round(duration, 2)
    }
