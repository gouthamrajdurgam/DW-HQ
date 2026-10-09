from __future__ import annotations

import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from app.scrapers.base import BaseScraper


class ImmoScoutScraper(BaseScraper):
    source_name = "immoscout"

    def collect(self, query: str) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 2200})
            page.goto(query, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
        selectors = [
            "article[data-id]",
            ".result-list-entry",
            ".result-item",
            "div[data-obid]",
            "article.result-list-entry",
        ]

        for selector in selectors:
            cards = soup.select(selector)
            if not cards:
                continue
            for article in cards:
                try:
                    title_el = article.select_one("h2, h3, .title, .result-item__title, .listing-title")
                    title = title_el.get_text(" ", strip=True) if title_el else "Property"

                    price_el = article.select_one(".price, .amount, .result-item__price, .rent")
                    price = self._extract_price(price_el.get_text(" ", strip=True) if price_el else "")

                    location_el = article.select_one(".address, .location, .result-item__address, .address-block")
                    location = location_el.get_text(" ", strip=True) if location_el else ""

                    size_el = article.select_one(".size, .living-space, .livingSpace, .result-item__details")
                    size_text = size_el.get_text(" ", strip=True) if size_el else ""
                    size_m2 = self._extract_size(size_text)

                    beds_el = article.select_one(".rooms, .number-of-rooms, .result-item__details")
                    beds_text = beds_el.get_text(" ", strip=True) if beds_el else ""
                    beds = self._extract_beds(beds_text)

                    link_el = article.select_one("a[href]")
                    url = link_el.get("href") if link_el else ""
                    if url and not url.startswith("http"):
                        url = "https://www.immoscout24.de" + url

                    if not url:
                        continue

                    results.append({
                        "source": "immoscout",
                        "title": title,
                        "price": price,
                        "location": location,
                        "district": self._district_from_location(location),
                        "property_type": self._property_type_from_title(title),
                        "size_m2": size_m2,
                        "beds": beds,
                        "url": url,
                    })
                except Exception:
                    continue

        return results

    def _extract_price(self, text: str) -> float:
        if not text:
            return 0.0
        match = re.search(r"(\d+(?:[\.,]\d{1,2})?)", text.replace(".", "").replace(" ", ""))
        if not match:
            return 0.0
        return float(match.group(1).replace(",", "."))

    def _extract_size(self, text: str) -> float:
        if not text:
            return 0.0
        match = re.search(r"(\d+(?:[\.,]\d{1,2})?)\s*(?:m²|m2|qm)", text.lower())
        if not match:
            return 0.0
        return float(match.group(1).replace(",", "."))

    def _extract_beds(self, text: str) -> int:
        if not text:
            return 0
        match = re.search(r"(\d+)\s*(?:Zimmer|rooms)", text.lower())
        if match:
            return int(match.group(1))
        match = re.search(r"(\d+)", text)
        if match:
            return int(match.group(1))
        return 0

    def _property_type_from_title(self, title: str) -> str:
        title = title.lower()
        if "haus" in title or "house" in title:
            return "house"
        return "apartment"

    def _district_from_location(self, location: str) -> str:
        parts = [p.strip() for p in location.split(",")]
        return parts[0] if parts else ""
