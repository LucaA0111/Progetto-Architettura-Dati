import os

# Configurazione MongoDB
MONGODB_CONFIG = {
    'replica_set': 'rs0',
    'sharded_cluster': {
        'mongos_port': 27020,
        'config_server_port': 27019,
        'shard_ports': {
            1: 27018,  # shard1
            2: 27017,  # shard2
            3: 27016,  # shard3
            4: 27015   # shard4
        }
    },
    'replica_set_ports': {
        1: 27021,  # mongo1
        2: 27022,  # mongo2
        3: 27023,  # mongo3
        4: 27024   # mongo4
    },
    'max_pool_size': 100,
    'socket_timeout_ms': 30000,
    'server_selection_timeout_ms': 5000
}

# Configurazione test
TEST_CONFIG = {
    'base_data_size': 100000,  # 100K documenti base
    'test_databases': ['test_scalability', 'test_resilience', 'test_isolation'],
    'test_collections': ['users', 'orders', 'products', 'transactions'],
    'data_percentages': [25, 50, 75, 100],
    'shard_configurations': [1, 2, 3, 4],  # Numero di shard da utilizzare
    'replica_configurations': [1, 2, 3, 4]  # Numero di nodi replica
}

# Configurazione sharding
SHARDING_CONFIG = {
    'strategies': ['range', 'hash', 'zone', 'compound'],
    'shard_keys': {
        'users': {
            'range': {'registration_date': 1},
            'hash': {'_id': 'hashed'},
            'zone': {'address.country': 1},
            'compound': {'address.country': 1, 'registration_date': 1}
        },
        'orders': {
            'range': {'created_at': 1},
            'hash': {'_id': 'hashed'},
            'zone': {'region': 1},
            'compound': {'user_id': 1, 'created_at': 1}
        },
        'products': {
            'range': {'category': 1},
            'hash': {'_id': 'hashed'},
            'zone': {'category': 1},
            'compound': {'category': 1, 'price': 1}
        },
        'transactions': {
            'range': {'created_at': 1},
            'hash': {'_id': 'hashed'},
            'zone': {'user_id': 1},
            'compound': {'user_id': 1, 'created_at': 1}
        }
    },
    'zones': {
        'europe': {'address.country': {'$in': ['Italy', 'France', 'Germany', 'Spain']}},
        'america': {'address.country': {'$in': ['USA', 'Canada', 'Mexico']}},
        'asia': {'address.country': {'$in': ['Japan', 'China', 'India']}}
    }
}

# Configurazione risultati
RESULTS_CONFIG = {
    'output_dir': 'results',
    'raw_data_dir': 'results/raw_data',
    'reports_dir': 'results/reports',
    'visualizations_dir': 'results/visualizations'
}

# Configurazione test isolamento
ISOLATION_CONFIG = {
    'read_concerns': ['local', 'available', 'majority', 'linearizable', 'snapshot'],
    'write_concerns': ['majority', 'w1', 'w2', 'w3'],
    'transaction_scenarios': [
        'dirty_read',
        'non_repeatable_read',
        'phantom_read',
        'lost_update',
        'write_skew'
    ]
}