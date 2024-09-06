from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql://postgres:qwerty@localhost/bank_system')
engine.connect()
Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    card_number = Column(Integer, nullable=False)
    card_password = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)


Base.metadata.create_all(engine)

