from dataclasses import dataclass, field
from typing import List, Dict, Any

from app import load_preferences


@dataclass
class Preferences:
    city: str = "Berlin"
    target_districts: List[str] = field(default_factory=lambda: ["Prenzlauer Berg", "Friedrichshain"])
    property_types: List[str] = field(default_factory=lambda: ["apartment", "house"])
    max_price: float = 2200
    min_size_m2: float = 55
    max_radius_km: int = 8
    preferred_beds: int = 2
    preferred_states: List[str] = field(default_factory=lambda: ["Berlin", "Berlin-Mitte"])
    top_n: int = 3
    email_to: str = ""
    email_from: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    @classmethod
    def from_file(cls) -> "Preferences":
        raw = load_preferences()
        data = cls()
        for key, value in raw.items():
            if hasattr(data, key):
                setattr(data, key, value)
        return data


def get_preferences() -> Preferences:
    return Preferences.from_file()
