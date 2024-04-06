from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime



class EventBase(BaseModel):
    """Abstract event class"""
    customer_id: int
    event_type: str
    timestamp: datetime = Field(example="2023-10-23T14:30:00")
    email_id: int
    #id: Optional[str] = None

class EmailClickEvent(EventBase):
    clicked_link: HttpUrl

class PurchaseEvent(EventBase):
    product_id: int
    amount: float

class EmailOpenEvent(EventBase):
    pass

class EmailUnsubscribeEvent(EventBase):
    pass

class EventResponse(EventBase):
    clicked_link: Optional[HttpUrl] = None
    product_id: Optional[int] = None
    amount: Optional[float] = None