from typing import Any, Dict, List


def build_feature_vector(listing: Dict[str, Any], prefs: Dict[str, Any]) -> Dict[str, Any]:
    price = float(listing.get("price") or 0)
    size = float(listing.get("size_m2") or 0)
    district = (listing.get("district") or "").lower()
    location = (listing.get("location") or "").lower()
    prop_type = (listing.get("property_type") or "").lower()

    features = {
        "price": price,
        "size_m2": size,
        "price_per_m2": price / size if size else 0,
        "beds": int(listing.get("beds") or 0),
        "district_match": 1.0 if any(d.lower() in district or d.lower() in location for d in prefs.get("target_districts", [])) else 0.0,
        "in_preferred_state": 1.0 if any(state.lower() in district or state.lower() in location for state in prefs.get("preferred_states", [])) else 0.0,
        "property_type_match": 1.0 if prop_type in {t.lower() for t in prefs.get("property_types", [])} else 0.0,
        "within_budget": 1.0 if price <= float(prefs.get("max_price", 999999)) else 0.0,
        "size_ok": 1.0 if size >= float(prefs.get("min_size_m2", 0)) else 0.0,
        "beds_ok": 1.0 if int(listing.get("beds") or 0) >= int(prefs.get("preferred_beds", 1)) else 0.0,
    }
    return features


def feature_columns() -> List[str]:
    return [
        "price",
        "size_m2",
        "price_per_m2",
        "beds",
        "district_match",
        "in_preferred_state",
        "property_type_match",
        "within_budget",
        "size_ok",
        "beds_ok",
    ]
