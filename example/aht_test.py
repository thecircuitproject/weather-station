from machine import Pin, I2C
from time import sleep
from AHT import AHT20

sda_sensor = Pin(16)
scl_sensor = Pin(17)
i2c_sensor = I2C(id=0, scl=scl_sensor, sda=sda_sensor, freq=40_000)
sensor = AHT20(i2c_sensor)

print(sensor.temperature())
