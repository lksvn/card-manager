import unicodedata
import re

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
