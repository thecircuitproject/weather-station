# MicroPython Project with Raspberry Pi Pico W, AHT20 Sensor, and OLED Screen

## Introduction

This project uses a Raspberry Pi Pico W, an AHT20 temperature and humidity sensor, and an OLED screen to display the sensor readings. The project is programmed using MicroPython.

## Hardware Requirements

- Raspberry Pi Pico W
- AHT20 Temperature and Humidity Sensor
- OLED Screen

## Software Requirements

- MicroPython
- Thonny IDE or any other Python IDE that supports MicroPython
- API Key from https://openweathermap.org/

## Setup

1. **Flash MicroPython onto the Raspberry Pi Pico W**: Follow the instructions here.

2. **Connect the AHT20 sensor and OLED screen to the Raspberry Pi Pico W**: Connect the sensor and screen to the Raspberry Pi Pico W using the GPIO pins. Make sure to connect the power (VCC and GND) and data pins (SDA and SCL) correctly.

3. **Install the necessary MicroPython libraries**: You will need the `ssd1306` library for the OLED screen. These can be installed via the Thonny IDE.

4. **Change the name of the keys module**: Rename `example_key.py` to `key.py`.

5. **Before running the `weather_station.py` file**: upload `key.py` and `AHT.py` to the Pico board.

## License

This project is licensed under the MIT License.
