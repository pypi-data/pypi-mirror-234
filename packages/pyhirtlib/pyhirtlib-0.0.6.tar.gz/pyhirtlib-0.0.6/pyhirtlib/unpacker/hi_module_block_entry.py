class HiModuleBlockEntry:
    def __init__(self):
        self.loaded = False
        self.comp_offset = -1
        self.comp_size = -1
        self.decomp_offset = -1
        self.decomp_size = -1
        self.b_compressed = False

    def readIn(self, f):
        # size 20 
        self.loaded = False
        init_pos = f.tell()
        self.comp_offset = int.from_bytes(f.read(4), 'little', signed=True) # 0-3 -> 4
        self.comp_size = int.from_bytes(f.read(4), 'little', signed=True) # 4-7 -> 8
        self.decomp_offset = int.from_bytes(f.read(4), 'little', signed=True) # 8-11 -> 12
        self.decomp_size = int.from_bytes(f.read(4), 'little', signed=True) # 12-15 -> 16
        self.b_compressed = int.from_bytes(f.read(4), 'little', signed=False) == 1 # 16-19 -> 20
        self.size = f.tell() - init_pos
        if self.size!= 20:
            print("error size")
        self.loaded = True