
from sqlalchemy.orm import Session
from api.models import NormalizedData


def get_data(
    db: Session,
    source: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = db.query(NormalizedData)

    if source:
        query = query.filter(NormalizedData.source == source)

    total = query.count()

    rows = (
        query
        .order_by(NormalizedData.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, rows
