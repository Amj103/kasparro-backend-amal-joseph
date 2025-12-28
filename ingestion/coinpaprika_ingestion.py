import requests
from sqlalchemy.orm import Session
from api.models import RawCoinPaprika, NormalizedData, ETLCheckpoint

SOURCE_NAME = "coinpaprika"
BASE_URL = "https://api.coinpaprika.com/v1"


def ingest_coinpaprika(db: Session):
    checkpoint = db.get(ETLCheckpoint, SOURCE_NAME)
    last_rank = checkpoint.last_processed_id if checkpoint else 0
    processed = 0

    response = requests.get(f"{BASE_URL}/coins", timeout=10)
    response.raise_for_status()
    coins = response.json()

    for coin in coins:
        rank = coin.get("rank") or 0
        if rank <= last_rank:
            continue

        coin_id = coin["id"]

        db.merge(
            RawCoinPaprika(
                id=coin_id,
                payload=coin
            )
        )

        db.merge(
            NormalizedData(
                source=SOURCE_NAME,
                external_id=rank,
                name=coin.get("name"),
                value=None,
                event_time=None
            )
        )

        last_rank = rank
        processed += 1

    if checkpoint:
        checkpoint.last_processed_id = last_rank
    else:
        db.add(
            ETLCheckpoint(
                source_name=SOURCE_NAME,
                last_processed_id=last_rank
            )
        )

    db.commit()
    return processed
