import logging

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    ForeignKey,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()
logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def connect():
    """
    Connects to the database
    :return:
    """
    try:
        connection_string = "postgresql://postgres:postgres@localhost:5432/CarSharing"
        engine = create_engine(connection_string)
        session = sessionmaker(bind=engine)
        db_session = session()
        return db_session, engine
    except OperationalError as e:
        logging.error(f"Failed to connect to the database: {str(e)}")


class Car(Base):
    __tablename__="cars"
    car_id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    owner_id = Column(Integer)
    current_renter = Column(Integer)
    available = Column(Boolean)

class Owner(Base):
    __tablename__="owners"
    owner_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

class Renter(Base):
    __tablename__="renters"
    renter_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    car_id = Column(Integer)

if __name__ == "__main__":
    """
    Creates the database
    """
    logging.info("Creating new database...")
    session, engine = connect()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session.close()
