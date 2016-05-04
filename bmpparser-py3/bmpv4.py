from bmp import ValidationError
from bmpinfo import BMPvInfo
from misc import Mask, int_from_bytes


class BMPv4(BMPvInfo):
    def __init__(self, raw, offset, filename):
        super().__init__(raw, offset, filename)
        self.red_mask = Mask(int_from_bytes(self.raw_bytes, 54, 58),
                             self.bit_count)
        self.green_mask = Mask(int_from_bytes(self.raw_bytes, 58, 62),
                               self.bit_count)
        self.blue_mask = Mask(int_from_bytes(self.raw_bytes, 62, 66),
                              self.bit_count)
        self.alpha_mask = Mask(int_from_bytes(self.raw_bytes, 66, 70),
                               self.bit_count)
        self.has_alpha = True
        self.color_table_offset = 122
        self.CS_type = self.raw_bytes[70:74].decode('utf-8')[::-1]
        self.end_points = []
        for i in range(74, 110, 4):
            self.end_points.append(self.raw_bytes[i:i + 4])
        self.gamma_red = int_from_bytes(self.raw_bytes, 110, 114)
        self.gamma_green = int_from_bytes(self.raw_bytes, 114, 118)
        self.gamma_blue = int_from_bytes(self.raw_bytes, 118, 122)

    def print_info(self):
        """
        Печатает информацию о файле
        """
        super().print_info()
        print('Red mask:\t{}'.format(self.red_mask.mask))
        print('Green mask:\t{}'.format(self.green_mask.mask))
        print('Blue mask:\t{}'.format(self.blue_mask.mask))
        print('Alpha mask:\t{}'.format(self.alpha_mask.mask))
        print('CS Type:\t{}'.format(self.CS_type))
        print('End points:\t{}'.format(self.end_points))
        print('Red gamma:\t{}'.format(self.gamma_red))
        print('Green gamma:\t{}'.format(self.gamma_green))
        print('Blue gamma:\t{}'.format(self.gamma_blue))

    def validate(self):
        """Проверяет чтобы все поля удовлетворяли требованиям спецификации"""
        super().validate()
        if self.CS_type not in ['\x00\x00\x00\x00', 'sRGB',
                                'LINK', 'MBED', 'WIN ']:
            raise ValidationError('Ошибка в поле "CSType". В данном файле %s'
                                  % self.CS_type)
