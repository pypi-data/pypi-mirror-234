from unpacker.hi_module_block_entry import HiModuleBlockEntry
from unpacker.hi_module_file_entry import HiModuleFileEntry
from unpacker.hi_module_header import HiModuleHeader
from unpacker.oodle_decompressor import InstanceOodle, OodleDecompressor


class HiModule:
    def __init__(self, path_file: str):
        self.path_file = path_file
        self.loaded = False 
        self.moduleHeader = HiModuleHeader()
        self.hiModuleFileEntries = {}
        self.blocks = {}
        self.hd1Handle = None
        self.decompressor :OodleDecompressor = None 
    
    def readIn(self):
        f = open(self.path_file, 'rb')
        self.__readIn(f)
        f.close()

    def __readIn(self, f):
        # size ?
        self.loaded = False
        self.moduleHeader.readIn(f)
        self.loaded = True

    def readFileEntry(self, index=-1) -> HiModuleFileEntry:
        f = open(self.path_file,  'rb')
        result = self.__readFileEntry(f,index)
        f.close()
        return result

    def __readFileEntry(self, f, index=-1) -> HiModuleFileEntry:
        if index<-1 or index>= self.moduleHeader.FilesCount:
            return None
        index_z = -1
        if index == -1:
            actual_pos = f.tell()
            dif = actual_pos - self.moduleHeader.FileEntrysOffset
            if dif<0:
                return None
            
            count = divmod(self.moduleHeader.FileEntrysSize, dif)
            if count[1] != 0:
                return None
            index_z = count[0]
        else:
            index_z = index
        
        if self.hiModuleFileEntries.keys().__contains__(index_z):
            return self.hiModuleFileEntries[index_z]
        
        init_pos = 72 + index_z * 88
        f.seek(init_pos)
        tempFileEntry = HiModuleFileEntry()
        tempFileEntry.readIn(f)
        tempFileEntry.index = index_z
        self.hiModuleFileEntries[index_z] = tempFileEntry
        return tempFileEntry

    def __readBlockEntryIn(self, f, index=-1)->HiModuleBlockEntry:
        if index<-1 or index>= self.moduleHeader.BlockCount:
            return None
        index_z = -1
        if index == -1:
            actual_pos = f.tell()
            dif = actual_pos - self.moduleHeader.BlockListOffset
            if dif<0:
                return None
            
            count = divmod(self.moduleHeader.BlockListSize, dif)
            if count[1] != 0:
                return None
            index_z = count[0]
        else:
            index_z = index
        
        if self.blocks.keys().__contains__(index_z):
            return self.blocks[index_z]
        if (index_z != -1):
            init_pos = self.moduleHeader.BlockListOffset + (index_z * self.moduleHeader.BlockListTypeSize)
            f.seek(init_pos)
        entry = HiModuleBlockEntry()
        entry.readIn(f)
        self.blocks[index_z] = entry
        return entry

    def __GetHd1Handle(self):
        try:
            self.hd1Handle = open(self.path_file + "_hd1", 'rb')
        except:
            self.hd1Handle = None

    def readFileEntryUnPackedBytes(self, file_entry:HiModuleFileEntry):
        f = open(self.path_file,  'rb')
        result = self.__readFileEntryUnPackedBytes(f,file_entry)
        f.close()
        return result
        
    def __readFileEntryUnPackedBytes(self, f, file_entry:HiModuleFileEntry):
        handle = f
        offset = file_entry.local_data_offset
        decomp_save_data = b""
        if self.moduleHeader.Version >= 0x34:
            if (file_entry.flags & 1) != 0:
                if self.hd1Handle is None:
                    self.__GetHd1Handle()
                if self.hd1Handle is None:
                    print( "Error extracting , no hd1 file for module ")
                    return decomp_save_data
                offset -= self.moduleHeader.hd1_delta
                handle = self.hd1Handle
            else:
                offset += self.moduleHeader.DataOffset
        else:
            offset += self.moduleHeader.DataOffset
            if (file_entry.flags & 1) != 0:
                if self.hd1Handle is None:
                    self.__GetHd1Handle()
                if self.hd1Handle is None:
                    print( "Error extracting , no hd1 file for module ")
                    return decomp_save_data
                offset -= self.moduleHeader.hd1_delta
                handle = self.hd1Handle


        file_entry.InModuleDataOffset = offset
        if (file_entry.decomp_size == 0):
            return decomp_save_data
        
        if file_entry.block_count !=0:
            for i in range(file_entry.first_block_index,file_entry.first_block_index+file_entry.block_count):
                block = self.__readBlockEntryIn(f,i)
                if block.b_compressed:
                    handle.seek(offset + block.comp_offset)
                    data = handle.read(block.comp_size)
                    if  self.decompressor is None:
                        self.decompressor = InstanceOodle.get()
                    decomp = self.decompressor.decompress(data, block.decomp_size)

                    if len(decomp_save_data) != block.decomp_offset:
                        raise Exception("Skipped data fix")
                    if decomp == False:
                        decomp_save_data += b"\0" * block.decomp_size
                        raise Exception("Warning: failed to decompress block in file: ")
                    else:
                        decomp_save_data += decomp
                else:
                    handle.seek(offset + block.comp_offset)
                    decomp = handle.read(block.comp_size)
                    if len(decomp_save_data) != block.decomp_offset:
                        raise Exception("Skipped data fix")
                    decomp_save_data += decomp
        else:
            handle.seek(offset)
            if file_entry.comp_size == file_entry.decomp_size:
                decomp_save_data = handle.read(file_entry.comp_size)
                #print(t1e.save_path)
            else:
                if  self.decompressor is None:
                        self.decompressor = InstanceOodle.get()
                decomp_save_data = self.decompressor.decompress(handle.read(file_entry.comp_size), file_entry.decomp_size)
                comp_save_data = self.decompressor.compress(decomp_save_data, len(decomp_save_data))
        
        return decomp_save_data        



