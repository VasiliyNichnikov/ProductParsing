from sqlalchemy import Column, Integer, String
from sqlalchemy import orm
from ..DbSession import SqlAlchemyBase


class Site(SqlAlchemyBase):
    __tablename__ = 'sites'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    NAME_SITE = Column(String, nullable=True)
    DELAY_ERROR = Column(Integer, nullable=True)
    DELAY_AD = Column(Integer, nullable=True)
    CAPTCHA = Column(String, nullable=True)
    NAME_EXCEL_TABLE = Column(String, nullable=True)
    LINKS = orm.relation('Link', back_populates='SITE')
