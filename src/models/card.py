from dataclasses import dataclass
from typing import Optional

@dataclass
class Card:
    name: str
    type: str
    number: int
    image_url: str
    set_name: str
    set_code: str

    flavor_name: Optional[str] = None
    
    @property
    def formatted_collection(self) -> str:
        return f"{self.set_name} ({self.set_code.upper()})"