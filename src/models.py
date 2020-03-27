from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Address:
    country: str
    zip_code: str
    city: str
    address_line_1: str


@dataclass
class Location:
    latitude: str
    longitude: str


@dataclass
class Restaurant:
    id: str
    name: str
    address: Optional[Address] = None
    location: Optional[Location] = None
    service_type: Optional[str] = None
    cuisine: Optional[str] = None
    web_address: Optional[str] = None
    tags: Optional[Tuple[str]] = None
