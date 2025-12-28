import requests
from sqlalchemy.orm import Session
from api.models import NormalizedData, ETLCheckpoint

SOURCE_NAME = "coingecko"
BASE_URL = "https://api.coingecko.com/api/v3"


def ingest_coingecko(db: Session):
    checkpoint = db.get(ETLCheckpoint, SOURCE_NAME)
    page = checkpoint.last_processed_id if checkpoint else 1
    processed = 0

    while True:
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": page,
            "sparkline": "false",
        }

        resp = requests.get(f"{BASE_URL}/coins/markets", params=params, timeout=15)
        resp.raise_for_status()
        coins = resp.json()

        if not coins:
            break

        for coin in coins:
            # Upsert price into normalized_data
            db.merge(
                NormalizedData(
                    source=SOURCE_NAME,
                    external_id=hash(coin["id"]) & 0x7FFFFFFF,
                    name=coin.get("name"),
                    value=coin.get("current_price"),
                    event_time=None,
                )
            )
            processed += 1

        page += 1

        # Be gentle to the API
        if page > 5:  # limit pages per run (safe default)
            break

    if checkpoint:
        checkpoint.last_processed_id = page
    else:
        db.add(
            ETLCheckpoint(
                source_name=SOURCE_NAME,
                last_processed_id=page
            )
        )

    db.commit()
    return processed
