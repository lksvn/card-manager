import time
from src.api.scryfall import download_image, get_card_data
from src.core.card_manager import createCardFile
from src.ui.cli import prompt, clear_screen
from src.core.grouping import choose_grouping_tag
from src.utils.text import get_image_filename

def handle_add_card(valid_types: list[str]) -> None:
    clear_screen()
    print("🆕 Add a New Card 🆕")
    url = prompt("🔗 Enter Scryfall URL (or 'q' to quit):", return_key='q', delay=True)
    if url is None or url == 'q':
        return

    try:
        card = get_card_data(url) # Card Object
        if card is None:
            return
        
        print(f"➖ 🃏 Found: {card.name} ({card.set_code})")
        
        # Download image
        img_filename = get_image_filename(card.flavor_name or card.name)
        if not download_image(card.image_url, img_filename):
            print("⚠️ Failed to download image. Using placeholder image instead.")
            img_filename = "placeholder.jpg"

        # Optional grouping
        group = choose_grouping_tag()

        # Additional info (optional)
        additional_info = prompt("📝 Add notes/additional info (optional):", return_key='')

        # Create file
        filename = createCardFile(card, img_filename, valid_types, additional_info, group)
        print(f"➖ ✅ Created card file: {filename}")
        
        again = prompt("➕ Add another card? (y/n):")
        if again is not None:
            handle_add_card(valid_types)

    except Exception as e:
        print(f"➖ ❌ Error: {e}")
        time.sleep(2)