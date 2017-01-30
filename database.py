from threading import Thread

import zmq
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, Float, DateTime


class Writer(Thread):
    def __init__(self, context, polltimeout=100):
        super().__init__()

        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect('inproc://dbwrite')
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
        self.poller = zmq.Poller()
        self.poller.register(self.subscriber, zmq.POLLIN)

        self.db_uri = 'mysql+mysqldb://cypress:cypress@localhost:3306/sensors'

    def run(self):
        engine = create_engine(self.db_uri, echo=True)
        session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)

        while True:
            events = dict(self.poller.poll(100))
            if not events:
                continue
            for socket in events:
                if events[socket] != zmq.POLLIN:
                    continue
                message = socket.recv_pyobj()
                self.store(session, message)
            session.commit()
        session.close()

    def store(self, session, message):
        identifier, datetime, data = message
        # DB storage
        if identifier == 'TEMP':
            session.add(Temperature(time=datetime,
                                    temperature=data))


Base = declarative_base()
class Sensor():

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Temperature(Sensor, Base):
    temperature = Column(Float)

    def __repr__(self):
        return "<T(time='%s', temperature='%s')>" % (
            self.time, self.temperature)
