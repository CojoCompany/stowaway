import time
import socket
import datetime
from ipaddress import ip_address


import zmq
import yaml
import quick2wire.i2c as i2c

import logging

import struct
from datastructs import gyroscope as l

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
    format_chain_size = struct.calcsize(format_chain)

    last_time = datetime.datetime.utcnow().timestamp()
    integrated = 0.
    while True:
        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(8, format_chain_size))
        now = datetime.datetime.utcnow()
        field = struct.unpack("<" + format_chain,data[0])
        data_dict = dict(zip([y[0] for y in l], field))

        gyro = data_dict['gyroscope'] - 32
        vdiff = 1.2 * gyro / 2048
        dps = vdiff / 0.003752
        degrees = dps * (now.timestamp() - last_time)
        if abs(degrees) < 0.01:
            degrees = 0
        integrated -= degrees

        temp = data_dict['temperature'] / 10
        hum = data_dict['humidity'] / 10
        light = data_dict['light']

        print(' - integrated', integrated)
        print(' - temperature', temp)
        print(' - humidity', hum)
        print(' - light', light)
        print(' - gyroscope', integrated)
        publisher.send_pyobj(('T', now.timestamp(), temp))
        publisher.send_pyobj(('H', now.timestamp(), hum))
        publisher.send_pyobj(('L', now.timestamp(), light))
        publisher.send_pyobj(('G', now.timestamp(), (0, 0, integrated)))
        logging.info('T,{},{}'.format(now, temp))
        logging.info('H,{},{}'.format(now, hum))
        logging.info('L,{},{}'.format(now, light))
        logging.info('G,{},{}'.format(now, dps))

        time.sleep(1)
        last_time = now.timestamp()
