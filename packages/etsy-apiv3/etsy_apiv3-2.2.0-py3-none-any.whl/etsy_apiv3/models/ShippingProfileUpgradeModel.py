from typing import Optional
from pydantic import BaseModel
from .PriceModel import Price

class ShippingProfileUpgrade(BaseModel):
    shipping_profile_id: int
    upgrade_id: int
    upgrade_name: str
    type: str
    rank: int
    language: str
    price: Price
    secondary_price: Price
    shipping_carrier_id: int
    mail_class: Optional[str]
    min_delivery_days: Optional[int]
    max_delivery_days: Optional[int]