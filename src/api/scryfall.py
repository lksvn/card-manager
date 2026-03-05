import re
import requests
from config import IMAGES_DIR
from src.models.card import Card

def extract_card_id_from_url(url: str) -> tuple[str | None, str | None]:
    """Extracts the set code and collector number from a Scryfall card URL. Returns (set_code, collector_number) or (None, None) if the URL is invalid."""
    match = re.search(r'/card/([^/]+)/([^/]+)', url)
    if match:
        set_code = match.group(1)
        collector_number = match.group(2)
        return set_code, collector_number
    return None, None

def get_card_data(url: str) -> Card | None:
    """Fetches the card data using the Scryfall API."""
    set_code, collector_number = extract_card_id_from_url(url)
    
    if not set_code or not collector_number:
        print("❌ Error: Invalid Scryfall URL. Please check the link and try again.")
        return None
    
    api_url = f"https://api.scryfall.com/cards/{set_code}/{collector_number}"
    
    try:
        response = requests.get(api_url, timeout=10)    
        response.raise_for_status()
        data = response.json()

        return Card(
            name=data.get('name', 'Unknown Card'),
            flavor_name=data.get('flavor_name', ''),
            type=data.get('type_line', 'Unknown'),
            number=int(data.get('collector_number', 0)),
            image_url=data.get('image_uris', {}).get('png') or data.get('image_uris', {}).get('large'),
            set_name=data.get('set_name', 'Unknown Set'),
            set_code=data.get('set', 'N/A').upper()
        )
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: No internet connection or Scryfall is unreachable.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Error: Card not found. Please check the URL and try again.")
        else:
            print(f"❌ Scryfall error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.Timeout:
        print("❌ Error: Request to Scryfall timed out. Please try again later.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

def download_image(
    image_url: str,
    filename: str
) -> str | None:
    """Downloads the image from the given URL and saves it to the images directory. Returns the filename if successful, or None if there was an error."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = IMAGES_DIR / filename

    if filepath.exists():
        print(f"⚠️ Image already exists: {filename}. Skipping download.")
        return filename
    
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()

        filepath.write_bytes(response.content)
        return filename
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download image: {e}")
        return None
    
