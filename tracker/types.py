from typing import TypedDict, Literal, Optional
from dataclasses import dataclass


class ExpenseFilters(TypedDict, total=False):
    month: str | None
    sort: Literal["date", "amount", "category"] | None
    desc: bool | None
    from_: str | None
    to: str | None
    category: str | None
    min: float | None
    max: float | None
    format: Literal["table", "csv"] | None
    limit: int | None


class ExpenseSummary(TypedDict):
    title: str
    grand_total: float
    total_expenses: float
    category_totals: dict
    average_per_day: float
    category_percentages: float
    highest_expense: dict
    currency: str
    summary_type: Literal["range", "monthly"]


@dataclass(frozen=True)
class ValidatedFilters:
    month: Optional[str]
    sort: Optional[Literal["date", "amount", "category"]]
    from_date: Optional[str]
    to_date: Optional[str]
    category: Optional[str]
    min_amount: Optional[float]
    max_amount: Optional[float]
    limit: Optional[int]
    sort_direction: int
