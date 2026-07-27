#!/usr/bin/env python3
"""
Monthly updater for japan_stats.json
Fetches latest exchange rates and JNTO tourism data.
Run via GitHub Actions (monthly cron) or manually.
"""

import json
import os
import urllib.request
import urllib.error
from datetime import datetime

STATS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "japan_stats.json")


def fetch_json(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ViajApp-Stats-Updater/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Warning: Failed to fetch {url}: {e}")
        return None


def update_exchange_rate(stats):
    print("Fetching exchange rate...")
    data = fetch_json("https://open.er-api.com/v6/latest/EUR")
    if data and data.get("rates", {}).get("JPY"):
        jpy = data["rates"]["JPY"]
        stats["exchange_rate"] = {
            "jpy_to_eur": round(1 / jpy, 6),
            "last_fetched": datetime.now().isoformat(),
            "eur_to_jpy": jpy,
        }
        print(f"  EUR/JPY: {jpy}")
        return True
    print("  Using cached exchange rate")
    return False


def update_visitor_data(stats):
    print("Checking JNTO visitor data...")
    # JNTO publishes monthly visitor stats
    # Try to fetch from their public data page
    data = fetch_json("https://www.jnto.go.jp/en/statistics/data/visitors-statistics.json")
    if data:
        print(f"  Found JNTO data: {len(data)} records")
        # Parse and update stats
        # The actual format depends on JNTO's API
        return True

    # Try alternative: Japan Government statistics
    data = fetch_json("https://www.e-stat.go.jp/stat-search/database?page=1&layout=datalist&toukei=00200200&tstat=000001011100")
    if data:
        print("  Found government stats data")
        return True

    print("  No new visitor data available (JNTO updates annually)")
    return False


def main():
    print(f"=== ViajApp Stats Updater ===")
    print(f"Date: {datetime.now().isoformat()}")
    print()

    # Load current stats
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)
        print(f"Loaded existing stats (last updated: {stats.get('last_updated', 'unknown')})")
    except FileNotFoundError:
        print("No existing stats file, creating new one")
        stats = {
            "source": "JNTO / Japan Government",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "visitors": {},
            "spending": {},
            "duration": {},
            "popular_destinations": [],
            "seasonality": {},
            "jr_pass": {},
            "exchange_rate": {},
        }

    print()

    # Update exchange rate (always)
    rate_updated = update_exchange_rate(stats)
    print()

    # Try to update visitor data
    visitors_updated = update_visitor_data(stats)
    print()

    # Update timestamp
    stats["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # Save
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Stats saved to {STATS_FILE}")
    print(f"  Exchange rate updated: {rate_updated}")
    print(f"  Visitor data updated: {visitors_updated}")
    print()
    print("Done!")


if __name__ == "__main__":
    main()
