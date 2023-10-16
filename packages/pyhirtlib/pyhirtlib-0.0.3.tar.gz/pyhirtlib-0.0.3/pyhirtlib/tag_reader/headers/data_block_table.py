import struct

class DataBlock:

    def __init__(self):
        self.section = -1
        self.offset = -1
        self.size = -1
        self.unknown_property = -1
        self.offset_plus = -1

    def readIn(self, f, header):
        self.size = struct.unpack('i', f.read(4))[0]
        self.unknown_property = struct.unpack('H', f.read(2))[0]  # only change in render_model
        self.section = struct.unpack('H', f.read(2))[0]
        self.offset = struct.unpack('Q', f.read(8))[0]
        if self.section == 1:
            self.offset_plus = self.offset + header.header_size
        elif self.section == 2:
            self.offset_plus = self.offset + header.header_size + header.data_size
        elif self.section == 3:
            self.offset_plus = self.offset + header.header_size + header.data_size + header.resource_data_size
        else:
            debug = True

        
        if self.unknown_property !=0:
            debug = True
            header.data_reference_count


        
        



class DataBlockTable:

    def __init__(self):
        self.entries = []
        pass

    def readTable(self, f, header):
        f.seek(header.data_block_offset)
        for x in range(header.data_block_count):
            entry = DataBlock()
            entry.readIn(f, header)
            if entry.section == 1:
                entry.offset_plus = entry.offset + header.header_size
            elif entry.section == 2:
                entry.offset_plus = entry.offset + header.header_size + header.data_size
            elif entry.section == 3:
                entry.offset_plus = entry.offset + header.header_size + header.data_size + header.resource_data_size
            else:
                debug = True
            self.entries.append(entry)
        return
