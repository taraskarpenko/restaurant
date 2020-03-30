from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Restaurant:
    id: str
    name: str
    country: str
    zip_code: str
    city: str
    address_line_1: str
    latitude: str
    longitude: str
    service_type: Optional[str] = None
    cuisine: Optional[str] = None
    web_address: Optional[str] = None
    tags: Optional[List[str]] = None
