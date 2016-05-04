from math import floor

from misc import Pixel


class PixelArray():
    """Парсит массив пикселей с помощью переданного парсера
    для битностей больше 8"""

    def __init__(self, bmp):
        self.bmp = bmp

    def parse_pixel_array(self, parser):
        """Парсит двумерный массив пикселей"""
        result = []
        start = self.bmp.bf_offset
        step = int(floor((self.bmp.bit_count * self.bmp.width + 31) / 32) * 4)
        for y in range(self.bmp.height):
            a = self.bmp.raw_bytes[start: start + step]
            row = []
            for i in range(0, self.bmp.width * self.bmp.bit_count // 8,
                           self.bmp.bit_count // 8):
                t = parser(a[i: i + self.bmp.bit_count // 8])
                row.append(t)
            result.append(row)
            start += step
        return result

    def get_16_or_32_bit_pixel(self, raw_bytes):
        """
        Возвращает пиксель при использовании
        16 или 32 битной глубине цвета
        """
        rgba = int.from_bytes(raw_bytes, byteorder='little')
        red = (rgba & self.bmp.red_mask.mask) >> self.bmp.red_mask.shift
        green = (rgba & self.bmp.green_mask.mask) >> self.bmp.green_mask.shift
        blue = (rgba & self.bmp.blue_mask.mask) >> self.bmp.blue_mask.shift
        red = self.convert(red, self.bmp.red_mask.width, 8)
        green = self.convert(green, self.bmp.green_mask.width, 8)
        blue = self.convert(blue, self.bmp.blue_mask.width, 8)
        alpha = 255
        if self.bmp.has_alpha:
            alpha = (rgba & self.bmp.alpha_mask.mask) \
                    >> self.bmp.alpha_mask.shift
            alpha = self.convert(alpha, self.bmp.alpha_mask.width, 8)
        return Pixel(red, green, blue, alpha)

    def convert(self, value, bits_from, bits_to):
        """Конвертирует значение из from-битной в to-битную"""
        return int((value / (1 << bits_from)) * (1 << bits_to))

    def get_24_bit_pixel(self, raw_bytes):
        """Возвращает пиксель при использовании 24 битной глубины цвета"""
        r = raw_bytes[2]
        g = raw_bytes[1]
        b = raw_bytes[0]
        return Pixel(r, g, b)

    def get_48_bit_pixel(self, raw_bytes):
        """Возвращает пиксель при использовании 48 битной глубины цвета"""
        r = raw_bytes[4:6]
        g = raw_bytes[2:4]
        b = raw_bytes[0:2]
        r = self.convert(r, self.bmp.bit_count, 8)
        g = self.convert(g, self.bmp.bit_count, 8)
        b = self.convert(b, self.bmp.bit_count, 8)
        return Pixel(r, g, b)

    def get_64_bit_pixel(self, raw_bytes):
        """Возвращает пиксель при использовании 64 битной глубины цвета"""
        a = raw_bytes[6:8]
        r = raw_bytes[4:6]
        g = raw_bytes[2:4]
        b = raw_bytes[0:2]
        r = self.convert(r, self.bmp.bit_count, 8)
        g = self.convert(g, self.bmp.bit_count, 8)
        b = self.convert(b, self.bmp.bit_count, 8)
        return Pixel(r, g, b, a)
