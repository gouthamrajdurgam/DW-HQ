from __future__ import annotations

from typing import Any, Dict, List

from app.feedback.feedback_store import add_feedback
from app.models.feature_builder import build_feature_vector


def review_shortlist(shortlist: List[Dict[str, Any]], prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not shortlist:
        print("No shortlist available to review.")
        return []

    reviewed = []
    for index, item in enumerate(shortlist, start=1):
        print(f"\n[{index}/{len(shortlist)}]")
        print(f"Title: {item.get('title')}")
        print(f"Price: {item.get('price')} EUR")
        print(f"Location: {item.get('location')}")
        print(f"URL: {item.get('url')}")
        choice = input("Like? [y]es / [n]o / [s]kip: ").strip().lower()

        if choice in {"y", "yes"}:
            features = build_feature_vector(item, prefs)
            add_feedback(item.get("id"), 1, features)
            item["liked"] = True
            reviewed.append(item)
        elif choice in {"n", "no"}:
            features = build_feature_vector(item, prefs)
            add_feedback(item.get("id"), 0, features)
            item["liked"] = False
        else:
            reviewed.append(item)

    return reviewed
