from config import COLLECTIONS_FILE, TYPES_FILE
from src.core.card_manager import deleteCardFile, edit_card_metadata, remove_unused_images
from src.core.collection import recreate_collection_list
from src.core.grouping import load_grouping_tags, list_grouping_tag, add_grouping_tag, delete_grouping_tag, edit_grouping_tag
from src.ui.card_actions import handle_add_card
from src.ui.cli import Menu, manage_list
from src.utils.types import load_types

def grouping_tags_menu() -> Menu:
    """Menu for managing grouping tags (list, add, delete, edit)."""
    def run_list():
        tags = load_grouping_tags()
        list_grouping_tag(tags)
    
    def run_add():
        tags = load_grouping_tags()
        add_grouping_tag(tags)

    def run_delete():
        tags = load_grouping_tags()
        delete_grouping_tag(tags)

    def run_edit():
        tags = load_grouping_tags()
        edit_grouping_tag(tags)

    return Menu("Grouping Tags Menu", {
        '1': ("List all grouping tags", run_list),
        '2': ("Add a new tag", run_add),
        '3': ("Delete a tag", run_delete),
        '4': ("Edit a tag", run_edit),
    })

def card_mgmt_menu() -> Menu:
    """Submenu for card management options (add, edit, delete)."""
    return Menu("Card Management", {
        '1': ("Add a card", lambda: handle_add_card(load_types())),
        '2': ("Edit a card", lambda: edit_card_metadata(load_types())),
        '3': ("Find and delete a card", deleteCardFile),
    })

def utils_menu() -> Menu:
    """Submenu for utility options."""
    return Menu("Utilities", {
        '1': ("Remove unused images", remove_unused_images),
        '2': ("View/Edit collection list", lambda: manage_list(COLLECTIONS_FILE, "Collections")),
        '3': ("Recreate collection list", recreate_collection_list),
        '4': ("View/Edit type list", lambda: manage_list(TYPES_FILE, "Card Types")),
    })

def main_menu() -> Menu:
    """Main menu for the MTG Card Manager application."""
    return Menu("MTG Card Scraper", {
        '1': ("Card Management", lambda: card_mgmt_menu()),
        '2': ("Utilities", lambda: utils_menu()),
        '3': ("Grouping Tags", lambda: grouping_tags_menu()),
    })
