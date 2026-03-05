from pathlib import Path

# Set this to the root of your Obsidian vault
# If empty, it assumes the current directory is the root
# r"" is used to handle Windows paths without needing to escape backslashes 
FOLDER = Path(r'My Vault path')

# Path where your card Markdown files will be created
CARDS_DIR = FOLDER

# Paths for data files
TYPES_FILE = FOLDER / 'any-subfolder' / 'types.md'
COLLECTIONS_FILE = FOLDER / 'any-subfolder' / 'collections.md'
GROUP_FILE = FOLDER / 'any-subfolder' / 'groups.md'

# Path for card images
IMAGES_DIR = FOLDER / 'Images'

# Custom type overrides for normalization
# Maps Scryfall types to your preferred names
CUSTOM_TYPE_OVERRIDES = {
    'boss': 'Token',
    'event': 'Token',
}