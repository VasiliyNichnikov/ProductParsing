from sqlalchemy import Column, Integer, String
from ..DbSession import SqlAlchemyBase


class AdModelLeroyMerlin(SqlAlchemyBase):
    __tablename__ = 'ad_leroy_merlin'

    ENTRY_ID = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(String, nullable=True)
    PRICE = Column(String, nullable=True)
    WEIGHT = Column(String, nullable=True)
    WIDTH = Column(String, nullable=True)
    HEIGHT = Column(String, nullable=True)
    MODEL = Column(String, nullable=True)
    TYPE_MODEL = Column(String, nullable=True)
    BRAND = Column(String, nullable=True)
    MANUFACTURER = Column(String, nullable=True)
    VOLUME = Column(String, nullable=True)
    MAIN_PHOTO = Column(String, nullable=True)
    ADDITIONAL_PHOTOS = Column(String, nullable=True)
    PHOTO_ARTICLES = Column(String, nullable=True)
    DESCRIPTION = Column(String, nullable=True)
    QUANTITY_GOODS = Column(String, nullable=True)
    OTHER = Column(String, nullable=True)
    URL = Column(String, nullable=True)
