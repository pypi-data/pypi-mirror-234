import struct
import xml.etree.ElementTree as ET

from commons.exception.read_tag_struct_exception import ReadTagStructException
from commons.logs import Log
from events import Event
from tag_reader.headers.data_block_table import DataBlock
from tag_reader.tag_element_type  import TagStructType


class TagStructInfo:
    def __init__(self):
        self.property_address = 0
        self.n_childs = -1
        self.child_data_size = 0
        self.childs_data_start_address = 0

class TagStruct:

    def __init__(self):
        self.onDataRead = Event()
        # self.hash = GUID()
        self.info : TagStructInfo= None
        self.GUID = ''
        self.GUID1 = ''
        self.GUID2 = ''
        self.type_id = -1
        self.type_id_tg: TagStructType = -1
        self.unknown_property_bool_0_1 = -1
        #self.target_index = -1
        self.field_data_block_index = -1
        # self.field_block = -1
        self.parent_field_data_block_index = -1
        self.field_offset = -1
        #self.data_reference: DataBlock = None
        self.field_data_block: DataBlock = None
        self.data_parent: DataBlock = None
        self.parent: TagStruct = None
        self.childs: [TagStruct] = []
        self.l_function = []
        self.l_tag_ref = []
        self.parent_entry_index = -1
        self.entry_index = -1
        self.p_entry_index = -1
        self.bin_datas_info = []
        self.bin_datas = []
        self.bin_datas_hex = []
        self.type_ = 'Tagblock'
        self.field_name = ''
    
    def AddSubscribersForOnPrint(self, objMethod):
        self.onDataRead += objMethod

    
    def RemoveSubscribersOnPrint(self, objMethod):
        self.onDataRead -= objMethod


    def readIn(self, f, header=None):
        # self.hash.readIn(f, header)
        t_bytes = f.read(16)
        self.GUID1 = t_bytes[0:8].hex()
        self.GUID2 = t_bytes[8:16].hex()
        self.GUID = t_bytes.hex()
        self.type_id = struct.unpack('H', f.read(2))[0]
        self.type_id_tg = TagStructType(self.type_id)
        self.unknown_property_bool_0_1 = struct.unpack('H', f.read(2))[0]
        self.field_data_block_index = struct.unpack('i', f.read(4))[0]
        self.parent_field_data_block_index = struct.unpack('i', f.read(4))[0]
        self.field_offset = struct.unpack('i', f.read(4))[0]
        if (self.type_id_tg == TagStructType.NoDataStartBlock):
           if self.unknown_property_bool_0_1 == 1:
               print("NoDataStartBlock <-> unknown_property_bool_0_1 = 1")

    def readTagStructInfo(self, f):
        address_to_back = f.tell()
        address = -1
        self.info = TagStructInfo()
        if self.type_id_tg == TagStructType.Root:
            if self.unknown_property_bool_0_1 == 1:
                print("debug")
            self.info.property_address =  0
            self.info.n_childs = 1
            if self.parent_field_data_block_index != -1:
                raise Exception("Root no debe pertenecer a otro campo")
        elif self.type_id_tg == TagStructType.Tagblock:
            #assert self.unknown_property_bool_0_1 == 0
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 16)
            self.info.property_addres = address
            self.info.n_childs = struct.unpack('i', f.read(4))[0]
        elif self.type_id_tg == TagStructType.ExternalFileDescriptor:
            assert self.unknown_property_bool_0_1 == 0
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 12)
            self.info.property_addres = address
            self.info.n_childs = struct.unpack('i', f.read(4))[0]

            if self.info.n_childs != 0:
                print("ExternalFileDescriptor no debe tener hijos, ya que estan en archivo aparte")

        elif self.type_id_tg == TagStructType.ResourceHandle:
            # assert self.unknown_property_bool_0_1 == 1
            address = self.data_parent.offset_plus + self.field_offset
            f.seek(address + 12)
            self.info.property_addres = address
            self.info.n_childs = struct.unpack('i', f.read(4))[0]

        elif self.type_id_tg == TagStructType.NoDataStartBlock:
            # assert self.unknown_property_bool_0_1 == 1
            address = self.data_parent.offset_plus + self.field_offset
            if self.field_data_block_index != -1:
                raise Exception("NoDataStartBlock significa q no tiene informacion")
            f.seek(address)
            self.info.property_addres = address
            self.info.n_childs = struct.unpack('i', f.read(4))[0]
                    

        f.seek(address_to_back)

    def readBlockData(self, f, index:int, start_pos: int, len:int):
        resutlt = b''
        if False:
            f.seek(start_pos)    
            resutlt = f.read(len)
        # self.onDataRead()    
        return {
            "sender": self,
            "index": index,
            "start_pos": start_pos,
            "len": len
        }
    
    
    def __readDataEntryOld(self, f):
        blocks = []
        pos_on_init = f.tell()
        self.info = self.readTagStructInfo(f=f)
        if self.type_id == TagStructType.NoDataStartBlock:
            return blocks
        elif self.type_id == TagStructType.ExternalFileDescriptor:
            if self.info.n_childs != 0:
                #f.seek(pos_on_init)    
                print("Error de interpretacion de Datos, ya q son externos")
                if self.unknown_property_bool_0_1 == 0:
                    assert(self.field_data_block.size % self.info.n_childs == 0)
            if self.unknown_property_bool_0_1 != 0:
                self.info.childs_data_start_address = self.field_data_block.offset_plus
                self.info.child_data_size = self.field_data_block.size
                self.info.n_childs = 1
                # blocks.append(self.readBlockData(f,0,self.field_data_block.offset_plus,self.field_data_block.size))
            f.seek(pos_on_init)
            return blocks
        else:
            if self.info.n_childs == 0:
                if self.field_data_block_index != -1:
                    f.seek(pos_on_init)
                    raise Exception("Si no tiene hijos, el refernce deberia ser -1")
                f.seek(pos_on_init)
                return blocks
            else:
                if self.field_data_block is None:
                    f.seek(pos_on_init)
                    if self.type_id == TagStructType.ResourceHandle:
                        raise ReadTagStructException(str(f), self)
                    else:
                        assert(self.info["n_childs"] == 1)
                        blocks.append({})
                        return blocks

                count = divmod(self.field_data_block.size, self.info["n_childs"])

                if count[1] != 0:
                    raise Exception(' Deberia ser 0 siempre el resto')
                else:
                    if self.field_data_block.size == 0:
                        raise Exception(
                            ' Deberia ser moyor q 0, de lo contrario seria un bloke vacio, error division 0')
                    #f.seek(self.field_data_block.offset_plus)
                    sub_block_size = count[0]
                    self.info.child_data_size = count[0]
                    self.info.childs_data_start_address = self.field_data_block.offset_plus
                    #for k in range(self.info["n_childs"]):
                    #    blocks.append(self.readBlockData(f,k,self.field_data_block.offset_plus + k*sub_block_size,sub_block_size))
                    
                    f.seek(pos_on_init)
                    return blocks

    def readInfoChilds(self, f):
        #pos_on_init = f.tell()
        self.readTagStructInfo(f=f)
        if self.type_id == TagStructType.NoDataStartBlock:
            #f.seek(pos_on_init)
            return 
        elif self.type_id == TagStructType.ExternalFileDescriptor:
            if self.info.n_childs != 0:
                #f.seek(pos_on_init)    
                print("Error de interpretacion de Datos, ya q son externos")
                if self.unknown_property_bool_0_1 == 0:
                    assert(self.field_data_block.size % self.info.n_childs == 0)
            if self.unknown_property_bool_0_1 != 0:
                self.info.childs_data_start_address = self.field_data_block.offset_plus
                self.info.child_data_size = self.field_data_block.size
                self.info.n_childs = 1
            #f.seek(pos_on_init)
            return
        else:
            if self.info.n_childs == 0:
                if self.field_data_block_index != -1:
                    #f.seek(pos_on_init)
                    raise Exception("Si no tiene hijos, el refernce deberia ser -1")
                #f.seek(pos_on_init)
                return 
            else:
                if self.field_data_block is None:
                    #f.seek(pos_on_init)
                    if self.type_id == TagStructType.ResourceHandle:
                        raise ReadTagStructException(str(f), self)
                    else:
                        assert(self.info.n_childs == 1)
                        return 

                count = divmod(self.field_data_block.size, self.info.n_childs)

                if count[1] != 0:
                    raise Exception(' Deberia ser 0 siempre el resto')
                else:
                    if self.field_data_block.size == 0:
                        raise Exception(
                            ' Deberia ser moyor q 0, de lo contrario seria un bloke vacio, error division 0')
                    self.info.child_data_size = count[0]
                    self.info.childs_data_start_address = self.field_data_block.offset_plus
                    return 

    def getInstanceIndexInParent(self):
        if self.bin_datas.__len__() != 0:
            temp = len(self.bin_datas[0])
            if temp == 0:
                raise Exception('Data vacia en conteentry')

            d_m = divmod(self.field_offset, temp)
            return d_m[0]
        else:
            return 0


class TagStructTable:
    def __init__(self) -> None:
        self.entries: [TagStruct] = []
        self.evetToCall = None
        self.onEntryRead = Event()
        pass

    def AddSubscribersForOnEntryRead(self, objMethod):
        self.onEntryRead += objMethod

    
    def RemoveSubscribersEntryRead(self, objMethod):
        self.onEntryRead -= objMethod


    def readTable(self, f, header, data_block_table):
        f.seek(header.tag_struct_offset)
        for x in range(header.tag_struct_count):
            # offset = header.content_table_offset + x * 0x20
            entry = TagStruct()
            entry.AddSubscribersForOnPrint(self.evetToCall)
            entry.readIn(f, header)

            if header.data_block_count > entry.field_data_block_index > -1:
                entry.field_data_block = data_block_table.entries[entry.field_data_block_index]

            if header.data_block_count > entry.parent_field_data_block_index > -1:
                entry.data_parent = data_block_table.entries[entry.parent_field_data_block_index]

                p_i = self.getContentEntryByRefIndex(entry.parent_field_data_block_index)
                if p_i is not None:
                    entry.parent_entry_index = p_i
                    entry.parent = self.entries[p_i]
                    entry.p_entry_index = self.entries[p_i].childs.__len__()
                    self.entries[p_i].childs.append(entry)
                    

            entry.entry_index = self.entries.__len__()
            entry.readInfoChilds(f)
            #entry.bin_datas_info = entry.readDataEntry(f)
            pos_on_init = f.tell()
            self.onEntryRead(f, entry)
            f.seek(pos_on_init)
            
            #for data in entry.bin_datas:
            #    entry.bin_datas_hex.append(data.hex())
            self.entries.append(entry)
            

    def getContentEntryByRefIndex(self, ref_index):
        count = 0
        entry_found = None
        for i, entry in enumerate(self.entries):
            if entry.field_data_block_index == ref_index:
                count = count + 1
                entry_found = i
                return entry_found
        if count > 1:
            Log.Print(count)
        return entry_found
