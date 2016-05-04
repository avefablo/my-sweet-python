from .misc import int_from_bytes


class BiosParameterBlock:
    """Represent BIOS Parameter Block"""

    def __init__(self, raw_bytes):
        self.raw_bytes = raw_bytes
        self.jmp_boot = raw_bytes[0:3]
        self.oem_name = raw_bytes[3:11].decode('utf-8')
        self.bytes_per_sector = int_from_bytes(raw_bytes, 11, 13)
        self.sectors_per_cluster = int_from_bytes(raw_bytes, 13, 14)
        self.reserved_sectors_count = int_from_bytes(raw_bytes, 14, 16)
        self.number_of_fats = int_from_bytes(raw_bytes, 16, 17)
        self.root_entry_count = int_from_bytes(raw_bytes, 17, 19)
        self.total_sectors_16 = int_from_bytes(raw_bytes, 19, 21)
        self.media = int_from_bytes(raw_bytes, 21, 22)
        self.fat_size_16 = int_from_bytes(raw_bytes, 22, 24)
        self.sectors_per_track = int_from_bytes(raw_bytes, 24, 26)
        self.num_heads = int_from_bytes(raw_bytes, 26, 28)
        self.hidden_sectors = int_from_bytes(raw_bytes, 28, 32)
        self.total_sectors_32 = int_from_bytes(raw_bytes, 32, 36)
        self.fat_size_32 = int_from_bytes(raw_bytes, 36, 40)
        self.ext_flags = int_from_bytes(raw_bytes, 40, 42)
        self.fs_version = int_from_bytes(raw_bytes, 42, 44)
        self.root_cluster = int_from_bytes(raw_bytes, 44, 48)
        self.fs_info = int_from_bytes(raw_bytes, 48, 50)
        self.bk_boot_sector = int_from_bytes(raw_bytes, 50, 52)
        self.reserved = int_from_bytes(raw_bytes, 52, 64)
        self.drv_num = int_from_bytes(raw_bytes, 64, 65)
        self.reserved1 = int_from_bytes(raw_bytes, 65, 66)
        self.boot_sig = int_from_bytes(raw_bytes, 66, 67)
        self.volume_id = int_from_bytes(raw_bytes, 67, 71)
        self.volume_label = raw_bytes[71:82].decode('utf-8')
        self.fs_type = raw_bytes[82:90].decode('utf-8')
        self.first_data_sector = self.get_first_data_sector()
        self.bytes_per_cluster = self.get_bytes_by_cluster()

    def get_first_data_sector(self):
        """Return first sector, that contains data"""
        return self.reserved_sectors_count +\
            self.number_of_fats * self.fat_size_32

    def get_bytes_by_cluster(self):
        """Return amount of bytes in one cluster"""
        return self.sectors_per_cluster * self.bytes_per_sector
