from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

SqlAlchemyBase = declarative_base()

def global_init(db_file):
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = db_file

    engine = create_engine(conn_str, echo=False)
    SqlAlchemyBase.metadata.create_all(engine)

    session = sessionmaker(bind=engine)
    return session()
