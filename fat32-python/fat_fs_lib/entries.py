from .fat_time import FATDateTime
from .misc import int_from_bytes


class Entry:
    """Represent entry of clustered file"""
    READONLY = 0x01
    HIDDEN = 0x02
    SYSTEM = 0x04
    LABEL = 0x08
    DIRECTORY = 0x10
    ARCHIVE = 0x20
    LONGFILENAME = READONLY | HIDDEN | SYSTEM | LABEL
    ENTRYLENGTH = 32

    def __init__(self, raw_bytes):
        self.raw = raw_bytes
        self.name = raw_bytes[0:11]
        self.attributes = raw_bytes[11]
        self.nt_res = raw_bytes[12]
        self.current_time = raw_bytes[13]
        self.creating_time = raw_bytes[14:16]
        self.creating_date = raw_bytes[16:18]
        self.last_access_date = raw_bytes[18:20]
        self.first_cluster_high = int_from_bytes(self.raw, 20, 22)
        self.write_time = raw_bytes[22:24]
        self.write_date = raw_bytes[24:26]
        self.first_cluster_low = int_from_bytes(self.raw, 26, 28)
        self.first_cluster = self.get_first_cluster()
        self.file_size = int_from_bytes(self.raw, 28, 32)
        self.long_name = None
        self.creating_dt = self.create_date_stamps(self.creating_time,
                                                   self.creating_date)
        self.write_dt = self.create_date_stamps(self.write_time,
                                                self.write_time)

    def create_date_stamps(self, time_bytes, date_bytes):
        """
        Create python datetime for write time and read time
        """
        if time_bytes != b'\x00\x00' and date_bytes != b'\x00\x00' \
                and not self.is_label() and not self.is_long_file_name():
            return FATDateTime(self.creating_time, self.creating_date).dt
        else:
            return None

    def is_readonly(self):
        return bool(self.attributes & Entry.READONLY)

    def is_hidden(self):
        return bool(self.attributes & Entry.HIDDEN)

    def is_system(self):
        return bool(self.attributes & Entry.SYSTEM)

    def is_label(self):
        return bool(self.attributes & Entry.LABEL)

    def is_dir(self):
        return bool(self.attributes & Entry.DIRECTORY)

    def is_archive(self):
        return bool(self.attributes & Entry.ARCHIVE)

    def is_long_file_name(self):
        return bool(self.attributes == Entry.LONGFILENAME)

    def is_deleted(self):
        return self.name[0] == 0xE5

    def get_first_cluster(self):
        return self.first_cluster_high << 16 | self.first_cluster_low

    def get_name(self):
        """
        Return long name (if entry contain long name)
        or dos name
        """
        if self.long_name:
            return self.long_name
        else:
            return self.get_dos_name()

    def get_dos_name(self):
        """
        Return fancy represent of dos name (8.3 for files)
        """
        if isinstance(self, DeletedEntry):
            return ''
        name = self.name[:8].decode('ascii').strip().lower()
        if not self.is_dir():
            extension = '.' + self.name[8:11].decode('ascii').strip().lower()
        else:
            extension = ''
        return name + extension


class DeletedEntry(Entry):
    pass


class FileEntry(Entry):
    pass


class DirEntry(Entry):
    pass
