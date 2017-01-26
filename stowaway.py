import time

from smbus2 import SMBusWrapper


print('Hello')

while True:
    try:
        with SMBusWrapper(1) as bus:
            # Read a block of 16 bytes from address 80, offset 0
            block = bus.read_i2c_block_data(80, 0, 16)
    except:
        print('error...')
    time.sleep(0.5)

# Returned value is a list of 16 bytes
print(block)
