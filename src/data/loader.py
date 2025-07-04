import time
import logging
from typing import List, Dict, Any
from pymongo import InsertOne, ASCENDING, DESCENDING
from concurrent.futures import ThreadPoolExecutor, as_completed
from .generator import DataGenerator
from ..config.database import DatabaseManager


class DataLoader:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.data_generator = DataGenerator()
        self.logger = logging.getLogger(__name__)

    def load_test_data(self, db_name: str, collection_name: str,
                       document_count: int, nodes_count: int = 4) -> Dict[str, Any]:
        """
        Carica dati di test e misura performance
        """
        client = self.db_manager.get_client(nodes_count)
        db = client[db_name]
        collection = db[collection_name]

        # Genera dati
        self.logger.info(f"Generating {document_count} documents for {collection_name}")
        documents = self._generate_documents(collection_name, document_count)

        # Pulisce collezione esistente
        collection.drop()

        # Crea indici
        self._create_indexes(collection, collection_name)

        # Misura tempo di inserimento
        start_time = time.time()

        # Inserimento batch
        batch_size = 1000
        inserted_count = 0

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            collection.insert_many(batch)
            inserted_count += len(batch)

            if inserted_count % 10000 == 0:
                self.logger.info(f"Inserted {inserted_count}/{document_count} documents")

        end_time = time.time()

        # Statistiche
        insert_time = end_time - start_time
        docs_per_second = document_count / insert_time

        result = {
            'collection': collection_name,
            'document_count': document_count,
            'nodes_count': nodes_count,
            'insert_time': insert_time,
            'docs_per_second': docs_per_second,
            'avg_doc_size': len(str(documents[0])) if documents else 0,
            'total_size_mb': (len(str(documents)) / 1024 / 1024) if documents else 0
        }

        self.logger.info(f"Loaded {document_count} documents in {insert_time:.2f}s ({docs_per_second:.2f} docs/sec)")

        return result

    def load_data_parallel(self, db_name: str, collection_name: str,
                           document_count: int, nodes_count: int = 4,
                           thread_count: int = 4) -> Dict[str, Any]:
        """
        Carica dati in parallelo per migliorare performance
        """
        client = self.db_manager.get_client(nodes_count)
        db = client[db_name]
        collection = db[collection_name]

        # Genera dati
        documents = self._generate_documents(collection_name, document_count)

        # Pulisce collezione
        collection.drop()
        self._create_indexes(collection, collection_name)

        # Divide documenti in chunk per thread
        chunk_size = len(documents) // thread_count
        chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

        start_time = time.time()

        # Inserimento parallelo
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            for chunk in chunks:
                future = executor.submit(self._insert_chunk, collection, chunk)
                futures.append(future)

            # Attendi completamento
            inserted_count = 0
            for future in as_completed(futures):
                inserted_count += future.result()
                self.logger.info(f"Thread completed, total inserted: {inserted_count}")

        end_time = time.time()

        insert_time = end_time - start_time
        docs_per_second = document_count / insert_time

        return {
            'collection': collection_name,
            'document_count': document_count,
            'nodes_count': nodes_count,
            'thread_count': thread_count,
            'insert_time': insert_time,
            'docs_per_second': docs_per_second,
            'parallel_speedup': True
        }

    def _generate_documents(self, collection_name: str, count: int) -> List[Dict[str, Any]]:
        """
        Genera documenti basati sul tipo di collezione
        """
        if collection_name == 'users':
            return self.data_generator.generate_users(count)
        elif collection_name == 'orders':
            # Genera prima alcuni user_ids
            user_ids = [self.data_generator.fake.pymongo_objectid() for _ in range(count // 10)]
            return self.data_generator.generate_orders(count, user_ids)
        elif collection_name == 'products':
            return self.data_generator.generate_products(count)
        elif collection_name == 'transactions':
            user_ids = [self.data_generator.fake.pymongo_objectid() for _ in range(count // 10)]
            return self.data_generator.generate_transactions(count, user_ids)
        else:
            raise ValueError(f"Unknown collection type: {collection_name}")

    def _create_indexes(self, collection, collection_name: str):
        """
        Crea indici appropriati per ogni collezione
        """
        if collection_name == 'users':
            collection.create_index('email')
            collection.create_index('username')
            collection.create_index('registration_date')
        elif collection_name == 'orders':
            collection.create_index('user_id')
            collection.create_index('created_at')
            collection.create_index('status')
            collection.create_index('region')
        elif collection_name == 'products':
            collection.create_index('category')
            collection.create_index('price')
            collection.create_index('created_at')
        elif collection_name == 'transactions':
            collection.create_index('user_id')
            collection.create_index('created_at')
            collection.create_index('status')

    def _insert_chunk(self, collection, documents: List[Dict[str, Any]]) -> int:
        """
        Inserisce un chunk di documenti
        """
        batch_size = 1000
        inserted_count = 0

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            collection.insert_many(batch)
            inserted_count += len(batch)

        return inserted_count