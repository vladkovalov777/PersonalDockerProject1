from apps.core.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String


class Product(Base):
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(default="")
    main_image: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)