from .entries import Entry, FileEntry, DeletedEntry, DirEntry
from .long_name import LongName


class ClusteredFile:
    """Represent clustered file with entry and array of clusters"""

    def __init__(self, fs, entry):
        self.fs = fs
        self.entry = entry
        first_cluster = self.entry.first_cluster
        cluster_chain = self.fs.fat0.get_cluster_chain(first_cluster)
        self.clusters_numbers = list(cluster_chain)
        cluster_info_chain = fs.get_cluster_chain_info(self.clusters_numbers)
        self.fragments = [f for f in cluster_info_chain]
        self.position = 0
        if isinstance(self.entry, FileEntry):
            self.size = self.entry.file_size
        else:
            self.size = len(self.clusters_numbers) * fs.bpb.bytes_per_cluster

    def seek(self, offset):
        """Move reading cursor"""
        self.position = offset

    def read(self, count=None):
        """
        Return data from position to pos + count
        Might be slow on big count
        """
        if count is None:
            count = self.size
        remain = self.size - self.position
        count = min(count, remain)
        start = self.position
        end = start + count
        start_cluster = start // self.fs.bpb.bytes_per_cluster
        end_cluster = end // self.fs.bpb.bytes_per_cluster + 1
        data = b''
        for fragment in self.fragments[start_cluster:end_cluster]:
            skip = max(0, start - fragment.chain_offset_start)
            take = min(fragment.size, end - fragment.chain_offset_start - skip)
            position = fragment.offset + skip
            self.fs.raw_image.seek(position)
            data += self.fs.raw_image.read(take)
            self.seek(self.position + take)
        return data

    def read_all(self):
        """Yield all data that is contained in file"""
        for fragment in self.fragments:
            self.fs.raw_image.seek(fragment.offset)
            if fragment == self.fragments[len(self.fragments) - 1]:
                size = self.size % self.fs.bpb.bytes_per_cluster
                if size == 0:
                    size = self.fs.bpb.bytes_per_cluster
                yield self.fs.raw_image.read(size)
            else:
                yield self.fs.raw_image.read(self.fs.bpb.bytes_per_cluster)


class ClusteredDirectory(ClusteredFile):
    """
    Represent clustered directory, that contain entry of this
    dir and entries for subdirs and files, contained in this dir
    """

    def __init__(self, fs, entry):
        super().__init__(fs, entry)
        self.files_entries = []
        self.dirs_entries = []
        self.entries = self.read_entries()

    def read_entries(self):
        """
        Read entries of subdirs and files contained in folder
        """
        entries = []
        current_entry = 0
        entry_count = self.size / Entry.ENTRYLENGTH
        while current_entry < entry_count:
            entry = self.read_entry()
            if not entry:
                break
            current_entry += 1
            if isinstance(entry, LongName):
                longname, skipped_entries = self.generate_long_name(entry)
                entry = self.read_entry()
                entry.long_name = longname
                current_entry += skipped_entries
            entries.append(entry)
            if isinstance(entry, FileEntry):
                self.files_entries.append(entry)
            if isinstance(entry, DirEntry):
                self.dirs_entries.append(entry)
        return entries

    def generate_long_name(self, entry):
        """
        Generate long name of entry
        """
        long_name_list = []
        long_name_list.append(entry)
        for j in range(long_name_list[0].get_sequence_number() - 1):
            long_name_list.append(self.read_entry())
        result = ''
        for name_part in long_name_list[::-1]:
            result += name_part.get_name()
        return result, long_name_list[0].get_sequence_number()

    def read_entry(self):
        """
        Determine type of entry and return it
        """
        raw = self.read(32)
        attributes = raw[11]
        if raw[0] == 0:
            return None
        elif raw[0] == 0xE5:
            return DeletedEntry(raw)
        elif attributes == Entry.LONGFILENAME:
            return LongName(raw)
        elif attributes & Entry.DIRECTORY:
            return DirEntry(raw)
        else:
            return FileEntry(raw)


class ClusterInfo:
    """Represent info about sector"""

    def __init__(self, number, offset, size, chain_offset=0):
        self.number = number
        self.offset = offset
        self.size = size
        self.chain_offset_start = chain_offset
        self.chain_offset_end = chain_offset + size

    def in_range(self, start, end):
        return self.chain_offset_start <= start and \
            end <= self.chain_offset_end
