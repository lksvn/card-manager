import os, time
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt(prompt_text, message="↩️ Returning to menu.", return_key='n', delay=False):
    user_input = input(f"{prompt_text} ").strip()
    if user_input.lower() == return_key or user_input == '':
        print(message)
        if delay: time.sleep(2)
        return None
    return user_input

def manage_list(file_path: Path, title: str) -> None:
    """View and manage a list file. Allows editing the file in an external editor."""
    while True:
        view_list(file_path, title)
        print("\n⚙️ Options:")
        print("1. Edit file (opens in external editor)")
        print("q. Back")
        choice = input("➖ ").strip().lower()
        if choice == '1':
            edit_file(file_path)
        elif choice in ['q', '']:
            break

def view_list(file_path, title):
    clear_screen()
    print(f"📄 {title} 📄")
    if not os.path.exists(file_path):
        print("➖ ❌ File not found.")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        print("➖ ℹ️ File is empty.")
    else:
        for idx, line in enumerate(lines, 1):
            print(f"{idx}. {line}")

def edit_file(file_path):
    if not os.path.exists(file_path):
        print(f"➖ ❌ File {file_path} not found.")
        return
    
    print(f"🔧 Opening {file_path} in your default editor...")
    try:
        os.startfile(file_path)
    except Exception as e:
        print(f"➖ ❌ Could not open file: {e}")

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options  # Dict of {key: (label, action)}

    def display(self):
        clear_screen()
        print(f"🕹️ {self.title} 🕹️")
        print("⚙️ Options:")
        for key, (label, _) in self.options.items():
            print(f"{key}. {label}")
        print("q. Back/Quit")
        return input("➖ ").strip().lower()

    def run(self):
        while True:
            choice = self.display()
            if choice in ['q', 'quit', 'exit', '']:
                break
            
            option = self.options.get(choice)
            if option:
                label, action = option

                # if it's a menu, run it
                if isinstance(action, Menu):
                    action.run()
                # if it's a function (lambda or regular), call it
                elif callable(action):
                    result = action()
                    # if the function returns a Menu, run it (w/o the prompt to return)
                    if isinstance(result, Menu):
                        result.run()
                    # else:
                    #     input("\n➖ Press Enter to return...")
            else:
                print("❌ Invalid choice, please try again.")
                time.sleep(1)
