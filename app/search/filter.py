from copy import deepcopy
from typing import Any, Dict


def expand_search_params(params: Dict[str, Any], results_count: int) -> Dict[str, Any]:
    expanded = deepcopy(params)
    if results_count > 0:
        return expanded

    expanded["max_price"] = float(params.get("max_price", 2200)) * 1.15
    expanded["max_radius_km"] = min(int(params.get("max_radius_km", 8)) + 2, 15)
    expanded["property_types"] = params.get("property_types", ["apartment"])
    expanded["preferred_beds"] = max(int(params.get("preferred_beds", 2)) - 1, 1)
    return expanded
