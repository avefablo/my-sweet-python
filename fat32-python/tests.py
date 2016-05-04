import unittest

from fat_fs_lib.directory import ClusteredDirectory, ClusteredFile
from fat_fs_lib.fat_fs import FatFs
from fat_fs_lib.mock_fs import MockFs
from fat_fs_lib.entries import Entry

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = FatFs(MockFs())

    def test_jmp_boot(self):
        self.assertEqual(self.image.bpb.jmp_boot, b"\xebX\x90")

    def test_oem_name(self):
        self.assertEqual(self.image.bpb.oem_name, 'mkfs.fat')

    def test_bytes_per_sector(self):
        self.assertEqual(self.image.bpb.bytes_per_sector, 512)

    def test_sectors_per_cluster(self):
        self.assertEqual(self.image.bpb.sectors_per_cluster, 8)

    def test_reserved_sectors_count(self):
        self.assertEqual(self.image.bpb.reserved_sectors_count, 32)

    def test_number_of_fats(self):
        self.assertEqual(self.image.bpb.number_of_fats, 2)

    def test_root_entry_count(self):
        self.assertEqual(self.image.bpb.root_entry_count, 0)

    def test_total_sectors_16(self):
        self.assertEqual(self.image.bpb.total_sectors_16, 0)

    def test_media(self):
        self.assertEqual(self.image.bpb.media, 248)

    def test_fat_size_16(self):
        self.assertEqual(self.image.bpb.fat_size_16, 0)

    def test_sectors_per_track(self):
        self.assertEqual(self.image.bpb.sectors_per_track, 16)

    def test_num_heads(self):
        self.assertEqual(self.image.bpb.num_heads, 4)

    def test_hidden_sectors(self):
        self.assertEqual(self.image.bpb.hidden_sectors, 2048)

    def test_total_sectors_32(self):
        self.assertEqual(self.image.bpb.total_sectors_32, 3909632)

    def test_fat_size_32(self):
        self.assertEqual(self.image.bpb.fat_size_32, 3811)

    def test_ext_flags(self):
        self.assertEqual(self.image.bpb.ext_flags, 0)

    def test_fs_version(self):
        self.assertEqual(self.image.bpb.fs_version, 0)

    def test_root_cluster(self):
        self.assertEqual(self.image.bpb.root_cluster, 2)

    def test_fs_info(self):
        self.assertEqual(self.image.bpb.fs_info, 1)

    def test_bk_boot_sector(self):
        self.assertEqual(self.image.bpb.bk_boot_sector, 6)

    def test_reserved(self):
        self.assertEqual(self.image.bpb.reserved, 0)

    def test_drv_num(self):
        self.assertEqual(self.image.bpb.drv_num, 128)

    def test_reserved1(self):
        self.assertEqual(self.image.bpb.reserved1, 1)

    def test_boot_sig(self):
        self.assertEqual(self.image.bpb.boot_sig, 41)

    def test_volume_id(self):
        self.assertEqual(self.image.bpb.volume_id, 3172229886)

    def test_volume_label(self):
        self.assertEqual(self.image.bpb.volume_label, 'NO NAME    ')

    def test_fs_type(self):
        self.assertEqual(self.image.bpb.fs_type, 'FAT32   ')

    def test_first_data_sector(self):
        self.assertEqual(self.image.bpb.first_data_sector, 7654)

    def test_bytes_per_cluster(self):
        self.assertEqual(self.image.bpb.bytes_per_cluster, 4096)

    def test_fat_offset(self):
        self.assertEqual(self.image.fat0.get_fat_offset(0), 16384)

    def test_fat_length(self):
        self.assertEqual(self.image.fat0.get_length(), 1951232)

    def test_root(self):
        r = self.image.get_root()
        dirs = r.dirs_entries
        self.assertTrue(len(dirs) == 3)

    def test_root_names(self):
        r = self.image.get_root()
        dirs = [entry.get_name() for entry in r.entries]
        self.assertTrue("java" in dirs)
        self.assertTrue("python" in dirs)
        self.assertTrue("longdirnameawesome" in dirs)

    def test_sub_folder(self):
        r = self.image.get_root()
        dirs = r.entries
        subdir_entry = next(my_dir for my_dir in dirs
                            if my_dir.get_name() == 'java')
        subdir = ClusteredDirectory(self.image, subdir_entry)
        files = [entry.get_name() for entry in subdir.entries]
        self.assertTrue("PolishNotationParser.java" in files)

    def test_contained_file(self):
        r = self.image.get_root()
        dirs = r.entries
        subdir_entry = next(dir for dir in dirs if dir.get_name() == 'java')
        subdir = ClusteredDirectory(self.image, subdir_entry)
        requied_file_entry = next(entry for entry in subdir.entries
                                  if entry.get_name() ==
                                  "PolishNotationParser.java")
        requied_file = ClusteredFile(self.image,
                                     requied_file_entry)
        data = requied_file.read()
        with open('mock/PolishNotationParser.java', 'rb') as actual_file:
            actual_data = actual_file.read()
        self.assertEqual(data, actual_data)

    def test_contained_big_file(self):
        r = self.image.get_root()
        dirs = r.entries
        name = "08 Vilaines filles, mauvais garçons.mp3"
        subdir_entry = next(my_dir for my_dir in dirs if my_dir.get_name()
                            == "longdirnameawesome")
        subdir = ClusteredDirectory(self.image, subdir_entry)
        requied_file_entry = next(entry for entry in subdir.entries
                                  if entry.get_name() == name)
        requied_file = ClusteredFile(self.image,
                                     requied_file_entry)
        data = requied_file.read()
        with open('mock/' + name, 'rb') as actual_file:
            actual_data = actual_file.read()
        self.assertEqual(data, actual_data)

    def test_entry(self):
        r = self.image.get_root()
        dirs = r.entries
        subdir_entry = next(dir for dir in dirs if dir.get_name() == 'java')
        subdir = ClusteredDirectory(self.image, subdir_entry)
        requied_file_entry = next(entry for entry in subdir.entries
                                  if entry.get_name() ==
                                  "PolishNotationParser.java")
        self.assertFalse(requied_file_entry.is_dir())
        self.assertTrue(requied_file_entry.is_archive())
        self.assertFalse(requied_file_entry.is_deleted())
        self.assertFalse(requied_file_entry.is_hidden())
        self.assertFalse(requied_file_entry.is_readonly())
        self.assertFalse(requied_file_entry.is_system())
        self.assertEqual(requied_file_entry.get_name(),
                         "PolishNotationParser.java")
        self.assertEqual(requied_file_entry.get_dos_name(),
                         "polish~1.jav")


if __name__ == '__main__':
    unittest.main()
