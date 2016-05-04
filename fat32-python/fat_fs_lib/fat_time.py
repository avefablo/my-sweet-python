import datetime


class FATDateTime:
    """Represent datetime for FAT"""

    def __init__(self, byte_time, byte_date):
        bin_date = bin(int.from_bytes(byte_date, byteorder='little'))[2:]
        bin_date = bin_date.zfill(16)

        year = 1980 + int(bin_date[0:7], 2)
        month = int(bin_date[7:11], 2)
        day = int(bin_date[11:16], 2)

        bin_time = bin(int.from_bytes(byte_time, byteorder='little'))[2:]
        bin_time = bin_time.zfill(16)

        hours = int(bin_time[0:5], 2)
        minutes = int(bin_time[5:11], 2)
        seconds = int(bin_time[11:16], 2) * 2

        self.dt = datetime.datetime(year, month, day, hours, minutes, seconds)
