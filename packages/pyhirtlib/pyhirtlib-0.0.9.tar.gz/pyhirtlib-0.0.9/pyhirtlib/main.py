"""    
import io
import os
from configs.config import Config
from commons.exception.read_tag_struct_exception import StopReadTagStructException
from tag_reader.tag_layouts import TagLayouts

from unpacker.tag_group_extension_map import *
import sys

from tag_reader.tag_parse import TagParse


def readEntry(f,i,k, entry, child_tag: TagLayouts.C):
    print(f"Reading field {child_tag.xmlPath[1]} index {i} sub index {k}")
    #if (child_tag.xmlPath[1] == "\\root\\render geometry\\Deformation parameter default value table from skeleton"):
    #    raise StopReadTagStructException(str(f), entry)

def testToDelete():
    from unpacker import run_unpacker
    unpack_path = ""
    Config.SetConfEntry("DEPLOY_PATH", "D:\\fbx_test\\modules")
    Config.SetConfEntry("TAG_XML_TEMPLATE_PATH","D:\\HaloInfiniteStuft\\Extracted\\UnPacked\\s4\\TagXml\\2023-09-27\\")
    deploy_path = Config.GetConfig()["DEPLOY_PATH"] 
    modules = []
    modules = run_unpacker.extract_all_modules("", False, unpack_path, deploy_path)
    path_xml = Config.GetConfig()["TAG_XML_TEMPLATE_PATH"]
    p = [os.path.join(dp, f)[len(path_xml):].replace("\\", "/") for dp, dn, fn in
        os.walk(os.path.expanduser(path_xml)) for f in fn if ".xml" in f]
    for key in p:
        #if key == "-ttag.xml":
        if key != "mode.xml":
            continue
        print(key)
        child_tag = TagLayouts.Tags(key.replace('.xml',''))
        out_t = TagLayouts.GetElemntAt(child_tag[0], "\\root\\render geometry\\Deformation parameter default value table from skeleton")
        pass
    
    if len(modules)>0:
        for mi, hi_module in enumerate(modules): 
            #if mi ==-1:
            if mi !=0:
                continue
            #hi_module = modules[0]
            #for index in range(hi_module.moduleHeader.FilesCount):
            #for index in range(7057,7058):
            for index in [1370,3341,7111,7057,8251]:
                #index= 2
                file_entry = hi_module.readFileEntry(index)
                
                decomp_save_data = hi_module.readFileEntryUnPackedBytes(file_entry)
                if (decomp_save_data==b''):
                    print(f"error de descompresion en {file_entry.tagGroupRev} index {index}")
                else:    
                    f_t = io.BytesIO(decomp_save_data)
                    if file_entry.tagGroupRev != '':
                        try:
                            tagParse = TagParse(file_entry.tagGroupRev)
                            tagParse.AddSubscribersForOnFieldRead(readEntry)
                            print(f'Realizando parse a {index} con id {file_entry.GlobalTagId} y template {file_entry.tagGroupRev}.')
                            tagParse.readIn(f_t)
                        except StopReadTagStructException as e:
                            print(e)

                        #tagFile.readInOnlyHeader(f_t)
            
    print("main")


if __name__ == "__main__":
    sys.path.append(Config.ROOT_DIR)
    testToDelete()
    
"""