from typing import Any, Dict, List


def filter_listings(listings: List[Dict[str, Any]], prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
    filtered = []
    for listing in listings:
        if not listing.get("url"):
            continue
        if float(listing.get("price") or 0) > float(prefs.get("max_price", 999999)):
            continue
        if float(listing.get("size_m2") or 0) < float(prefs.get("min_size_m2", 0)):
            continue
        if listing.get("property_type") not in {pt.lower() for pt in prefs.get("property_types", [])}:
            continue
        filtered.append(listing)
    return filtered
