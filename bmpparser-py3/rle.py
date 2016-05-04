from misc import Pixel


class RleException(Exception):
    pass


class RLEDecoder:
    def __init__(self, bmp):
        self.bmp = bmp
        self.x = 0
        self.y = 0
        self.pos = 0
        self.rle_bytes = self.bmp.raw_bytes[self.bmp.bf_offset:]
        self.pixels = []
        for i in range(self.bmp.height):
            self.pixels.append([Pixel(0, 0, 0)] * self.bmp.width)

    def rle_8bit(self):
        """Определяет текущую RLE-команду и выполняет ее (для 8бит)"""
        while self.pos < len(self.rle_bytes):
            if self.rle_bytes[self.pos] > 0:
                self.fill_8bit_pixels()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 0:
                self.new_line()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 1:
                break

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 2:
                self.move_cursor()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] > 2:
                self.draw_8bit_pixels()

    def rle_4bit(self):
        """Определяет текущую RLE-команду и выполняет ее (для 8бит)"""
        while self.pos < len(self.rle_bytes):
            if self.rle_bytes[self.pos] > 0:
                self.fill_4bit_pixels()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 0:
                self.new_line()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 1:
                break

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] == 2:
                self.move_cursor()

            elif self.rle_bytes[self.pos] == 0 \
                    and self.rle_bytes[self.pos + 1] > 2:
                self.draw_4bit_pixels()

    def move_cursor(self):
        """Двигает курсор на pos+2 позиций вправо и pos+3 позиции вверх"""
        self.x += self.rle_bytes[self.pos + 2]
        self.y += self.rle_bytes[self.pos + 3]
        self.pos += 4

    def new_line(self):
        """Переводит курсор на новую строку"""
        self.y += 1
        self.x = 0
        self.pos += 2

    def fill_8bit_pixels(self):
        """Заливает пиксели цветом в ячейке pos+1 (для 8 бит)"""
        for j in range(self.rle_bytes[self.pos]):
            if self.in_bound() and self.pos + 1 < len(self.rle_bytes) \
                    and self.is_color(self.rle_bytes[self.pos + 1]):
                self.pixels[self.y][self.x] = \
                    self.bmp.color_table[self.rle_bytes[self.pos + 1]]
            else:
                raise RleException('Ошибка при назначении пикселя (%i, %i)'
                                   % (self.x, self.y))
            self.x += 1
        self.pos += 2

    def draw_8bit_pixels(self):
        """Рисует последовательность пикселей (для 8бит)"""
        length = self.rle_bytes[self.pos + 1]
        count = 0
        self.pos += 2
        while count < length:
            if self.in_bound() and self.pos < len(self.rle_bytes) \
                    and self.is_color(self.rle_bytes[self.pos]):
                self.pixels[self.y][self.x] = \
                    self.bmp.color_table[self.rle_bytes[self.pos]]
            else:
                raise RleException('Ошибка при назначении пикселя (%i, %i)'
                                   % (self.x, self.y))
            self.pos += 1
            self.x += 1
            count += 1
        if length % 2 == 1:
            self.pos += 1

    def in_bound(self):
        """Проверяет, что x и y не выходят за границы картинки"""
        return self.y < self.bmp.height and self.x < self.bmp.width

    def is_color(self, index):
        return len(self.bmp.color_table) > index

    def fill_4bit_pixels(self):
        """Заливает пиксели цветом в ячейке pos+1
        (первые 4 бита для первого пикселя,
        следующие для стоящего рядом пикселя) (для 4 бит)"""
        color1, color2 = self.get_4bit_colors(self.rle_bytes[self.pos + 1])
        for j in range(self.rle_bytes[self.pos]):
            if self.in_bound() and self.is_color(color1) \
                    and self.is_color(color2) \
                    and self.pos < len(self.rle_bytes):
                if j % 2 == 0:
                    self.pixels[self.y][self.x] = self.bmp.color_table[color1]
                else:
                    self.pixels[self.y][self.x] = self.bmp.color_table[color2]
            else:
                raise RleException('Ошибка при назначении пикселя (%i, %i)'
                                   % (self.x, self.y))
            self.x += 1
        self.pos += 2

    def draw_4bit_pixels(self):
        """Рисует последовательность пикселей (для 4бит)"""
        length = self.rle_bytes[self.pos + 1]
        count = 0
        self.pos += 2
        while count < length:
            color1, color2 = self.get_4bit_colors(self.rle_bytes[self.pos])
            if self.in_bound() and self.is_color(color1) \
                    and self.pos < len(self.rle_bytes):
                self.pixels[self.y][self.x] = self.bmp.color_table[color1]
            else:
                raise RleException('Ошибка при назначении пикселя (%i, %i)'
                                   % (self.x, self.y))
            self.x += 1
            count += 1
            self.pos += 1
            if count >= length:
                break
            if self.in_bound() and self.is_color(color2) \
                    and self.pos < len(self.rle_bytes):
                self.pixels[self.y][self.x] = self.bmp.color_table[color2]
            else:
                raise RleException('Ошибка при назначении пикселя (%i, %i)'
                                   % (self.x, self.y))
            self.x += 1
            count += 1
        if self.pos % 2 == 1:
            self.pos += 1

    def get_4bit_colors(self, byte):
        """Получает два цвета из байта [4 бита-col1|4бита-col2]"""
        binary = bin(byte)[2:]
        if len(binary) < 8:
            binary = '0' * (8 - len(binary)) + binary
        a = int(binary[:4], 2)
        b = int(binary[4:], 2)
        return a, b
