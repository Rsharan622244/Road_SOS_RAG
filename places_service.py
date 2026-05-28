import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

SERVICE_CONFIG = {
    "hospital":          {"type": "hospital",           "keyword": "hospital emergency", "icon": "🏥", "label": "Hospital"},
    "ambulance_service": {"type": "ambulance_service",  "keyword": "ambulance service",  "icon": "🚑", "label": "Ambulance"},
    "police":            {"type": "police",              "keyword": "police station",     "icon": "🚔", "label": "Police Station"},
    "towing_service":    {"type": "car_repair",          "keyword": "towing service",     "icon": "🚛", "label": "Towing Service"},
    "car_repair":        {"type": "car_repair",          "keyword": "car repair garage",  "icon": "🔧", "label": "Car Repair"},
    "tire_shop":         {"type": "car_repair",          "keyword": "tyre puncture shop", "icon": "🔩", "label": "Tyre Shop"},
}

SEARCH_RADIUS_METERS = 5000


def find_nearby(lat: float, lng: float, service_type: str, max_results: int = 3) -> list:
    if service_type not in SERVICE_CONFIG:
        return []

    config = SERVICE_CONFIG[service_type]

    # New Places API v1 uses POST with JSON body
    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.internationalPhoneNumber,places.id,places.regularOpeningHours,places.rating"
    }

    body = {
        "includedTypes": [config["type"]],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": float(SEARCH_RADIUS_METERS)
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=8)
        data = response.json()

        if response.status_code != 200:
            print(f"[Places] API error {response.status_code}: {data.get('error', {}).get('message', data)}")
            # Fallback: try text search with keyword
            return find_nearby_text_search(lat, lng, service_type, max_results)

        places = data.get("places", [])

        if not places:
            print(f"[Places] No results for {service_type}, trying text search fallback")
            return find_nearby_text_search(lat, lng, service_type, max_results)

        results = []
        for place in places:
            place_lat = place.get("location", {}).get("latitude", lat)
            place_lng = place.get("location", {}).get("longitude", lng)
            distance_km = haversine(lat, lng, place_lat, place_lng)

            phone = (place.get("nationalPhoneNumber")
                     or place.get("internationalPhoneNumber")
                     or "Not available")

            open_now = None
            opening = place.get("regularOpeningHours", {})
            if opening:
                open_now = opening.get("openNow")

            results.append({
                "name":        place.get("displayName", {}).get("text", "Unknown"),
                "address":     place.get("formattedAddress", "Address not available"),
                "phone":       phone,
                "distance_km": round(distance_km, 1),
                "open_now":    open_now,
                "rating":      place.get("rating"),
                "place_id":    place.get("id", ""),
                "lat":         place_lat,
                "lng":         place_lng,
                "icon":        config["icon"],
                "label":       config["label"],
                "type":        service_type,
            })

        results.sort(key=lambda x: x["distance_km"])
        print(f"[Places] {service_type}: found {len(results)} results")
        return results

    except requests.exceptions.Timeout:
        print(f"[Places] Timeout for {service_type}")
        return []
    except Exception as e:
        print(f"[Places] Exception for {service_type}: {e}")
        return []


def find_nearby_text_search(lat: float, lng: float, service_type: str, max_results: int = 3) -> list:
    """
    Fallback using Places v1 Text Search API.
    Used when Nearby Search returns no results for a type.
    """
    config = SERVICE_CONFIG.get(service_type, {})
    keyword = config.get("keyword", service_type)

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.internationalPhoneNumber,places.id,places.rating"
    }

    body = {
        "textQuery": keyword,
        "maxResultCount": max_results,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": float(SEARCH_RADIUS_METERS)
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=8)
        data = response.json()

        if response.status_code != 200:
            print(f"[Places TextSearch] Error: {data.get('error', {}).get('message', '')}")
            return []

        places = data.get("places", [])
        results = []

        for place in places:
            place_lat = place.get("location", {}).get("latitude", lat)
            place_lng = place.get("location", {}).get("longitude", lng)
            distance_km = haversine(lat, lng, place_lat, place_lng)

            phone = (place.get("nationalPhoneNumber")
                     or place.get("internationalPhoneNumber")
                     or "Not available")

            results.append({
                "name":        place.get("displayName", {}).get("text", "Unknown"),
                "address":     place.get("formattedAddress", "Address not available"),
                "phone":       phone,
                "distance_km": round(distance_km, 1),
                "open_now":    None,
                "rating":      place.get("rating"),
                "place_id":    place.get("id", ""),
                "lat":         place_lat,
                "lng":         place_lng,
                "icon":        config.get("icon", "📍"),
                "label":       config.get("label", service_type),
                "type":        service_type,
            })

        results.sort(key=lambda x: x["distance_km"])
        print(f"[Places TextSearch] {service_type}: found {len(results)} results")
        return results

    except Exception as e:
        print(f"[Places TextSearch] Exception: {e}")
        return []


def get_all_nearby(lat: float, lng: float, service_types: list) -> dict:
    all_results = {}
    for service_type in service_types:
        places = find_nearby(lat, lng, service_type)
        if places:
            all_results[service_type] = places
    return all_results


def haversine(lat1, lng1, lat2, lng2) -> float:
    from math import radians, sin, cos, sqrt, atan2
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))