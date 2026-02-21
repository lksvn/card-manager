import requests
import re
import os

from config import IMAGES_DIR

def extract_card_id_from_url(url):
    match = re.search(r'/card/([^/]+)/([^/]+)', url)
    if match:
        set_code = match.group(1)
        collector_number = match.group(2)
        return set_code, collector_number
    return None, None

def get_card_data(url):
    set_code, collector_number = extract_card_id_from_url(url)
    
    if not set_code or not collector_number:
        raise ValueError("Could not parse Scryfall URL")
    
    api_url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
    
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    collection_name = f"{data.get('set_name', 'Unknown Set')} ({data.get('set', 'N/A').upper()})"

    return {
        'name': data.get('name', 'Unknown Card'),
        'flavor_name': data.get('flavor_name', ''),
        'type': data.get('type_line', 'Unknown'),
        'number': data.get('collector_number', 'N/A'),
        'image_url': data.get('image_uris', {}).get('png') or data.get('image_uris', {}).get('large'),
        'set_name': data.get('set_name', 'Unknown Set'),
        'set_code': data.get('set', 'N/A').upper(),
        'formatted_collection': collection_name
    }

def download_image(image_url, filename):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    response = requests.get(image_url)
    response.raise_for_status()

    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath):
        print(f"➖ ⚠️ Image already exists: {filename}, skipping download.")
        return filename
    
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filename
