import sys
from pathlib import Path

ROOT_DIR = sys.path.append(str(Path(__file__).resolve().parent.parent))

# Create data files if they don't exist
from config import TYPES_FILE, COLLECTIONS_FILE, GROUP_FILE
for file_path in [TYPES_FILE, COLLECTIONS_FILE, GROUP_FILE]:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)

from src.ui.menu import main_menu

def main():
    main_menu().run()

if __name__ == "__main__":
    main()
