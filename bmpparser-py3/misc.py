class Pixel:
    """Представление пикселя RGBA"""
    def __init__(self, red, green, blue, alpha=255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __repr__(self):
        return "({} {} {})".format(self.red, self.green, self.blue)


class Mask:
    """Маска каналов"""
    def __init__(self, hex_mask, bits):
        self.mask = hex_mask
        self.bits = bits
        self.shift = self.least_sign_bit(self.mask) - 1
        self.width = self.most_sign_bit(self.mask) - self.shift

    def least_sign_bit(self, mask):
        """Получает младший значащий бит"""
        shift = 1
        if not mask:
            return shift
        while mask and mask & 0x01 == 0:
            mask >>= 1
            shift += 1
        return shift

    def most_sign_bit(self, mask):
        """Получает старший значащий бит"""
        if not mask:
            return 0
        shift = self.bits
        while mask and mask & 2 ** (self.bits - 1) == 0:
            mask <<= 1
            shift -= 1
        return shift


def int_from_bytes(raw_bytes, start, end):
    """Возвращает число от байтов с byteorder=little"""
    return int.from_bytes(raw_bytes[start:end], byteorder='little')
