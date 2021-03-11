from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import orm
from ..db_session import SqlAlchemyBase


class Link(SqlAlchemyBase):
    __tablename__ = 'links'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    LINK = Column(String, nullable=True)
    SITE_ID = Column(Integer, ForeignKey('sites.ID'))
    SITE = orm.relation('Site')

