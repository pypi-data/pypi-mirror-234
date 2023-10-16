from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from .PriceModel import Price

class ShippingProfileDestination(BaseModel):
    shipping_profile_destination_id: int
    shipping_profile_id: int
    origin_country_iso: str
    destination_country_iso: str
    destination_region: str
    primary_cost: Price
    secondary_cost: Price
    shipping_carrier_id: Optional[int]
    mail_class: Optional[str]
    min_delivery_days: Optional[int]
    max_delivery_days: Optional[int]