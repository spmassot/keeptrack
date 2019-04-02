from dataclasses import dataclass
from src.models.base import BaseModel
import pynamodb.attributes as atr


class Invoice(BaseModel):
    class Meta:
        table_name = 'my-qb-invoice'
        region = 'us-east-1'
        read_capacity_units = 1
        write_capacity_units = 1

    id = atr.UnicodeAttribute(hash_key=True)
    number = atr.NumberAttribute()
    customer_id = atr.UnicodeAttribute()
    issued_on = atr.UTCDateTimeAttribute(range_key=True)
    paid_on = atr.UTCDateTimeAttribute(null=True)
    total = atr.NumberAttribute()
    tasks = atr.ListAttribute()
    archived = atr.BooleanAttribute(null=True)


def init():
    if not Invoice.exists():
        Invoice.create_table()


@dataclass
class Task:
    date: str = None
    hours: float = 0.0
    description: str = None
    rate: float = 0.0
