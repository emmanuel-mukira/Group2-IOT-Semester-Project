# MicroPython SH1106 OLED driver for 128x64 I2C OLED displays

from micropython import const
import framebuf
import time

_SET_CONTRAST = const(0x81)
_SET_NORM_INV = const(0xA6)
_SET_DISP = const(0xAE)
_SET_SCAN_DIR = const(0xC0)
_SET_SEG_REMAP = const(0xA0)
_LOW_COLUMN_ADDRESS = const(0x00)
_HIGH_COLUMN_ADDRESS = const(0x10)
_SET_PAGE_ADDRESS = const(0xB0)


class SH1106_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8

        # SH1106 has 132 columns internally.
        # 128x64 displays usually start at column offset 2.
        self.column_offset = 2

        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(
            self.buffer,
            self.width,
            self.height,
            framebuf.MONO_VLSB
        )

        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, data):
        self.i2c.writeto(self.addr, bytearray([0x40]) + data)

    def init_display(self):
        init_cmds = [
            _SET_DISP | 0x00,       # display off
            0xD5, 0x80,             # display clock divide ratio
            0xA8, 0x3F,             # multiplex ratio for 64 rows
            0xD3, 0x00,             # display offset
            0x40,                   # display start line
            0xAD, 0x8B,             # DC-DC control
            0xA1,                   # segment remap
            0xC8,                   # COM output scan direction
            0xDA, 0x12,             # COM pins hardware config
            _SET_CONTRAST, 0xFF,    # contrast
            0xD9, 0x1F,             # pre-charge period
            0xDB, 0x40,             # VCOM deselect level
            0xA4,                   # entire display ON follows RAM
            _SET_NORM_INV,          # normal display
            _SET_DISP | 0x01        # display on
        ]

        for cmd in init_cmds:
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)

    def text(self, string, x, y, color=1):
        self.framebuf.text(string, x, y, color)

    def line(self, x1, y1, x2, y2, color=1):
        self.framebuf.line(x1, y1, x2, y2, color)

    def rect(self, x, y, w, h, color=1):
        self.framebuf.rect(x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color=1):
        self.framebuf.fill_rect(x, y, w, h, color)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(_SET_PAGE_ADDRESS | page)

            col = self.column_offset
            self.write_cmd(_LOW_COLUMN_ADDRESS | (col & 0x0F))
            self.write_cmd(_HIGH_COLUMN_ADDRESS | (col >> 4))

            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])

    def contrast(self, contrast):
        self.write_cmd(_SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        if invert:
            self.write_cmd(0xA7)
        else:
            self.write_cmd(0xA6)

    def poweroff(self):
        self.write_cmd(_SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(_SET_DISP | 0x01)