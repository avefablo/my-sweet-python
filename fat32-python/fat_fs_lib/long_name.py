class LongName:
    """Represent long name"""
    LAST = 0x40
    NUL = b'\0\0'

    def __init__(self, raw):
        self.raw = raw
        self.sequence_ord = int.from_bytes(raw[0:1], byteorder='little')
        self.name1 = raw[1:11]
        self.attr = raw[11:12]
        self.type = raw[12:13]
        self.chksum = raw[13:14]
        self.name2 = raw[14:26]
        self.first_clus_LO = raw[26:28]
        self.name3 = raw[28:32]

    def is_last(self):
        """True if this is the last part of long name"""
        return self.sequence_ord & self.LAST

    def get_sequence_number(self):
        """Return number of parts"""
        return self.sequence_ord ^ self.LAST

    def get_name(self):
        """Concatenate name by parts"""
        result = self.name1 + self.name2 + self.name3
        if self.NUL in result:
            result = result.rpartition(self.NUL)[0]
        return result.decode('utf-16')
