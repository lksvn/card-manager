import re
import time

from pathlib import Path
from config import CARDS_DIR, IMAGES_DIR, CUSTOM_TYPE_OVERRIDES
from src.ui.cli import clear_screen, prompt
from src.utils.text import get_image_filename, normalize_type
from src.core.grouping import choose_grouping_tag
from src.models.card import Card

def createCardFile(
    card: Card, 
    img_filename: str, 
    valid_types: list[str],
    additional_info: str ="",
    group: str | None = None, 
    cards_dir: Path = CARDS_DIR
) -> str:
    
    cards_dir.mkdir(parents=True, exist_ok=True)

    filename = get_image_filename(card.flavor_name or card.name, extension=".md")
    filepath = cards_dir / filename

    if filepath.exists():
        print(f"⚠️ Duplicate found: {filename}.")
        newfilename = prompt("✏️ Enter a new filename:", "➖ ✅ No changes made.", return_key='')

        if not newfilename:
            newfilename = f"{card.flavor_name or card.name} - {card.number}"

        filename = Path(newfilename).with_suffix('.md').name
        filepath = cards_dir / filename

    normalized_type = normalize_type(card.type, valid_types, CUSTOM_TYPE_OVERRIDES)

    content = f"""---
Collection: "{card.formatted_collection}"
Type: {normalized_type}
Number: {card.number}
Group: {group if group else ''}
Cover: "[[{img_filename}]]"
---
{additional_info}"""
    
    filepath.write_text(content, encoding='utf-8')
    return filename

def deleteCardFile():
    clear_screen()
    print("🗑️ Delete Card File 🗑️")

    search = prompt("🔍 Enter card name to delete (or 'q' to quit):", return_key='q', delay=True)
    if search is not None:    
        # iterdir returns Path objects
        matches = [f.name for f in CARDS_DIR.iterdir()
                    if f.suffix == '.md' and search in f.name.lower()]
        
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

            filepath = CARDS_DIR / selected
            content = filepath.read_text(encoding='utf-8')
            
            img_match = re.search(r'Cover:\s*"\[\[\s*(.*?)\s*\]\]"', content)
            img_file = img_match.group(1) if img_match else None

            confirm = prompt(f"➖ Are you sure you want to delete '{selected}' and its image '{img_file}'? (y/n):", "➖ ❌ Deletion cancelled.", return_key='n')
            if confirm is not None:
                filepath.unlink(missing_ok=True)
                print(f"➖ ✅ Deleted card file: {selected}")

                if img_file:
                    img_file = img_file.strip().replace('"', '').replace("'", "")
                    if img_file.lower() != "placeholder.jpg":
                        img_path = IMAGES_DIR / img_file
                        if img_path.exists():
                            try:
                                img_path.unlink(missing_ok=True)
                                print(f"➖ ✅ Deleted image file: {img_file}")
                            except Exception as e:
                                print(f"➖ ❌ Error deleting image {img_file}: {e}")
                        else:
                            print(f"➖ ⚠️ Image file not found: {img_file}")

                again = prompt("➖ Delete another card? (y/n):")
                if again is not None:
                    deleteCardFile()

def edit_card_metadata(valid_types: list[str]) -> None:
    clear_screen()
    print("✏️ Edit Card Metadata ✏️")

    search = prompt("🔍 Enter card name to edit (or 'q' to quit):", return_key='q', delay=True)
    if search is not None:    
        matches = [f.name for f in CARDS_DIR.iterdir()
                    if f.suffix == '.md' and search in f.name.lower()]
        
        if not matches:
            print("➖ ❌ No matching cards found.")
            time.sleep(2)
            return

        print("➖ 🗂️ Matching cards:")
        for idx, file in enumerate(matches, 1):
            print(f"{idx}. {file}")   

        choice = prompt("➖ ✏️ Enter the number of the card to edit (or 'q' to quit):", return_key='q', delay=True)
        if choice is not None and choice != 'q':
            if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
                print("➖ ❌ Invalid selection.")
                time.sleep(2)
                return

            selected = matches[int(choice) - 1]
            filepath = CARDS_DIR / selected

            try:
                content = filepath.read_text(encoding='utf-8')
                
                # Split content into YAML frontmatter and notes
                parts = content.split('---', 2)
                if len(parts) < 3:
                    print("➖ ❌ File does not have valid frontmatter.")
                    return
                
                frontmatter = parts[1]
                notes = parts[2].strip()

                # Parse frontmatter (rudimentary parsing)
                metadata = {}
                for line in frontmatter.strip().split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        metadata[k.strip()] = v.strip().replace('"', '')

                print(f"\nEditing '{selected}':")
                print(f"1. Collection: {metadata.get('Collection', 'N/A')}")
                print(f"2. Type: {metadata.get('Type', 'N/A')}")
                print(f"3. Group: {metadata.get('Group', 'None')}")
                print(f"4. Notes: {notes[:50]}...")
                
                change = prompt("\nEnter field number to edit (or 'q' to finish):", return_key='q')
                if not change: return

                if change == '1':
                    new_val = prompt(f"New collection (current: {metadata.get('Collection')}):")
                    if new_val: metadata['Collection'] = new_val
                elif change == '2':
                    new_val = normalize_type(prompt(f"New type (current: {metadata.get('Type')}):"), valid_types, CUSTOM_TYPE_OVERRIDES)
                    if new_val: metadata['Type'] = new_val
                elif change == '3':
                    new_val = choose_grouping_tag()
                    if new_val: metadata['Group'] = new_val
                elif change == '4':
                    new_val = prompt("New notes (will replace current notes):")
                    if new_val is not None: notes = new_val

                # Reconstruct file
                new_content = "---\n"
                for k, v in metadata.items():
                    if k in ['Collection', 'Cover']: # Add quotes back
                        new_content += f'{k}: "{v}"\n'
                    else:
                        new_content += f"{k}: {v}\n"
                new_content += f"---\n{notes}"

                filepath.write_text(new_content, encoding='utf-8')
                print(f"➖ ✅ Updated '{selected}'.")

            except Exception as e:
                print(f"➖ ❌ Error editing card: {e}")

def remove_unused_images():
    clear_screen()
    print("🔍 Scanning for unused images")

    # Get all images in the images directory
    images = set(f.name for f in IMAGES_DIR.iterdir() if f.is_file())
    images.discard('placeholder.jpg')  # Ignore placeholder
    # Get all card files
    cards = [f for f in CARDS_DIR.iterdir() if f.suffix == '.md']

    # Find all images that are referenced in card files
    used_images = set()
    for card_file in cards:
        content = card_file.read_text(encoding='utf-8')
        match = re.search(r'Cover:\s*"\[\[\s*(.*?)\s*\]\]"', content)
        if match:
            img = match.group(1).strip()
            if img and img.lower() != 'placeholder.jpg':
                used_images.add(img)
    
    # Find unused images
    unused_images = images - used_images

    if not unused_images:
        print("➖ ✅ No unused image(s) found.")
        return
    
    print("➖ 🗑️ Unused image(s) found:")
    for idx, img in enumerate(unused_images, 1):
        print(f"{idx}. {img}")

    confirm = prompt("➖ Do you want to delete these unused images? (y/n):", "➖ ❌ Deletion cancelled.", return_key='n')
    if confirm is not None:
        for img in unused_images:
            try:
                (IMAGES_DIR / img).unlink(missing_ok=True)
                print(f"➖ ✅ Deleted: {img}")
            except Exception as e:
                print(f"➖ ❌ Error deleting {img}: {e}")

        print("➖ ✅ All unused images deleted.")
