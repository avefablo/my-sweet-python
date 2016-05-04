class BMPFile:
    """Представляет собой BMP файл, состоящий из потока байтов,
    имени файла и отступа до заголовка BMP"""

    def __init__(self, raw, offset, filename):
        self.raw_bytes = raw
        self.bf_offset = offset
        self.filename = filename

    def print_info(self):
        """Печатает информацию о файле"""
        print("Offset:\t{}".format(self.bf_offset))


class ValidationError(Exception):
    pass
