from math import floor

from misc import Pixel


class ColoredPixelArray:
    """Парсит массив пикселей с помощью переданного парсера
    для битностей меньше 8 (используя палитру)"""

    def __init__(self, bmp):
        self.bmp = bmp

    def get_colored_pixel_array(self):
        result = []
        start = self.bmp.bf_offset
        step = int(floor((self.bmp.bit_count * self.bmp.width + 31) / 32) * 4)
        for y in range(self.bmp.height):
            a = self.bmp.raw_bytes[start: start + step]
            row = []
            for i in range(int(self.bmp.width * self.bmp.bit_count / 8)):
                t = self.get_values_from_byte(a[i])
                for res in t:
                    row.append(self.bmp.color_table[res])
            result.append(row)
            start += step
        return result

    def get_values_from_byte(self, byte):
        """
        Возвращает подряд идущие значения
        из байта для битностей от 8 и ниже
        """
        count_of_pixels = 8 // self.bmp.bit_count
        result = []
        binary = bin(byte)[2:]
        if len(binary) < 8:
            binary = '0' * (8 - len(binary)) + binary
        for i in range(count_of_pixels):
            start = i * self.bmp.bit_count
            end = (i + 1) * self.bmp.bit_count
            result.append(int(binary[start:end], 2))
        return result


class ColorTable(list):
    """Парсит таблицу цветов"""

    def __init__(self, bmp, bytes_per_cell):
        super().__init__()
        self.bmp = bmp
        self.bytes_per_cell = bytes_per_cell
        start = self.bmp.color_table_offset
        end = start + self.bytes_per_cell * 2 ** self.bmp.bit_count
        raw = self.bmp.raw_bytes[start:end]
        for i in range(0, len(raw), bytes_per_cell):
            b = raw[i]
            g = raw[i + 1]
            r = raw[i + 2]
            self.append(Pixel(r, g, b))
