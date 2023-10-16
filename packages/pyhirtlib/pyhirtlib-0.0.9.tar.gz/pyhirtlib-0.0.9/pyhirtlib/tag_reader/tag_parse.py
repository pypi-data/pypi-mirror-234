from commons.to_debug import NoDataStartedStruct
from commons.exception.read_tag_struct_exception import ReadTagStructException
from tag_reader.headers.tag_struct_table import TagStruct
from tag_reader.tag_element_type import BLOCKS, TagElemntType, TagStructType
from tag_reader.tag_layouts import TagLayouts
from tag_reader.tag_file import  TagFile
from events import Event

class TagFileMap:
    def __init__(self):
        self.blocks = {}
        self.datas = {}
        self.refers = {}
        
class TagParse:
    def __init__(self, group:str):
        self.debug = False
        self.tagFile = TagFile()
        self.tagFile.evetToCall = self.doSomeOn
        self.tagFile.tag_struct_table.AddSubscribersForOnEntryRead(self.onEntryRead)
        self.group = group
        self.xml_template =None
        self.tag_structs_list = {}
        self.onFieldRead = Event()

    def AddSubscribersForOnFieldRead(self, objMethod):
        self.onFieldRead += objMethod

    
    def RemoveSubscribersForOnFieldRead(self, objMethod):
        self.onFieldRead -= objMethod

    def readIn(self, f, p_xml_tamplate = None):
        if p_xml_tamplate is None:
            self.xml_template = TagLayouts.Tags(self.group)
        #self.tag_structs_list[0]=self.xml_template[0]
        self.tagFile.readIn(f)
        
        #tagFile.readInOnlyHeader(f_t)

    def doSomeOn(self, params):
        pass

    def onEntryRead(self, f, entry: TagStruct):
        if not (entry is None):
            if entry.field_data_block_index == -1:
                pass
                #return
            
            tag: TagLayouts.C = None
            if entry.type_id_tg != TagStructType.Root:
                tag = self.tag_structs_list[entry.parent_entry_index].blocks[entry.field_offset]
                if (tag.T == TagElemntType.Struct):
                    if entry.type_id_tg != TagStructType.NoDataStartBlock:
                        raise ReadTagStructException(str(f), entry)
                
                if tag.E["hash"].upper() != entry.GUID.upper():
                    print("No equal hash")
            else:
                tag = self.xml_template[0]
            
            outresult = TagFileMap()
            
            if entry.info.n_childs != -1:
                for x in range(entry.info.n_childs): 
                    s = self.readTagDefinition(f, x, 0,entry,tag, outresult,int(tag.E['size'])*x)
            else:
                print("debug")
            self.tag_structs_list[entry.entry_index] = outresult
            if self.debug:
                if tag.T == TagElemntType.RootTagInstance:
                    assert(tag.E["hash"]==  entry.GUID.upper())
                    assert(entry.type_id_tg == TagStructType.Root)
                else:
                    assert tag.E["hash"]==entry.GUID.upper(), f"No equal hash {tag.E['hash']} == {entry.GUID.upper()}"
        pass
        
    def readTagDefinition(self,f, i, k, entry: TagStruct, tags: TagLayouts.C, outresult: TagFileMap, field_offset:int = 0) -> int:
        result = 0
        
        for address in tags.B:
            
            child_tag = tags.B[address]
            result+= child_tag.S
            self.onFieldRead(f,i,k, entry, child_tag)
            self.verifyAndAddTagBlocks(outresult, child_tag, field_offset + address)
            if child_tag.T == TagElemntType.Struct:
                self.readTagDefinition(f, i, k, entry, child_tag, outresult, field_offset + address)
            elif child_tag.T == TagElemntType.Array:
                for _k in range(child_tag.E["count"]):
                    self.readTagDefinition(f, i, _k, entry, child_tag, outresult, field_offset + address)
        return result

    def verifyAndAddTagBlocks(self, tag_maps: TagFileMap, child_item: TagLayouts.C, field_offset: int):
        if child_item.T == TagElemntType.DataV2:
            tag_maps.datas[field_offset] = child_item
            return
        elif child_item.T == TagElemntType.TagReference:
            tag_maps.refers[field_offset] = child_item
            return
        elif child_item.T == TagElemntType.Struct:
            if child_item.E["comp"] == "1" : 
                tag_maps.blocks[field_offset] =  child_item
            return
        elif child_item.T == TagElemntType.Block:
            tag_maps.blocks[field_offset] =  child_item
            return
        elif child_item.T == TagElemntType.ResourceHandle:
            tag_maps.blocks[field_offset] =  child_item
            return
        else:
            return