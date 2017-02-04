import time
import socket
import datetime
from ipaddress import ip_address


import zmq
import yaml
import quick2wire.i2c as i2c

import logging

import struct
from datastructs import five_std_sensors as l

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
    
    format_chain = ''.join(x[1] for x in l)
    format_chain_s = struct.calcsize(format_chain)

    while True:
        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(8, format_chain_s))
        now = datetime.datetime.utcnow()
        field = struct.unpack("<" + format_chain,data[0])
        data_dict = dict(zip([y[0] for y in l], field))
        temp = data_dict['Temperature']/10
        hum = data_dict['Humidity']/10
        light = data_dict['LightIntensity']
        publisher.send_pyobj(('T', now.timestamp(), temp))
        publisher.send_pyobj(('H', now.timestamp(), hum))
        publisher.send_pyobj(('L', now.timestamp(), light))
        logging.info('T,{},{}'.format(now,temp))
        logging.info('H,{},{}'.format(now,hum))
        logging.info('L,{},{}'.format(now,light))
        print(now, temp, hum, light)

        time.sleep(0.05)
