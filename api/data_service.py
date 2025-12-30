from api.models import Asset, AssetMetric


def get_data(db, source=None, limit=10, offset=0):
    query = (
        db.query(
            Asset.symbol,
            Asset.name,
            AssetMetric.source,
            AssetMetric.value,
            AssetMetric.event_time
        )
        .join(AssetMetric)
    )

    if source:
        query = query.filter(AssetMetric.source == source)

    total = query.count()

    rows = (
        query
        .order_by(Asset.symbol)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, [
        {
            "symbol": s,
            "name": n,
            "source": src,
            "value": v,
            "event_time": t,
        }
        for s, n, src, v, t in rows
    ]
