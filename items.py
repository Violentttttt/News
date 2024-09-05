from pydantic import BaseModel
from typing import Optional, Union


class RSSItem(BaseModel):
    title: str
    link: str
    description: Optional[str] = None
    published_date: Optional[str] = None


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None