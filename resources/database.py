from _load_env import (
    db_user,
    db_host,
    db_pass,
    db_port,
    db_name
)

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Connection:

    def __init__(
        self: object
    ) -> None:
        
        self.engine = create_engine(f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
        self.base = declarative_base()
        self.session = Session(self.engine)

DB_CONNECTION = Connection()