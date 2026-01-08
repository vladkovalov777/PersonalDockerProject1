from pydantic import BaseModel, Field
from datetime import datetime


class SavedProductSchema(BaseModel):
    id: int
    title: str
    description: str
    main_image: str
    images: list[str]
    price: int = Field(qt=0)
    created_at: datetime