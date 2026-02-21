import os

from config import COLLECTIONS_FILE

def load_collections(collections_file=COLLECTIONS_FILE):
    if not os.path.exists(collections_file):
        return []
    with open(collections_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def add_collection(collection_name, collections_file=COLLECTIONS_FILE):
    collections = load_collections(collections_file)

    if collection_name in collections:
        print(f"➖ ℹ️ Collection '{collection_name}' already exists in the collections list.")
        print("➖ Ignoring new addition to the collections list.")
        return False
    else:
        collections.append(collection_name)
        collections.sort()

        with open(collections_file, 'w', encoding='utf-8') as f:
            for col in collections:
                f.write(f"{col}\n")

        print(f"➖ ✅ Added '{collection_name}' into the collections list.")
        return True
