from bmp import ValidationError
from bmpv4 import BMPv4
from misc import int_from_bytes


class BMPv5(BMPv4):
    def __init__(self, raw, offset, filename):
        super().__init__(raw, offset, filename)
        self.intent = int_from_bytes(self.raw_bytes, 122, 126)
        self.profile_data = int_from_bytes(self.raw_bytes, 126, 130)
        self.profile_size = int_from_bytes(self.raw_bytes, 130, 134)
        self.reserved = int_from_bytes(self.raw_bytes, 134, 138)
        self.color_table_offset = 138

    def print_info(self):
        """
        Печатает информацию о файле
        """
        super().print_info()
        print('Intent:\t{}'.format(self.intent))
        print('Profile data:\t{}'.format(self.profile_data))
        print('Profile size:\t{}'.format(self.profile_size))
        print('Reserved field:\t{}'.format(self.reserved))

    def validate(self):
        """Проверяет чтобы все поля удовлетворяли требованиям спецификации"""
        super().validate()
        if self.reserved != 0:
            error_msg = 'Ошибка в поле "Reserved". Должно быть обнулено'' \
            ''В данном файле %s' % self.reserved
            raise ValidationError(error_msg)
        if self.intent not in [1, 2, 4, 8]:
            raise ValidationError('Ошибка в поле "intent". В данном файле %s'
                                  % self.intent)
