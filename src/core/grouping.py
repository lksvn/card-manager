import time

from pathlib import Path
from config import GROUP_FILE
from src.ui.cli import clear_screen, prompt

def load_grouping_tags(
    group_file: Path = GROUP_FILE
) -> list[str]:
    """Load grouping tags from the group file. Returns a list of grouping tags."""    
    if not group_file.exists():
        return []
    return [line.strip() for line in group_file.read_text(encoding='utf-8').splitlines() if line.strip()]

def tag_list(
    tags: list[str], 
    show_header: bool = True
) -> None:
    """Helper function to display a numbered list of grouping tags."""
    if show_header: print("📋 Existing tags:")
    for idx, tag in enumerate(tags, start=1):
        print(f"{idx}. {tag}")

def list_grouping_tag(
    tags: list[str]
) -> None:
    """Display all grouping tags in a numbered list."""
    clear_screen()
    print("🏷️ Listing all grouping tags 🏷️")
    if not tags:
        print("No grouping tags found.")
    else:
        tag_list(tags, False)
    input("➖ Press Enter to return to the menu...")

def add_grouping_tag(
    tags: list[str],
    group_file: Path = GROUP_FILE
) -> None:
    """Add a new grouping tag to the group file if it doesn't already exist."""
    aux_list = tags
    clear_screen()
    print("🏷️ Create a new grouping tag 🏷️")

    tag_list(tags)

    new_tag = prompt("➖ Enter new grouping tag to add (or 'q' to quit):", return_key='q', delay=True)
    if new_tag is not None:
        if new_tag in aux_list:
            print("➖ ⚠️ Grouping tag already exists. Please try again.")
            time.sleep(2)
            add_grouping_tag(aux_list, group_file)
        else:
            group_file.write_text(group_file.read_text(encoding='utf-8') + f"{new_tag}\n")
                
            print(f"➖ ✅ Added new grouping tag: {new_tag}")
            aux_list.append(new_tag)

            again = prompt('➕ Add another tag? (y/n):')
            if again is not None:
                add_grouping_tag(aux_list, group_file)

def delete_grouping_tag(
    tags: list[str],
    group_file: Path = GROUP_FILE
) -> None:
    """Delete a grouping tag from the group file if it exists."""
    aux_list = tags
    clear_screen()
    print("🏷️ Delete a grouping tag 🏷️")
    if not aux_list:
        print("➖ ⚠️ No grouping tags found to delete.")
        time.sleep(2)
        return
    
    tag_list(aux_list)

    choice = prompt("➖ Enter the number of the tag to delete (or 'q' to quit):", return_key='q', delay=True)
    if choice is not None and choice != 'q':
        if not choice.isdigit() or not (1 <= int(choice) <= len(aux_list)):
            print("➖ ❌ Invalid selection. Please try again.")
            time.sleep(2)
            delete_grouping_tag(aux_list, group_file)
            return
        else: 
            idx = int(choice) - 1
            choosed_tag = aux_list[idx]

            confirm = prompt(f"➖ Are you sure you want to delete '{choosed_tag}'? (y/n):", "➖ ❌ Deletion cancelled.", delay=True)
            if confirm is not None:
                aux_list.pop(idx)
                try:
                    group_file.write_text('\n'.join(aux_list) + '\n')
                    print(f"➖ ✅ Deleted grouping tag: {choosed_tag}")
                except Exception as e:
                    print(f"➖ ❌ Error deleting tag: {e}")
                
                again = prompt('➖ Delete another tag? (y/n):')
                if again is not None:
                    delete_grouping_tag(aux_list, group_file)

def edit_grouping_tag(
    tags: list[str],
    group_file: Path = GROUP_FILE
) -> None:
    """Edit an existing grouping tag in the group file."""
    aux_list = tags
    clear_screen()
    print("🏷️ Edit a grouping tag 🏷️")
    if not aux_list:
        print("➖ ⚠️ No grouping tags found to edit.")
        time.sleep(2)
        return
    
    tag_list(aux_list)

    choice = prompt("➖ Enter the number of the tag to edit (or 'q' to quit):", return_key='q', delay=True)
    if choice is not None and choice != 'q':
        if not choice.isdigit() or not (1 <= int(choice) <= len(aux_list)):
            print("➖ ❌ Invalid selection. Please try again.")
            time.sleep(2)
            edit_grouping_tag(aux_list, group_file)
            return
        
        idx = int(choice) - 1
        choosed_tag = aux_list[idx]
        new_tag = prompt(f"➖ Enter new name for '{choosed_tag}':")

        if new_tag is not None:
            aux_list[idx] = new_tag
            try:
                group_file.write_text('\n'.join(aux_list) + '\n')
                print(f"➖ ✅ Updated grouping tag: {choosed_tag} -> {new_tag}")
            except Exception as e:
                print(f"➖ ❌ Error updating tag: {e}")
                time.sleep(2)

            again = prompt('➖ Edit another tag? (y/n):')
            if again is not None:
                edit_grouping_tag(aux_list, group_file)

def choose_grouping_tag() -> str | None:
    """Prompt the user to choose a grouping tag from the list of available tags. Returns the chosen tag or None if no tag is selected."""
    print("🏷️ Choose a grouping tag for this card:")
    tags = load_grouping_tags()
    tag = ''

    if not tags:
        print("➖ ⚠️ No grouping tags available.")
        return None
    tag_list(tags)
    print("0. No grouping tag")

    choice = prompt("➖ Enter the number of your choice (or '0' for no tag):", "➖ ✅ No tag selected.", return_key='0')
    if choice is None or choice == '0':
        return None
    if choice.isdigit():
        choice_num = int(choice)
        if 1 <= choice_num <= len(tags):
            tag = tags[choice_num - 1]
    return tag
