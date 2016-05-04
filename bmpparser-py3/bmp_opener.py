from sys import exit

from bmpcore import BMPvCORE
from bmpinfo import BMPvInfo
from bmpv4 import BMPv4
from bmpv5 import BMPv5
from misc import int_from_bytes

BMPCOREHEADERSIZE = 12
BMPINFOHEADERSIZE = 40
BMPV4HEADERSIZE = 108
BMPV5HEADERSIZE = 124


class BMPOpener:
    """
    Считывает байты из файла, открывает файл как BMP (определяется версия и
    создается объект соотв. класса)
    Поддерживаются версии заголовков BMP размера 12, 40, 108, 124
    """

    def read_raw_bytes(self, filename):
        """Читает поток байтов"""
        return open(filename, 'rb').read()

    def __init__(self, filename):
        self.filename = filename
        self.raw_bytes = self.read_raw_bytes(filename)
        self.size, self.offset = self.parse_file_header()
        self.bc_size = int.from_bytes(self.raw_bytes[14:18],
                                      byteorder='little')
        self.bmp_file = self.open_as_bmp()

    def parse_file_header(self):
        """
        Парсит DIB. Проверяет, что первые два байта это "BM" и
        что зарезервированные значения равны нулю
        """
        bitmap_file_header = self.raw_bytes[:14]
        bf_type = bitmap_file_header[0:2].decode('utf-8')
        bf_size = int_from_bytes(bitmap_file_header, 2, 6)
        bf_reserved1 = int_from_bytes(bitmap_file_header, 6, 8)
        bf_reserved2 = int_from_bytes(bitmap_file_header, 8, 10)
        bf_off_bits = int_from_bytes(bitmap_file_header, 10, 14)
        if bf_type != "BM":
            print("First two bytes is not BM")
            exit()
        if bf_reserved1 != 0 or bf_reserved2 != 0:
            print("One of reserved fields isn't zero")
            exit()
        return bf_size, bf_off_bits

    def open_as_bmp(self):
        """
        В зависимости от размера заголовка открывает файл как BMP
        """
        if self.bc_size == BMPCOREHEADERSIZE:
            return BMPvCORE(self.raw_bytes, self.offset, self.filename)
        elif self.bc_size == BMPINFOHEADERSIZE:
            return BMPvInfo(self.raw_bytes, self.offset, self.filename)
        elif self.bc_size == BMPV4HEADERSIZE:
            return BMPv4(self.raw_bytes, self.offset, self.filename)
        elif self.bc_size == BMPV5HEADERSIZE:
            return BMPv5(self.raw_bytes, self.offset, self.filename)
        else:
            print("Not supported format")
            exit()
