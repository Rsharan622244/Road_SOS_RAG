"""
offline_cache.py - SQLite cache for last-known nearby services

When Google Places API is unavailable (no network), we serve
the last cached results for the user's area.
"""

import sqlite3
import json
import time
from math import radians, sin, cos, sqrt, atan2

DB_PATH = "roadsos.db"
CACHE_EXPIRY_HOURS = 48  # cached results valid for 48 hours


def init_db():
    """Create tables if they don't exist. Called once on startup."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS service_cache (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lat         REAL NOT NULL,
            lng         REAL NOT NULL,
            service_type TEXT NOT NULL,
            data        TEXT NOT NULL,
            saved_at    REAL NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_location ON service_cache(lat, lng)")
    conn.commit()
    conn.close()


def save_to_cache(lat: float, lng: float, services: dict):
    """Save a full services response to SQLite."""
    conn = sqlite3.connect(DB_PATH)
    now = time.time()
    for service_type, places in services.items():
        conn.execute("""
            INSERT INTO service_cache (lat, lng, service_type, data, saved_at)
            VALUES (?, ?, ?, ?, ?)
        """, (lat, lng, service_type, json.dumps(places), now))
    conn.commit()
    conn.close()


def get_from_cache(lat: float, lng: float, service_types: list, radius_km: float = 20) -> dict:
    """
    Returns cached services within radius_km of the given location.
    Only returns results saved within CACHE_EXPIRY_HOURS.
    """
    conn = sqlite3.connect(DB_PATH)
    expiry_time = time.time() - (CACHE_EXPIRY_HOURS * 3600)

    results = {}
    for service_type in service_types:
        rows = conn.execute("""
            SELECT lat, lng, data FROM service_cache
            WHERE service_type = ? AND saved_at > ?
            ORDER BY saved_at DESC
            LIMIT 50
        """, (service_type, expiry_time)).fetchall()

        best = []
        for row_lat, row_lng, data_json in rows:
            dist = haversine(lat, lng, row_lat, row_lng)
            if dist <= radius_km:
                places = json.loads(data_json)
                best.extend(places)

        if best:
            # Deduplicate by name, sort by distance
            seen = set()
            unique = []
            for p in best:
                if p["name"] not in seen:
                    seen.add(p["name"])
                    unique.append(p)
            unique.sort(key=lambda x: x.get("distance_km", 99))
            results[service_type] = unique[:3]

    conn.close()
    return results


def haversine(lat1, lng1, lat2, lng2) -> float:
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))


# Initialize DB when module is imported
init_db()