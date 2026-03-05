from config import TYPES_FILE

def load_types() -> list[str]:
    """Load card types from the types file. Returns a list of types."""
    if not TYPES_FILE.exists():
        return []
    content = TYPES_FILE.read_text(encoding='utf-8')
    return [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
