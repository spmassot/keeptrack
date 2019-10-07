from src.models.base import BaseModel
import pynamodb.attributes as atr


class Customer(BaseModel):
    class Meta:
        table_name = 'my-qb-customer'
        region = 'us-east-1'
        read_capacity_units = 1
        write_capacity_units = 1

    id = atr.UnicodeAttribute(hash_key=True)
    name = atr.UnicodeAttribute()
    attn = atr.UnicodeAttribute()
    address_1 = atr.UnicodeAttribute()
    address_2 = atr.UnicodeAttribute(null=True)
    city = atr.UnicodeAttribute()
    state = atr.UnicodeAttribute()
    zip_code = atr.UnicodeAttribute()
    email = atr.UnicodeAttribute()


def init():
    if not Customer.exists():
        Customer.create_table()
