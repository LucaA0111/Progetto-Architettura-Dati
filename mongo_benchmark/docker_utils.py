import subprocess

ALL_SHARDS = ["shard1", "shard2", "shard3", "shard4"]

def set_active_shards(n_shards: int):
    """
    Attiva i primi n_shards e ferma gli altri shard.
    """
    for i, shard in enumerate(ALL_SHARDS, start=1):
        if i <= n_shards:
            print(f"Avvio {shard}...")
            subprocess.run(["docker", "start", shard], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"Stop {shard}...")
            subprocess.run(["docker", "stop", shard], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
