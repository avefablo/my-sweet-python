from bmp import BMPFile, ValidationError
from misc import int_from_bytes
from palette import ColorTable, ColoredPixelArray
from pixel_array import PixelArray


class BMPvCORE(BMPFile):
    """
    Версия BMP с заголовком размера 12
    """

    def __init__(self, raw, offset, filename):
        super().__init__(raw, offset, filename)
        self.width = int_from_bytes(self.raw_bytes, 18, 20)
        self.height = int_from_bytes(self.raw_bytes, 20, 22)
        self.planes = int_from_bytes(self.raw_bytes, 22, 24)
        self.bit_count = int_from_bytes(self.raw_bytes, 24, 26)
        self.color_table = None
        self.color_table_offset = 26
        self.is_reversed = False
        self.pixels = []

    def print_info(self):
        """
        Печатает информацию о файле
        """
        super().print_info()
        print('Width:\t{}'.format(self.width))
        print('Height:\t{}'.format(self.height))
        print('Planes:\t{}'.format(self.planes))
        print('Bit count:\t{}'.format(self.bit_count))

    def validate(self):
        """Проверяет чтобы все поля удовлетворяли требованиям спецификации"""
        if self.width <= 0:
            raise ValidationError('Ошибка в поле "width" '
                                  'Должно быть больше нуля. В данном файле %i'
                                  % self.width)

        if self.height <= 0:
            raise ValidationError('Ошибка в поле "height" '
                                  'Должно быть больше нуля. В данном файле %i'
                                  % self.height)

        if self.planes != 1:
            raise ValidationError('Ошибка в поле "planes". '
                                  'Должно быть 1. В данном файле %i'
                                  % self.planes)
        if self.bit_count not in [1, 2, 4, 8, 24]:
            raise ValidationError('Глубина цвета %i не поддерживается'
                                  % self.bit_count)

    def parse_pixels(self):
        """Парсит пиксели в соответствии с таблицей цветов"""
        if self.bit_count <= 8:
            self.color_table = ColorTable(self, 3)
            self.pixels = ColoredPixelArray(self).get_colored_pixel_array()
        elif self.bit_count == 24:
            p = PixelArray(self)
            self.pixels = p.parse_pixel_array(p.get_24_bit_pixel)
