import time
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Create data files if they don't exist
from pathlib import Path
from config import TYPES_FILE, COLLECTIONS_FILE, GROUP_FILE
for file_path in [TYPES_FILE, COLLECTIONS_FILE, GROUP_FILE]:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

from src.api.scryfall import get_card_data, download_image
from src.core.collection import add_collection
from src.core.card_manager import createCardFile, deleteCardFile, load_card_types, remove_unused_images
from src.core.grouping import choose_grouping_tag, grouping_tags_menu
from src.ui.cli import clear_screen, prompt
from src.utils.text import normalize_card_name

def handle_add_card(valid_types):
    while True:
        url = input("🔗 Enter Scryfall card URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            print("↩️ Returning to main menu.")
            time.sleep(2)
            break

        try:
            print("🔍 Fetching card data from API")
            card_data = get_card_data(url)
            print(f"➖ ✅ Found: {card_data['name']} - {card_data['formatted_collection']}")

            print("🔄 Checking the collection list")
            add_collection(card_data['formatted_collection'])

            if card_data['image_url']:
                print("🖼️ Downloading card image")
                filename = f"{card_data['set_code'].lower()}-{card_data['number']}-{normalize_card_name(card_data['name'])}.png"
                img_filename = download_image(card_data['image_url'], filename)
                print(f"➖ ✅ Done: {img_filename}")
            else:
                img_filename = "placeholder.jpg"
                print("➖ ⚠️ No image URL found")

            print("📝 Gathering additional card info")
            additional_info = prompt("➖ Additional information (notes/comments about this card):", '➖ ✅ No additional information added.')
            group = choose_grouping_tag()

            print("📜 Creating markdown file")
            cardFile = createCardFile(card_data, img_filename, valid_types, additional_info, group)
            print(f"➖ ✅ New card added: {cardFile}")

        except Exception as e:
            print(f"❌ Error: {e}")

        again = input("➕ Add another card? (y/n): ").strip().lower()
        if again != 'y':
            print("↩️ Returning to main menu.")
            time.sleep(2)
            break

def display_menu():
    print("🕹️ MTG Card Scraper for Scryfall (API) 🕹️")
    print("⚙️ Options:")
    print("1. Add a card")
    print("2. Find and delete a card")
    print("3. Remove unused images")
    print("4. Grouping Tags")
    print("q. Quit")
    return input("➖ ").strip().lower()

def main():
    try:
        valid_types = load_card_types()
    except FileNotFoundError:
        print("⚠️ types.md not found, using raw types from Scryfall")
        valid_types = []

    menu_actions = {
        '1': lambda: handle_add_card(valid_types),
        '2': deleteCardFile,
        '3': remove_unused_images,
        '4': grouping_tags_menu,
    }

    while True:
        clear_screen()
        choice = display_menu()

        if choice in ['q', 'quit', 'exit', '']:
            print("👋 Exiting program. Goodbye!")
            sys.exit(0)

        action = menu_actions.get(choice)
        if action:
            action()
            if choice != '1' and choice != '4':
                input("➖ Press Enter to return to the menu...")
        else:
            print("❌ Invalid choice, please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
