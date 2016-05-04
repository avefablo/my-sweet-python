from .bpb import BiosParameterBlock
from .directory import ClusterInfo, ClusteredDirectory
from .entries import Entry
from .fat import FAT


class FatFs:
    """Represent FAT FileSystem"""
    def __init__(self, raw):
        self.raw_image = raw
        bpb_bytes = self.raw_image.read(90)
        self.bpb = BiosParameterBlock(bpb_bytes)
        self.fat0 = FAT(self, 0)
        self.fat1 = FAT(self, 1)

    def get_first_data_sector(self):
        """Return first sector that contain data"""
        return self.bpb.reserved_sectors_count + \
            self.bpb.number_of_fats * self.bpb.fat_size_32

    def get_first_sector_of_cluster(self, cluster_num):
        """Return first sector of cluster"""
        return (cluster_num - 2) * self.bpb.sectors_per_cluster + \
            self.get_first_data_sector()

    def get_first_byte_of_sector(self, sec_num):
        """Return first sector of sector"""
        return sec_num * self.bpb.bytes_per_sector

    def get_cluster_chain_info(self, clusters):
        """Yield chain of cluster info"""
        chain_offset = 0
        for cluster_num in clusters:
            sector_num = self.get_first_sector_of_cluster(cluster_num)
            offset = self.get_first_byte_of_sector(sector_num)
            yield ClusterInfo(cluster_num, offset,
                              self.bpb.bytes_per_cluster,
                              chain_offset)
            chain_offset += self.bpb.bytes_per_cluster

    def get_root(self):
        """Return root directory"""
        root_sec = self.get_first_sector_of_cluster(self.bpb.root_cluster)
        start_root = self.get_first_byte_of_sector(root_sec)
        self.raw_image.seek(start_root)
        root_entry = Entry(self.raw_image.read(Entry.ENTRYLENGTH))
        root_entry.first_cluster = self.bpb.root_cluster
        return ClusteredDirectory(self, root_entry)
