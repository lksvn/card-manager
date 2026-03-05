import re
from config import COLLECTIONS_FILE, CARDS_DIR
from pathlib import Path

def load_collections(collections_file: Path = COLLECTIONS_FILE) -> list[str]:
    """Load collections from the collections file. Returns a list of collection names."""
    
    if not collections_file.exists():
        return []
    content = collections_file.read_text(encoding='utf-8')
    return [ line.strip() for line in content.splitlines() if line.strip() ]

def add_collection(
    collection_name: str, 
    collections_file: Path = COLLECTIONS_FILE
) -> bool:
    """Add a new collection to the collections file if it doesn't already exist. Returns True if added, False if duplicate."""
    
    collections = load_collections(collections_file)

    if collection_name in collections:
        print(f"➖ ℹ️ Collection '{collection_name}' already exists in the collections list.")
        print("➖ Ignoring new addition to the collections list.")
        return False
    else:
        collections.append(collection_name)
        collections.sort()

        collections_file.write_text('\n'.join(collections) + '\n', encoding='utf-8')

        print(f"➖ ✅ Added '{collection_name}' into the collections list.")
        return True

def recreate_collection_list(
    cards_dir: Path = CARDS_DIR,
    collections_file: Path = COLLECTIONS_FILE
) -> None:
    """Scan all card files in the cards directory, extract unique collection names, and recreates the collections file."""

    print(f"🔍 Scanning {cards_dir} for collections...")
    collections = set()
    
    if not cards_dir.exists():
        print(f"❌ Error: Cards directory {cards_dir} does not exist.")
        return

    for file_path in cards_dir.iterdir():
        if file_path.is_file() and file_path.suffix == '.md':
            try:
                content = file_path.read_text(encoding='utf-8')
                # Look for Collection: "Value" or Collection: Value
                match = re.search(r'Collection:\s*"(.*?)"', content)
                if not match:
                    match = re.search(r'Collection:\s*(.*)', content)
                if match:
                    col = match.group(1).strip()
                    if col and not col == 'Any':
                        collections.add(col)
            except Exception as e:
                print(f"⚠️ Could not read {file_path}: {e}")
    
    if not collections:
        print("➖ ⚠️ No collections found in card files.")
        return

    sorted_collections = sorted(list(collections))
    collections_file.write_text('\n'.join(sorted_collections) + '\n', encoding='utf-8')

    print(f"➖ ✅ Recreated {collections_file} with {len(sorted_collections)} collections.")
