import webbrowser
import requests
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

geolocator = Nominatim(user_agent="geo_utils")


def get_current_location():
    """Get current location via IP"""
    g = geocoder.ip("me")
    if not g.ok or not g.latlng:
        raise RuntimeError("Unable to determine current location")

    return {
        "latlng": tuple(g.latlng),
        "city": g.city or "",
        "state": g.state or "",
        "country": g.country or ""
    }


def geocode_place(place: str):
    """Geocode a place name into coordinates and address info"""
    location = geolocator.geocode(place, addressdetails=True)
    if not location:
        raise ValueError(f"Could not geocode location: {place}")

    address = location.raw.get("address", {})

    return {
        "latlng": (location.latitude, location.longitude),
        "city": address.get("city", ""),
        "state": address.get("state", ""),
        "country": address.get("country", "")
    }


def distance_between(latlng1, latlng2) -> float:
    """Return distance in kilometers (rounded)"""
    return round(great_circle(latlng1, latlng2).kilometers, 2)


def locate(place: str, open_map: bool = True):
    """
    Locate a place, calculate distance from current IP location,
    and optionally open Google Maps.
    """
    if open_map:
        webbrowser.open(f"https://www.google.com/maps/place/{place}")

    current = get_current_location()
    target = geocode_place(place)

    distance_km = distance_between(current["latlng"], target["latlng"])

    return {
        "current_location": current,
        "target_location": target,
        "distance_km": distance_km
    }
