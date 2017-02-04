# Data structures exchanged between Cypress and Raspberry pi within i2c. 
# The C structures from Cypress are saved as python lists of tuplas [name, size]
# where the size is a character specified on python struct module (https://docs.python.org/3/library/struct.html) that corresponds to C types.

five_std_sensors =  [('Version','H'),
    ('Vth','H'),
    ('Rth','H'),
    ('Temperature','h'),
    ('ALSCurrent','H'),
    ('LightIntensity','H'),
    ('PIRRaw','h'),
    ('PIRHpf','h'),
    ('PIRWindowHigh','h'),
    ('PIRWindowLow','h'),
    ('PIRTrigger','h'),
    ('IPSRawCounts','h'),
    ('IPSDifferenceCounts','h'),
    ('IPSBaselineCounts','h'),
    ('IPSTrigger','H'),
    ('RawCountsRefCap','H'),
    ('RawCountsHumidity','H'),
    ('SensorCapacitance','H'),
    ('Humidity','H')]