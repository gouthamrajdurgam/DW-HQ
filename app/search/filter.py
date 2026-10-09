from __future__ import annotations

import json
from typing import Any, Dict, List

from app.config import get_preferences
from app.db import get_connection
from app.feedback.feedback_store import add_feedback
from app.models.feature_builder import build_feature_vector, feature_columns
from app.models.ranking_model import HybridRanker
from app.models.trainer import train_model_from_feedback
from app.notifications.emailer import send_shortlist_email
from app.scrapers.immoscout import ImmoScoutScraper
from app.scrapers.kleinanzeigen import KleinanzeigenScraper
from app.scrapers.normalize import normalize_batch
from app.search.expand import expand_search_params
from app.search.filter import filter_listings
from app.utils import unique_by_url


def build_search_queries(prefs: Dict[str, Any]) -> List[Dict[str, str]]:
    city = prefs.get("city", "Berlin")
    city_slug = city.lower().replace(" ", "-")
    max_price = int(prefs.get("max_price", 2200))
    radius = int(prefs.get("max_radius_km", 8))
    base_queries = [
        {
            "source": "immoscout",
            "url": f"https://www.immoscout24.de/Suche/S-2/Wohnung-Miete/{city_slug}?price={max_price}&r={radius}&enteredFrom=result_list",
        },
        {
            "source": "kleinanzeigen",
            "url": f"https://www.kleinanzeigen.de/s-wohnung-mieten/{city_slug}?price=0-{max_price}&radius={radius}",
        },
    ]

    expanded = expand_search_params(prefs, 0)
    expanded_price = int(expanded.get("max_price", max_price))
    expanded_radius = int(expanded.get("max_radius_km", radius))
    base_queries.append({
        "source": "immoscout",
        "url": f"https://www.immoscout24.de/Suche/S-2/Wohnung-Miete/{city_slug}?price={expanded_price}&r={expanded_radius}&enteredFrom=result_list",
    })
    base_queries.append({
        "source": "kleinanzeigen",
        "url": f"https://www.kleinanzeigen.de/s-wohnung-mieten/{city_slug}?price=0-{expanded_price}&radius={expanded_radius}",
    })
    return base_queries


def store_listings(listings: List[Dict[str, Any]]) -> None:
    conn = get_connection()
    for item in listings:
        conn.execute(
            """
            INSERT OR REPLACE INTO listings (
                id, source, title, price, location, district, property_type,
                size_m2, beds, url, created_at, raw
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
            """,
            (
                item["id"],
                item["source"],
                item["title"],
                item["price"],
                item["location"],
                item["district"],
                item["property_type"],
                item["size_m2"],
                item["beds"],
                item["url"],
                json.dumps(item),
            ),
        )
    conn.commit()
    conn.close()


def collect_search_results(prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_listings: List[Dict[str, Any]] = []
    seen_urls = set()

    for search in build_search_queries(prefs):
        try:
            source = search["source"]
            url = search["url"]
            scraper = ImmoScoutScraper(prefs) if source == "immoscout" else KleinanzeigenScraper(prefs)
            for item in scraper.collect(url):
                url_value = item.get("url")
                if not url_value or url_value in seen_urls:
                    continue
                seen_urls.add(url_value)
                raw_listings.append(item)
        except Exception as exc:
            print(f"Error collecting from {search['source']}: {exc}")

    return normalize_batch(raw_listings)


def build_shortlist() -> List[Dict[str, Any]]:
    prefs = get_preferences().__dict__
    listings = collect_search_results(prefs)
    listings = unique_by_url(listings)
    filtered = filter_listings(listings, prefs)

    if not filtered:
        expanded = expand_search_params(prefs, 0)
        filtered = filter_listings(listings, expanded)

    model = HybridRanker()
    trained_model = train_model_from_feedback()
    if hasattr(trained_model, "coef_"):
        model.model = trained_model
        model.is_trained = True

    ranked = model.rank(filtered, prefs)
    return ranked[: int(prefs.get("top_n", 3))]


def send_daily_email(top_listings: List[Dict[str, Any]], prefs: Dict[str, Any]) -> None:
    if not top_listings:
        print("No listings shortlisted.")
        return

    body_lines = ["Top 3 property shortlist:"]
    for idx, item in enumerate(top_listings, start=1):
        body_lines.append(
            f"{idx}. {item.get('title')} | {item.get('price')} EUR | {item.get('location')} | {item.get('url')}"
        )
    body = "\n".join(body_lines)

    send_shortlist_email(
        subject="Daily property shortlist",
        body=body,
        to_email=prefs.get("email_to", ""),
        from_email=prefs.get("email_from", ""),
        smtp_host=prefs.get("smtp_host", ""),
        smtp_user=prefs.get("smtp_user", ""),
        smtp_password=prefs.get("smtp_password", ""),
        smtp_port=int(prefs.get("smtp_port", 587)),
    )


if __name__ == "__main__":
    preferences = get_preferences().__dict__
    shortlist = build_shortlist()
    send_daily_email(shortlist, preferences)
    print(f"Found {len(shortlist)} shortlisted properties.")
    for item in shortlist:
        print(item.get("title"), item.get("price"), item.get("url"))
