from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AwardQuote:
    carrier: str
    origin: str
    destination: str
    date: str
    points: int
    cash_usd: float

    @property
    def cents_per_point(self) -> float | None:
        if self.points <= 0:
            return None
        return (self.cash_usd / self.points) * 100


@dataclass(frozen=True)
class AlertCriteria:
    min_cents_per_point: float | None = None
    max_points: int | None = None


def is_alert(quote: AwardQuote, criteria: AlertCriteria) -> bool:
    cpp = quote.cents_per_point
    if criteria.min_cents_per_point is not None:
        if cpp is None or cpp < criteria.min_cents_per_point:
            return False
    if criteria.max_points is not None and quote.points > criteria.max_points:
        return False
    return True
