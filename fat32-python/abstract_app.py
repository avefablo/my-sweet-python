from fat_fs_lib.entries import DirEntry, FileEntry
from fat_fs_lib.directory import ClusteredFile, ClusteredDirectory
from fat_fs_lib.fat_fs import FatFs


class AbstractApplication:
    def __init__(self, image):
        self.raw = image
        self.fat32_image = FatFs(self.raw)
        self.pwd_entry = self.fat32_image.get_root()

    def save(self, entry):
        """
        Function that saves files to dir "saved"
        """
        input_file = ClusteredFile(self.fat32_image, entry)
        output_file = open('saved/%s' % entry.get_name(), 'wb+')
        saved_fragments_count = 0
        total_fragments = len(input_file.fragments)
        for fragment in input_file.read_all():
            output_file.write(fragment)
            saved_fragments_count += 1
            yield self.get_percentage(saved_fragments_count,
                                      total_fragments)

    def get_percentage(self, saved, total):
        """Return percentage of already copied data"""
        return int(saved / total * 100)

    def cat(self, entry):
        file = ClusteredFile(self.fat32_image, entry)
        for fragment in file.read_all():
            yield str(fragment)[2:-1]

    def cd(self, entry):
        self.pwd_entry = ClusteredDirectory(self.fat32_image, entry)
        if self.pwd_entry.entry.first_cluster == 0:
            self.pwd_entry = self.fat32_image.get_root()

    def ls(self, entries):
        for entry in entries:
            if type(entry) in {FileEntry, DirEntry}:
                yield entry
