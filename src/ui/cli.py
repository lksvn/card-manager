import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt(prompt_text, message="↩️ Returning to menu.", return_key='n', delay=False):
    user_input = input(f"{prompt_text} ").strip()
    if user_input.lower() == return_key or user_input == '':
        print(message)
        if delay: time.sleep(2)
        return None
    return user_input
