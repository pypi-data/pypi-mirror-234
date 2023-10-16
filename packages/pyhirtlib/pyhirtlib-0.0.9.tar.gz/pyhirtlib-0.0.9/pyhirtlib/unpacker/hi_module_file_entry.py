import struct

class HiModuleFileEntry:
    # size 88
    def __init__(self):
        self.loaded = False
        self.index = -1
        self.resource_count = -1
        self.parent_file_index = -1
        self.unk0x08 = -1
        self.block_count = -1
        self.first_block_index = -1
        self.first_resource_index = -1
        self.tag = ""
        self.tagGroupRev = ""
        self.local_data_offset = -1
        self.flags = -1
        self.comp_size = -1
        self.decomp_size = -1
        self.GlobalTagId = -1
        self.UncompressedHeaderSize = -1
        self.UncompressedTagDataSize = -1
        self.UncompressedResourceDataSize = -1
        self.HeaderBlockCount = -1
        self.TagDataBlockCount = -1
        self.ResourceBlockCount = -1
        self.ResourceBlockCountPad = -1
        self.string_offset = -1
        self.parent_of_resource = -1
        self.hash = -1
        self.size = -1

        self.InModuleDataOffset = -1

    def readIn(self, f):
        # size 88 
        self.loaded = False
        init_pos = f.tell()
        self.resource_count = int.from_bytes(f.read(4), 'little', signed=True) # 0-3 -> 4
        self.parent_file_index = int.from_bytes(f.read(4), 'little', signed=True) # 4-7 -> 8
        self.unk0x08 = int.from_bytes(f.read(2), 'little', signed=True) # 8-9 -> 10
        self.block_count = int.from_bytes(f.read(2), 'little', signed=True) # 10-11 -> 12
        self.first_block_index = int.from_bytes(f.read(4), 'little', signed=True) # 12-15 -> 16
        self.first_resource_index = int.from_bytes(f.read(4), 'little', signed=True) # 16-19 -> 20
        self.tag = struct.unpack('4s', f.read(4))[0] # 20-23 -> 24
        if self.tag != b'\xff\xff\xff\xff':
            self.tagGroupRev = self.tag[::-1].decode("utf-8")
        self.local_data_offset = int.from_bytes(f.read(6), 'little', signed=True) # 24-29 -> 30
        self.flags = int.from_bytes(f.read(2), 'little', signed=True) # 30-31 -> 32
        self.comp_size = int.from_bytes(f.read(4), 'little', signed=True) # 32-35 -> 36
        self.decomp_size = int.from_bytes(f.read(4), 'little', signed=True) # 36-39 -> 40
        self.GlobalTagId = int.from_bytes(f.read(4), 'little', signed=True) # 40-43 -> 44
        self.UncompressedHeaderSize = int.from_bytes(f.read(4), 'little', signed=True) # 44-47 -> 48
        self.UncompressedTagDataSize = int.from_bytes(f.read(4), 'little', signed=True) # 48-51 -> 52
        self.UncompressedResourceDataSize = int.from_bytes(f.read(4), 'little', signed=True) # 52-55 -> 56
        self.HeaderBlockCount = int.from_bytes(f.read(2), 'little', signed=True) # 56-57 -> 58
        self.TagDataBlockCount = int.from_bytes(f.read(2), 'little', signed=True) # 58-59 -> 60
        self.ResourceBlockCount = int.from_bytes(f.read(2), 'little', signed=True) # 60-61 -> 62
        self.ResourceBlockCountPad = int.from_bytes(f.read(2), 'little', signed=True) # 62-63 -> 64
        self.string_offset = int.from_bytes(f.read(4), 'little', signed=True) # 64-67 -> 68
        self.parent_of_resource = int.from_bytes(f.read(4), 'little', signed=True) # 68-71 -> 72
        self.hash = f.read(16) # 72-87 -> 88
        self.size = f.tell() - init_pos
        if self.size!= 88:
            print("error size")
        self.loaded = True

        
