from pymongo import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
from .settings import MONGODB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.clients = {}
        self.config = MONGODB_CONFIG

    def get_sharded_client(self, read_concern='majority', write_concern='majority'):
        """
        Client per cluster sharded (mongos router)
        """
        key = f"sharded_{read_concern}_{write_concern}"

        if key not in self.clients:
            # Connessione tramite mongos router
            connection_string = "mongodb://localhost:27020/"

            self.clients[key] = MongoClient(
                connection_string,
                read_concern=ReadConcern(read_concern),
                write_concern=WriteConcern(write_concern),
                read_preference=ReadPreference.SECONDARY_PREFERRED
            )

        return self.clients[key]

    def get_replica_client(self, nodes_count=4, read_concern='majority', write_concern='majority'):
        """
        Client per replica set (per test transazioni)
        """
        key = f"replica_{nodes_count}_{read_concern}_{write_concern}"

        if key not in self.clients:
            # Costruisci connection string per replica set
            hosts = []
            for i in range(nodes_count):
                port = 27021 + i  # Porte del replica set
                hosts.append(f"localhost:{port}")

            connection_string = f"mongodb://{','.join(hosts)}/"

            self.clients[key] = MongoClient(
                connection_string,
                replicaSet="rs0",
                read_concern=ReadConcern(read_concern),
                write_concern=WriteConcern(write_concern),
                read_preference=ReadPreference.SECONDARY_PREFERRED
            )

        return self.clients[key]

    def get_single_shard_client(self, shard_number, read_concern='majority', write_concern='majority'):
        """
        Client per connessione diretta a singolo shard
        """
        key = f"shard_{shard_number}_{read_concern}_{write_concern}"

        if key not in self.clients:
            # Mappa shard number alla porta
            port_map = {
                1: 27018,  # shard1
                2: 27017,  # shard2
                3: 27016,  # shard3
                4: 27015  # shard4
            }

            if shard_number not in port_map:
                raise ValueError(f"Invalid shard number: {shard_number}")

            port = port_map[shard_number]
            connection_string = f"mongodb://localhost:{port}/"

            self.clients[key] = MongoClient(
                connection_string,
                read_concern=ReadConcern(read_concern),
                write_concern=WriteConcern(write_concern)
            )

        return self.clients[key]

    def get_multi_shard_client(self, shard_numbers, read_concern='majority', write_concern='majority'):
        """
        Client per connessione a multipli shard (per test scalabilità)
        """
        key = f"multi_shard_{'_'.join(map(str, shard_numbers))}_{read_concern}_{write_concern}"

        if key not in self.clients:
            port_map = {
                1: 27018,  # shard1
                2: 27017,  # shard2
                3: 27016,  # shard3
                4: 27015  # shard4
            }

            hosts = []
            for shard_num in shard_numbers:
                if shard_num in port_map:
                    hosts.append(f"localhost:{port_map[shard_num]}")

            if not hosts:
                raise ValueError(f"No valid shards found: {shard_numbers}")

            connection_string = f"mongodb://{','.join(hosts)}/"

            self.clients[key] = MongoClient(
                connection_string,
                read_concern=ReadConcern(read_concern),
                write_concern=WriteConcern(write_concern)
            )

        return self.clients[key]

    def close_all_connections(self):
        """
        Chiude tutte le connessioni
        """
        for client in self.clients.values():
            client.close()
        self.clients.clear()