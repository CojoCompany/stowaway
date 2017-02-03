import time
import socket
import datetime
from ipaddress import ip_address


import zmq
import yaml
import quick2wire.i2c as i2c

import logging

if __name__ == '__main__':

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    database = context.socket(zmq.PUB)
    server = yaml.load(open('config.yaml'))['server']
    host = server['host']
    try:
        ip_address(host)
    except ValueError:
        host = socket.gethostbyname(host)
    publisher.bind('tcp://{}:{}'.format(host, server['port']))
    database.bind('inproc://dbwrite')

    logging.basicConfig(format='%(levelname)s,%(message)s',
                        filename='sensors.log', level=logging.INFO)

    while True:
        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(8, 6))
        now = datetime.datetime.utcnow()
        temp = data[0][-2:]
        temp = int.from_bytes(temp, byteorder='little', signed=True) / 100.
        publisher.send_pyobj(('TEMP', now.timestamp(), temp))
        print(now, temp)
        logging.info('T,{},{}'.format(now,temp))
        logging.info('H,{},{}'.format(now,temp))
        logging.info('L,{},{}'.format(now,temp))

        time.sleep(0.05)
