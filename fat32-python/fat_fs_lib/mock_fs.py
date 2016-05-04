class MockFs:
    """Сделал образ диска и сдампил его.
    Посмотрел по каким адресам лежат данные и сделал Mock"""
    FAT0_OFFSET = 16384
    FAT1_OFFSET = 1967616
    BPB_OFFSET = 0
    DATA_OFFSET_DIFFERENCE = 3918848

    def __init__(self):
        self.pos = 0
        self.current_file = open('mock/bpb', 'rb')
        self.is_data = None

    def read(self, count):
        self.current_file.seek(self.pos)
        data = self.current_file.read(count)
        self.pos += count
        return data

    def seek(self, pos):
        if pos == self.BPB_OFFSET:
            self.change_file('bpb')
        elif pos == self.FAT0_OFFSET:
            self.change_file('fat0')
        elif pos == self.FAT1_OFFSET:
            self.change_file('fat1')
        else:
            if not self.is_data:
                self.is_data = True
                self.change_file('data')
            self.pos = pos - self.DATA_OFFSET_DIFFERENCE

    def change_file(self, name):
        self.current_file.close()
        self.current_file = open('mock/%s' % name, 'rb')
        self.pos = 0

    def close(self):
        self.current_file.close()
