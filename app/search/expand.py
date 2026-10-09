from typing import Any, Dict, List


def normalize_listing(raw: Dict[str, Any]) -> Dict[str, Any]:
    listing = {
        "id": f"{raw.get('source')}::{raw.get('url') or raw.get('title')}",
        "source": raw.get("source", "unknown"),
        "title": raw.get("title", "Property"),
        "price": float(raw.get("price") or 0),
        "location": raw.get("location", ""),
        "district": raw.get("district", ""),
        "property_type": raw.get("property_type", "apartment"),
        "size_m2": float(raw.get("size_m2") or 0),
        "beds": int(raw.get("beds") or 0),
        "url": raw.get("url", ""),
    }
    return listing


def normalize_batch(raw_listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_listing(item) for item in raw_listings]
