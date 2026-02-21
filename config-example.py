import os

# Set this to the root of your Obsidian vault
# If empty, it assumes the current directory is the root
FOLDER = r'C:\Path\To\Your\Vault'

# Paths for data files (typically inside the Scripts folder)
TYPES_FILE = os.path.join(FOLDER, 'Scripts', 'types.md')
COLLECTIONS_FILE = os.path.join(FOLDER, 'Scripts', 'collections.md')
GROUP_FILE = os.path.join(FOLDER, 'Scripts', 'groups.md')

# Path where your card Markdown files will be created
CARDS_DIR = FOLDER

# Path for card images
IMAGES_DIR = os.path.join(FOLDER, 'Images')

# Custom type overrides for normalization
# Maps Scryfall types to your preferred names
CUSTOM_TYPE_OVERRIDES = {
    'boss': 'Token',
    'event': 'Token',
}