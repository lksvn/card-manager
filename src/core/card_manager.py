import os
import re
import time

from config import CARDS_DIR, IMAGES_DIR, CUSTOM_TYPE_OVERRIDES, TYPES_FILE
from src.ui.cli import clear_screen, prompt
from src.utils.text import normalize_type

def load_card_types(types_file=TYPES_FILE):
    with open(types_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def createCardFile(card_data, img_filename, valid_types, additional_info="", group=None, cards_dir=CARDS_DIR):
    os.makedirs(cards_dir, exist_ok=True)
    filename = f"{card_data['flavor_name'] if card_data['flavor_name'] else card_data['name']}.md"
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filepath = os.path.join(cards_dir, filename)

    if os.path.exists(filepath):
        print(f"⚠️ Duplicate found: {filename}.")
        newfilename = prompt("✏️ Enter a new filename:", "➖ ✅ No changes made.", return_key='')
        if not newfilename:
            newfilename = f"{card_data['flavor_name'] if card_data['flavor_name'] else card_data['name']} - {card_data['number']}.md"
        if not newfilename.endswith('.md'):
            newfilename += '.md'
        filepath = os.path.join(cards_dir, newfilename)
        filename = newfilename

    normalized_type = normalize_type(card_data['type'], valid_types, CUSTOM_TYPE_OVERRIDES)

    content = f"""---
Collection: "{card_data['formatted_collection']}"
Type: {normalized_type}
Number: {card_data['number']}
Group: {group if group else ''}
Cover: "[[{img_filename}]]"
---
{additional_info}"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def deleteCardFile():
    clear_screen()
    print("🗑️ Delete Card File 🗑️")

    search = prompt("🔍 Enter card name to delete (or 'q' to quit):", return_key='q', delay=True)
    if search is not None:    
        matches = [file for file in os.listdir(CARDS_DIR)
                    if file.lower().endswith('.md') and search in file.lower()]

        if not matches:
            print("➖ ❌ No matching cards found. Please try again.")
            time.sleep(2)
            deleteCardFile()
            return

        print("➖ 🗂️ Matching cards:")
        for idx, file in enumerate(matches, 1):
            print(f"{idx}. {file}")   

        choice = prompt("➖ 🗑️ Enter the number of the card to delete (or 'q' to quit):", return_key='q', delay=True)
        if choice is not None and choice != 'q':
            if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
                print("➖ ❌ Invalid selection.")
                time.sleep(2)
                deleteCardFile()
                return

            selected = matches[int(choice) - 1]

            filepath = os.path.join(CARDS_DIR, selected)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            img_match = re.search(r'Cover:\s*"\[\[\s*(.*?)\s*\]\]"', content)
            img_file = img_match.group(1) if img_match else None

            confirm = prompt(f"➖ Are you sure you want to delete '{selected}' and its image '{img_file}'? (y/n):", "➖ ❌ Deletion cancelled.", return_key='n')
            if confirm is not None:            
                os.remove(filepath)
                print(f"➖ ✅ Deleted card file: {selected}")

                if img_file:
                    img_file = img_file.strip().replace('"', '').replace("'", "")
                    if img_file.lower() != "placeholder.jpg":
                        img_path = os.path.join(IMAGES_DIR, img_file)
                        if os.path.exists(img_path):
                            try:
                                os.remove(img_path)
                                print(f"➖ ✅ Deleted image file: {img_file}")
                            except Exception as e:
                                print(f"➖ ❌ Error deleting image {img_file}: {e}")
                        else:
                            print(f"➖ ⚠️ Image file not found: {img_file}")

                again = prompt("➖ Delete another card? (y/n):")
                if again is not None:
                    deleteCardFile()

def remove_unused_images():
    clear_screen()
    print("🔍 Scanning for unused images")

    images = set(os.listdir(IMAGES_DIR))
    images = images - {'placeholder.jpg'}
    cards = [f for f in os.listdir(CARDS_DIR) if f.lower().endswith('.md')]
    used_images = set()

    for card_file in cards:
        with open(os.path.join(CARDS_DIR, card_file), 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'Cover:\s*"\[\[\s*(.*?)\s*\]\]"', content)
        if match:
            img = match.group(1).strip()
            if img and img.lower() != 'placeholder.jpg':
                used_images.add(img)
    
    unused_images = images - used_images

    if not unused_images:
        print("➖ ✅ No unused image(s) found.")
        print("↩️ Returning to main menu.")
        time.sleep(2.5)
        return
    
    print("➖ 🗑️ Unused image(s) found:")
    for idx, img in enumerate(unused_images, 1):
        print(f"{idx}. {img}")

    confirm = prompt("➖ Do you want to delete these unused images? (y/n):", "➖ ❌ Deletion cancelled. ↩️ Returning to main menu.", return_key='n')
    if confirm is not None:
        for img in unused_images:
            try:
                os.remove(os.path.join(IMAGES_DIR, img))
                print(f"➖ ✅ Deleted: {img}")
            except Exception as e:
                print(f"➖ ❌ Error deleting {img}: {e}")

        print("➖ ✅ All unused images deleted.")
        print("↩️ Returning to main menu.")
        time.sleep(2.5)
        return
