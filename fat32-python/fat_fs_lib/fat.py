class FAT:
    """
    Represent File Allocation Table
    """

    def __init__(self, image, number):
        super().__init__()
        self.image = image
        self.offset = self.get_fat_offset(number)
        self.length = self.get_length()
        self.image.raw_image.seek(self.offset)
        self.media_descriptor = self.image.raw_image.read(1)
        self.image.raw_image.read(3)
        self.eoc = self.image.raw_image.read(4)
        self.cluster_pairs = {}
        self.bad_clusters = {}
        for i in range(2, self.length // 4):
            cluster = int.from_bytes(self.image.raw_image.read(4),
                                     byteorder='little')
            if not cluster:
                continue
            elif self.is_cluster_value_valid(cluster):
                self.cluster_pairs[i] = cluster
            elif self.is_cluster_bad(cluster):
                self.bad_clusters[i] = cluster
            elif self.is_cluster_final(cluster):
                self.cluster_pairs[i] = None
        if self.bad_clusters:
            print("There are %i bad clusters." % len(self.bad_clusters))

    def is_cluster_value_valid(self, cl_val):
        """True if cluster isn't eoc or bad"""
        return 0x00000002 <= cl_val <= 0x0FFFFFEF

    def is_cluster_final(self, cl_val):
        """True if eoc"""
        return 0x0FFFFFF8 <= cl_val <= 0x0FFFFFFF

    def is_cluster_bad(self, cl_val):
        """True if sector is bad"""
        return cl_val == 0x0FFFFFF7

    def get_length(self):
        """Return length of fat"""
        return self.image.bpb.fat_size_32 * self.image.bpb.bytes_per_sector

    def get_fat_offset(self, n):
        """Return offset of fat number n from start of file"""
        offset = self.image.bpb.reserved_sectors_count * \
            self.image.bpb.bytes_per_sector
        fat_size = self.image.bpb.fat_size_32 * self.image.bpb.bytes_per_sector
        offset += n * fat_size
        return offset

    def get_cluster_chain(self, cluster):
        """Yield chain of clusters for file"""
        while cluster:
            yield cluster
            cluster = self.cluster_pairs[cluster]
