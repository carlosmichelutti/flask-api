from resources.database import Connection

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String

import cryptography

class Base(DeclarativeBase):
    
    '''
        Class basis for mapping.
    '''
    pass

class Books(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    category: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[str] = mapped_column(String(50))
    
Base.metadata.create_all(Connection().engine)