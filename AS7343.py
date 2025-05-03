import time
import board
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

# I2C address
_AS7343_I2C_ADDR = const(0x39)

# Register map
ENABLE = const(0x80)
CFG0 = const(0xBF)
CFG1 = const(0xC6)  # ✅ Correct for AS7343
CFG20 = const(0xD6)
CH_BASE = const(0x95)

# Enable bits
PON = const(0x01)
SP_EN = const(0x02)
SMUX_EN = const(0x08)

# Gain constants (AGAIN in CFG1)
GAIN_0_5X = 0x00
GAIN_1X   = 0x01
GAIN_2X   = 0x02
GAIN_4X   = 0x03
GAIN_8X   = 0x04
GAIN_16X  = 0x05
GAIN_32X  = 0x06
GAIN_64X  = 0x07
GAIN_128X = 0x08
GAIN_256X = 0x09
GAIN_512X = 0x0A
GAIN_1024X = 0x0B
GAIN_2048X = 0x0C

CHANNELS = [
    "F1", "F2", "F3", "F4", "FY", "F5", "F6",
    "F7", "F8", "FZ", "FXL", "NIR", "CLR", "RESERVED"
]

class AS7343:
    def __init__(self, i2c):
        self.dev = I2CDevice(i2c, _AS7343_I2C_ADDR)
        self._gain = None
        self._initialize_sensor()
        self.set_gain(GAIN_4X)
        time.sleep(0.1)

    def _initialize_sensor(self):
        self._write_u8(CFG0, 0x00)
        self._write_u8(ENABLE, PON | SP_EN | SMUX_EN)
        self._write_u8(CFG20, 0x03 << 5)  # auto_smux mode 3

    def set_gain(self, gain_code):
        if not (0x00 <= gain_code <= 0x0C):
            raise ValueError("Invalid gain code")
        self._write_u8(CFG1, gain_code)
        self._gain = gain_code
        self._write_u8(ENABLE, PON)
        time.sleep(0.01)
        self._write_u8(ENABLE, PON | SP_EN | SMUX_EN)

    def get_gain(self):
        return self._gain

    def trigger_measurement(self):
        self._write_u8(ENABLE, PON | SP_EN)
        time.sleep(0.5)
        self._write_u8(ENABLE, PON)

    def read_all(self):
        self.trigger_measurement()
        result = {}
        for i, name in enumerate(CHANNELS):
            reg = CH_BASE + (i * 2)
            result[name] = self._read_u16(reg)
        return result

    def _write_u8(self, reg, val):
        with self.dev:
            self.dev.write(bytes([reg, val]))

    def _read_u16(self, reg):
        buf = bytearray(2)
        with self.dev:
            self.dev.write(bytes([reg]))
            self.dev.readinto(buf)
        return buf[0] | (buf[1] << 8)
