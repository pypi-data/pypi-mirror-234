import struct

class HiModuleHeader:
    def __init__(self):
        self.loaded = False
        self.Magic = ""
        self.Version = -1
        self.ModuleId = -1
        self.ModuleIntId = -1
        self.FilesCount = -1
        self.ManifestCount = -1
        self.unk0x18 = -1
        self.unk0x1C = -1
        self.ResourceIndex = -1
        self.StringsSize = -1
        self.ResourceCount = -1
        self.BlockCount = -1
        self.unk0x30 = -1
        self.unk0x34 = -1
        self.hd1_delta = -1
        self.data_size = -1
        self.unk0x44 = -1

        self.ResourceListOffset = -1
        self.ResourceListSize = -1
        self.ResourceListTypeSize = 4
        self.BlockListOffset = -1
        self.BlockListSize = -1
        self.BlockListTypeSize = 20
        self.FileDataOffset = -1

        self.DataOffset = -1
        
        self.FileEntrysOffset = (72)
        self.FileEntrysSize = -1
        self.FileEntrysTypeSize = (88)
        self.StringTableOffset = -1

    def readIn(self, f):
        # size 72 
        self.loaded = False
        f.seek(0)
        init_pos = f.tell()
        read_b = f.read(4)
        self.Magic =  struct.unpack('4s', read_b)[0] # 0 - 3 = 4
        self.Version = int.from_bytes(f.read(4), 'little', signed=True) # 4 - 7 = 8
        bytes_unk = f.read(8) # 8 - 15 = 16
        self.ModuleId = int.from_bytes(bytes_unk[0:8], 'little', signed=True)
        self.ModuleIntId = int.from_bytes(bytes_unk[0:4], 'little', signed=True)
        self.FilesCount = int.from_bytes(f.read(4), 'little', signed=True) # 16 - 19= 20
        self.ManifestCount = int.from_bytes(f.read(4), 'little', signed=True) # 20 - 23 = 24
        self.unk0x18 = int.from_bytes(f.read(4), 'little', signed=True) # 24 - 27 = 28
        self.unk0x1C = int.from_bytes(f.read(4), 'little', signed=True) # 28 - 31 = 32
        self.ResourceIndex = int.from_bytes(f.read(4), 'little', signed=True) # 32 - 35 = 36
        self.StringsSize = int.from_bytes(f.read(4), 'little', signed=True) # 36 - 39 = 40
        self.ResourceCount = int.from_bytes(f.read(4), 'little', signed=True) # 40 - 43 = 44
        self.BlockCount = int.from_bytes(f.read(4), 'little', signed=True) # 44 - 47 = 48
        self.unk0x30 = int.from_bytes(f.read(4), 'little', signed=True) # 48 - 51 = 52
        self.unk0x34 = int.from_bytes(f.read(4), 'little', signed=True) # 52 - 55 = 56
        self.hd1_delta = int.from_bytes(f.read(8), 'little', signed=True) # 56 - 63 = 64
        self.data_size = int.from_bytes(f.read(4), 'little', signed=True) # 64 - 67 = 68
        self.unk0x44 = int.from_bytes(f.read(4), 'little', signed=True) # 68 - 71 = 72
        self.size = f.tell() - init_pos
        if self.size != 72:
            print("error size")

        self.FileEntrysSize = (self.FilesCount * self.FileEntrysTypeSize)
        self.StringTableOffset = self.FileEntrysOffset + self.FileEntrysSize + 8   
        self.ResourceListOffset = (self.StringTableOffset + self.StringsSize) 
        self.ResourceListSize = (self.ResourceCount * 4)
        self.BlockListOffset = self.ResourceListOffset + self.ResourceListSize
        self.BlockListSize = self.BlockCount * self.BlockListTypeSize
        
        tmp = self.BlockListOffset + self.BlockListSize

        if (self.DataOffset & 0xfff) == 0:
            self.DataOffset = tmp
        else:
            self.DataOffset = (tmp & 0xfffffffffffff000) + 0x1000
              
        self.loaded = True