from sqlalchemy import Column, Integer, String
from sqlalchemy import Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class PupHub(Base):
    __tablename__ = 'Pup_Data'

    id = Column(Integer, primary_key=True, nullable =False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    for_sale = Column(Boolean, server_default='True',default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))