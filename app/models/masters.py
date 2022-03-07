from sqlalchemy import Column, Numeric, String
from ..db.base_class import Base


class Masters(Base):
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    patronymic = Column(String(100), nullable=True)
    salary = Column(Numeric(), nullable=True, default=0)
    

    
    