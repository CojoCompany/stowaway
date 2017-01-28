import time
import socket
from ipaddress import ip_address

import zmq
import yaml
import quick2wire.i2c as i2c


if __name__ == '__main__':

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    server = yaml.load(open('config.yaml'))['server']
    host = server['host']
    try:
        ip_address(host)
    except ValueError:
        host = socket.gethostbyname(host)
    publisher.bind('tcp://{}:{}'.format(host, server['port']))

    while True:
        with i2c.I2CMaster() as bus:
            data = bus.transaction(i2c.reading(8, 6))
        temp = data[0][-2:]
        temp = int.from_bytes(temp, byteorder='little', signed=True)
        print(temp)
        publisher.send_pyobj(('TEMP', time.time(), temp / 100.))
        time.sleep(0.05)
