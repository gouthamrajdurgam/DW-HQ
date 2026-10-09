from typing import Dict, List


def filter_listings(listings: List[Dict[str, object]], prefs: Dict[str, object]) -> List[Dict[str, object]]:
    filtered = []
    for listing in listings:
        if not listing.get("url"):
            continue
        if float(listing.get("price") or 0) > float(prefs.get("max_price", 999999)):
            continue
        if float(listing.get("size_m2") or 0) < float(prefs.get("min_size_m2", 0)):
            continue
        listing_type = str(listing.get("property_type") or "").lower()
        allowed_types = {str(pt).lower() for pt in prefs.get("property_types", [])}
        if listing_type not in allowed_types:
            continue
        filtered.append(listing)
    return filtered
