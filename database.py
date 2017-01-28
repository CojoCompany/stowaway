import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime


Base = declarative_base()
class Sensor():
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    
class Temperature(Sensor, Base):
    temperature = Column(Integer)
    
    def __repr__(self):
        return "<T(time='%s', temperature='%s')>" % (
            self.time, self.temperature)        