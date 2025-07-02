import json
import os

def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        docs = json.load(f)
    for i, doc in enumerate(docs):
        if "_id" not in doc:
            doc["_id"] = i
    return docs

def load_all_json_from_folder(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_map = {}
    for file_name in json_files:
        full_path = os.path.join(folder_path, file_name)
        data_map[file_name] = load_data_from_json(full_path)
    return data_map
