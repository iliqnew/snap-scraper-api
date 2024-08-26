from sqlalchemy import Column, Integer, String

from .database import Base


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    path = Column(String, index=True)
    scrape_id = Column(String, index=True)
