# =================================================
# sh1106.py
# SH1106 OLED display driver for 128x64 I2C OLED
# =================================================

import framebuf


class SH1106_I2C(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8

        self.buffer = bytearray(self.width * self.pages)

        super().__init__(
            self.buffer,
            self.width,
            self.height,
            framebuf.MONO_VLSB
        )

        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def write_data(self, data):
        self.i2c.writeto(self.addr, bytearray([0x40]) + data)

    def init_display(self):
        # Initialization sequence for SH1106 OLED.
        cmds = [
            0xAE,       # Display OFF
            0xD5, 0x80, # Set display clock
            0xA8, 0x3F, # Multiplex ratio
            0xD3, 0x00, # Display offset
            0x40,       # Display start line
            0xAD, 0x8B, # DC-DC control
            0xA1,       # Segment remap
            0xC8,       # COM output scan direction
            0xDA, 0x12, # COM pins hardware configuration
            0x81, 0xCF, # Contrast
            0xD9, 0xF1, # Pre-charge period
            0xDB, 0x40, # VCOM detect
            0xA4,       # Resume RAM display
            0xA6,       # Normal display
            0xAF        # Display ON
        ]

        for cmd in cmds:
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def show(self):
        # SH1106 usually needs a small column offset.
        column_offset = 2

        for page in range(self.pages):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x00 + (column_offset & 0x0F))
            self.write_cmd(0x10 + ((column_offset >> 4) & 0x0F))

            start = self.width * page
            end = start + self.width

            self.write_data(self.buffer[start:end])