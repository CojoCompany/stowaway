import time
import socket
from ipaddress import ip_address

import zmq
import yaml
import quick2wire.i2c as i2c

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datetime

from database import Temperature, Base


if __name__ == '__main__':

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    server = yaml.load(open('config.yaml'))['server']
    port = server['port']
    host = server['host']
    try:
        ip_address(host)
    except ValueError:
        host = socket.gethostbyname(host)
    publisher.bind('tcp://{}:{}'.format(host, port))
    
    # DataBase setup
    engine = create_engine('sqlite:////home/pi/sensors.db', echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    while True:
        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(8, 6))
        temp = data[0][-2:]
        temp = int.from_bytes(temp, byteorder='little', signed=True)
        print(temp)
        publisher.send_pyobj(temp)
        
        # DB storage
        session = Session()
        session.add(Temperature(time = datetime.datetime.now(), temperature = temp))
        session.commit()
        session.close()
        
        time.sleep(0.05)
