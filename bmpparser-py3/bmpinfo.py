from struct import unpack

from bmp import BMPFile, ValidationError
from misc import Mask, int_from_bytes
from palette import ColoredPixelArray, ColorTable
from pixel_array import PixelArray
from rle import RLEDecoder


class BMPvInfo(BMPFile):
    """Представляет версию BMP с заголовком размера 40"""

    def __init__(self, raw, offset, filename):
        super().__init__(raw, offset, filename)
        self.width = unpack("i", self.raw_bytes[18:22])[0]
        self.height = unpack("i", self.raw_bytes[22:26])[0]
        self.planes = int_from_bytes(self.raw_bytes, 26, 28)
        self.bit_count = int_from_bytes(self.raw_bytes, 28, 30)
        self.compression = int_from_bytes(self.raw_bytes, 30, 34)
        self.size_image = int_from_bytes(self.raw_bytes, 34, 38)
        self.x_pels_per_meter = int_from_bytes(self.raw_bytes, 38, 42)
        self.y_pels_per_meter = int_from_bytes(self.raw_bytes, 42, 46)
        self.clr_used = int_from_bytes(self.raw_bytes, 46, 50)
        self.clr_important = int_from_bytes(self.raw_bytes, 50, 54)
        self.color_table_offset = 54
        self.opacity = 1
        self.color_table = None
        self.pixels = None
        self.red_mask = None
        self.green_mask = None
        self.blue_mask = None
        self.alpha_mask = None
        self.is_reversed = self.height < 0
        self.height = abs(self.height)
        self.has_alpha = False
        if self.compression == 3:
            self.color_table_offset = 66
        if self.compression == 6:
            self.color_table_offset = 70
            self.has_alpha = True

    def print_info(self):
        """Печатает информацию о файле"""
        super().print_info()
        print('Width:\t{}'.format(self.width))
        print('Height:\t{}'.format(self.height))
        print('Planes:\t{}'.format(self.planes))
        print('Bit count:\t{}'.format(self.bit_count))
        print('Compression:\t{}'.format(self.compression))
        print('Size image:\t{}'.format(self.size_image))
        print('X pels per meter:\t{}'.format(self.x_pels_per_meter))
        print('Y pels per meter:\t{}'.format(self.y_pels_per_meter))
        print('Clr used:\t{}'.format(self.clr_used))
        print('Clr important:\t{}'.format(self.clr_important))

    def validate(self):
        """Проверяет чтобы все поля удовлетворяли требованиям спецификации"""
        if self.width <= 0:
            raise ValidationError('Ошибка в поле "width"'
                                  'Должно быть больше нуля. В данном файле %i'
                                  % self.width)
        if self.height == 0:
            raise ValidationError('Ошибка в поле "height"'
                                  'Не должно равняться нулю. В данном файле %i'
                                  % self.height)
        if self.compression not in [0, 1, 2, 3, 6]:
            raise ValidationError('Компрессия вида %i не поддерживается'
                                  % self.compression)

        if self.planes != 1:
            raise ValidationError('Ошибка в поле "planes"'
                                  'Должно быть 1. В данном файле %i'
                                  % self.planes)
        if self.bit_count not in [1, 2, 4, 8, 16, 24, 32, 48, 64]:
            raise ValidationError('Глубина цвета %i не поддерживается'
                                  % self.bit_count)
        if self.clr_used > 0:
            max_capacity = 2 ** self.bit_count
            if self.clr_used > max_capacity:
                error_msg = 'Таблице цветов превышает допустимый размер {}.' \
                            'В данном файле {}'.format(max_capacity,
                                                       self.clr_used)
                raise ValidationError(error_msg)

    def parse_pixels(self):
        """
        Определяет метод определения пикселей
        и записывает пиксели в self.pixels
        """
        if self.bit_count <= 8 and self.compression == 0:
            parser = ColoredPixelArray(self)
            self.color_table = ColorTable(self, 4)
            self.pixels = parser.get_colored_pixel_array()

        elif self.bit_count == 4 and self.compression == 2:
            rle = RLEDecoder(self)
            self.color_table = ColorTable(self, 4)
            rle.rle_4bit()
            self.pixels = rle.pixels

        elif self.bit_count == 8 and self.compression == 1:
            rle = RLEDecoder(self)
            self.color_table = ColorTable(self, 4)
            rle.rle_8bit()
            self.pixels = rle.pixels

        elif self.bit_count in [16, 32]:
            self.red_mask, self.green_mask, self.blue_mask = self.get_mask()
            p = PixelArray(self)
            self.pixels = p.parse_pixel_array(p.get_16_or_32_bit_pixel)

        elif self.bit_count == 24:
            p = PixelArray(self)
            self.pixels = p.parse_pixel_array(p.get_24_bit_pixel)

        elif self.bit_count == 48:
            p = PixelArray(self)
            self.pixels = p.parse_pixel_array(p.get_48_bit_pixel)

        elif self.bit_count == 64:
            p = PixelArray(self)
            self.pixels = p.parse_pixel_array(p.get_64_bit_pixel)

    def get_mask(self):
        """Возвращает маску каналов"""
        red_mask = None
        green_mask = None
        blue_mask = None
        if self.compression in [3, 6]:
            red_mask = Mask(int_from_bytes(self.raw_bytes, 54, 58),
                            self.bit_count)
            green_mask = Mask(int_from_bytes(self.raw_bytes, 58, 62),
                              self.bit_count)
            blue_mask = Mask(int_from_bytes(self.raw_bytes, 62, 66),
                             self.bit_count)
            if self.compression == 6:
                self.alpha_mask = Mask(int_from_bytes(self.raw_bytes, 66, 70),
                                       self.bit_count)
        elif self.bit_count == 16:
            red_mask = Mask(0x7c00, 16)
            green_mask = Mask(0x03e0, 16)
            blue_mask = Mask(0x001f, 16)
        elif self.bit_count == 32:
            red_mask = Mask(0x00ff0000, 32)
            green_mask = Mask(0x0000ff00, 32)
            blue_mask = Mask(0x000000ff, 32)
        return red_mask, green_mask, blue_mask
