import unicodedata
import re
from pathlib import Path

def normalize_type(card_type, valid_types, custom_type=None):
    if custom_type and card_type.lower() in custom_type:
        card_type = custom_type[card_type.lower()]

    types_found = []
    for valid_type in valid_types:
        if valid_type.lower() in card_type.lower():
            types_found.append(valid_type)
    return ', '.join(types_found) if types_found else card_type

def normalize_card_name(name):
    normalized = unicodedata.normalize('NFKD', name)
    normalized = normalized.encode('ascii', 'ignore').decode('ascii')
    normalized = normalized.lower()
    normalized = re.sub(r'[^a-z0-9]+', '-', normalized)
    normalized = normalized.strip('-')
    return normalized

def sanitize_filename(name: str) -> str:
    """
    Receives only strings, returns (-> str) sanitized string for filenames
    """
    # Replace anything NOT a letter, number, space or dash with empty
    clean = re.sub(r'[^\w\s-]', '', name).strip() 
    # Replace multiple spaces with a single space
    clean = re.sub(r'\s+', ' ',clean)
    return clean

def get_image_filename(card_name: str, extension: str = ".png") -> str:
    """
    Receives a card name and returns a sanitized filename with extension (default png)
    """
    clean_name = sanitize_filename(card_name)
    return str(Path(clean_name).with_suffix(extension).name)