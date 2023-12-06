import utime
from micropython import const
from machine import I2C


class AHT10:
    """Interface library for AHT10/AHT20 temperature+humidity sensors"""

    DEFAULT_I2C_ADDRESS: int = const(0x38)  # Default I2C device address
    INITIALIZATION_COMMAND: int = 0xE1  # Initialization command
    # Measurement command/Trigger Measurement
    TRIGGER_MEASUREMENT_COMMAND: int = const(0xAC)
    SOFT_RESET_COMMAND: int = const(0xBA)  # Soft reset command
    STATUS_BUSY_BIT: int = const(0x80)  # Status bit for busy
    STATUS_CALIBRATED_BIT: int = const(0x08)  # Status bit for calibrated

    def __init__(self, i2c: I2C) -> None:
        utime.sleep_ms(20)  # 20ms delay to wake up
        self._i2c = i2c
        self._buffer = bytearray(6)
        self.reset()
        if not self.initialize():
            raise RuntimeError("Could not initialize")
        self._temp = None
        self._humidity = None

    def reset(self) -> None:
        """Perform a soft-reset of the AHT"""
        self._buffer[0] = self.SOFT_RESET_COMMAND
        self._i2c.writeto(self.DEFAULT_I2C_ADDRESS, self._buffer[0:1])
        utime.sleep_ms(20)

    def initialize(self) -> bool:
        """Ask the sensor to self-initialize. Returns True on success, False otherwise"""
        self._buffer[0] = self.INITIALIZATION_COMMAND
        self._buffer[1] = 0x08
        self._buffer[2] = 0x00
        self._i2c.writeto(self.DEFAULT_I2C_ADDRESS, self._buffer[0:3])
        self._wait_for_idle()
        if self.status & self.STATUS_CALIBRATED_BIT:
            return True
        return False

    @property
    def status(self) -> int:
        """The status byte initially returned from the sensor, see datasheet for details"""
        self._read_to_buffer()
        return self._buffer[0]

    def relative_humidity(self) -> float:
        """The measured relative humidity in percent."""
        self._perform_measurement()
        self._humidity = (
            (self._buffer[1] << 12) | (self._buffer[2] << 4) | (self._buffer[3] >> 4)
        )
        self._humidity = (self._humidity * 100) / 0x100000
        return self._humidity

    def temperature(self, fahrenheit: bool = False) -> float:
        """The measured temperature in degrees Celcius."""
        self._perform_measurement()
        self._temp = (
            ((self._buffer[3] & 0xF) << 16) | (self._buffer[4] << 8) | self._buffer[5]
        )

        self._temp = ((self._temp * 200.0) / 0x100000) - 50

        if fahrenheit:
            self._temp = (9 / 5 * self._temp) + 32

        return self._temp

    def _read_to_buffer(self) -> None:
        """Read into buffer from the sensor"""
        self._i2c.readfrom_into(self.DEFAULT_I2C_ADDRESS, self._buffer)

    def _trigger_measurement(self) -> None:
        """Internal function for triggering the AHT to read temp/humidity"""
        self._buffer[0] = self.TRIGGER_MEASUREMENT_COMMAND
        self._buffer[1] = 0x33
        self._buffer[2] = 0x00
        self._i2c.writeto(self.DEFAULT_I2C_ADDRESS, self._buffer[0:3])

    def _wait_for_idle(self) -> None:
        """Wait until sensor can receive a new command"""
        while self.status & self.STATUS_BUSY_BIT:
            utime.sleep_ms(5)

    def _perform_measurement(self):
        """Trigger measurement and write result to buffer"""
        self._trigger_measurement()
        self._wait_for_idle()
        self._read_to_buffer()


class AHT20(AHT10):
    # Initialization command
    INITIALIZATION_COMMAND = 0xBE
