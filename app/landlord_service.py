from __future__ import annotations

from dataclasses import dataclass, asdict

from app.paths import LANDLORD_FILE
from app.storage import read_json, write_json


@dataclass
class LandlordDetails:
    landlord_name: str = ""
    landlord_director: str = ""
    landlord_basis: str = ""
    landlord_address: str = ""
    landlord_details: str = ""


def load_landlord_details() -> LandlordDetails:
    payload = read_json(LANDLORD_FILE, default=asdict(LandlordDetails()))
    return LandlordDetails(**payload)


def save_landlord_details(details: LandlordDetails) -> None:
    write_json(LANDLORD_FILE, asdict(details))
