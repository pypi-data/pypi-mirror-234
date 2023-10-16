import inspect
import os
import xml.etree.ElementTree as ET

from configs.config import Config
from tag_reader.tag_element_type import TagElemntType


class TagLayouts:

    def GetElemntType(tagGroup:str) -> TagElemntType:
            if tagGroup == "root":
                return TagElemntType.RootTagInstance
            result =  TagElemntType(int(tagGroup.replace('_',"0x"),0))
            if result == 0 and tagGroup != "_0":
                return TagElemntType.Undefined
            return result
    
    class C:

        def __init__(self,p_G='', p_N='', p_S=0, p_E={}, xmlPath=None):
            
            self.E = p_E
            """
            #/ <summary>
            #/ Length of the tagblock
            #/ </summary>
            """
            self.S = p_S  # public long S { get set } # S = size # length of tagblock

            self.N = p_N  # N = name # our name for the block

            self.G = p_G
            
            self.xmlPath = xmlPath

            """
            #/ <summary>
            #/ Set during load, will be used when I add netcode 
            #/ </summary>
            """
            self.MemoryAddress = 0

            """
            #/ <summary>
            #/ The absolute offset from the base address of the tag
            #/ eg C2 will resolve to assault_rifle_mp.weapon + C2 
            #/ 
            #/ This will be recursive so the actual value might be 
            #/		assault_rifle_mp.weapon + C2 + (nested block) 12 + (nested block) 4
            #/		
            #/ This will allow us to sync up changes across the server and client without
            #/ the need to re-resolve memory addresses.
            #/ </summary>
            """

            self.T = TagLayouts.GetElemntType(self.G)

    class FlagGroup(C):

        def __init__(self, p_G: str='', p_N: str = '', p_A: int = 0,  p_STR={}, p_S=0, p_E={}, xmlPath=None ):
            super().__init__(p_G, p_N, p_S, p_E, xmlPath)
            """
                    #/ <summary>
                    #/ Amount of bytes for flags
                    #/ </summary>
                    """
            self.A = p_A

            """
            #/ <summary>
            #/ The max bit, if 0 then defaults to A * 8
            #/ </summary>
            """
            self.MB: int = 0

            """
            #/ <summary>
            #/ String description of the flags
            #/ </summary>
            """
            self.STR = p_STR  # public Dictionary<int, string> STR { get set } = new Dictionary<int, string>()

    class EnumGroup(C):

        def __init__(self,p_G: str='', p_N: str = '', p_A: int = 0, p_STR={}, p_S=0, p_E={}, xmlPath=None ):
            super().__init__(p_G, p_N, p_S, p_E, xmlPath)
            # self.T = TagElemntType.EnumGroup
            """
                    #/ <summary>
                    #/ Amount of bytes for enum
                    #/ </summary>
                    """
            self.A = p_A

            """
            #/ <summary>
            #/ String description of the flags
            #/ </summary>
            """
            self.STR = p_STR
    
    class P(C):
        def __init__(self, p_G: str='', p_N: str = '',  p_B = {}, p_S=0, p_E={}, xmlPath=None ):
            super().__init__(p_G, p_N, p_S, p_E, xmlPath)
            if p_B is None:
                p_B = {}
            self.B = p_B  # Dictionary<long, C>? B { get set } = null  # B = blocks? i forgot what B stands for

    @staticmethod
    def GetElemntAt(tag_template: P , elemn_path:str, by_names = True) -> TagElemntType:
        if tag_template is None:
            return None
        if by_names:
            if tag_template.xmlPath[1] == elemn_path:
                return tag_template
        else:
            if tag_template.xmlPath[0] == elemn_path:
                return tag_template
        for address in tag_template.B:
            child_tag = tag_template.B[address]
            to_compare = child_tag.xmlPath[1]
            if not by_names:
                to_compare = child_tag.xmlPath[0]
            
            if to_compare == elemn_path:
                return child_tag
                
            if isinstance(child_tag, TagLayouts.P):
                if elemn_path.find(to_compare)==0:
                    return TagLayouts.GetElemntAt(child_tag, elemn_path, by_names)

    
    @staticmethod
    def Tags(grouptype: str):
        r = TagLayouts.run_parse()
        return r.parse_the_mfing_xmls(grouptype)

    class run_parse:

        def __init__(self):
            self.evalutated_index_PREVENT_DICTIONARYERROR = 99999
            pass

        def parse_the_mfing_xmls(self, file_to_find: str):
            poopdict = {}

            # e still need to evalute the string and find the value withoin our plugins folder

            if file_to_find.__contains__("*"):
                file_to_find = file_to_find.replace("*", "_")

            #predicted_file = os.path.curdir + '\\plugins\\' + file_to_find + '.xml'

            filename = inspect.getframeinfo(inspect.currentframe()).filename
            #path = os.path.dirname(os.path.abspath(filename))
            #predicted_file = path + '\\tags\\' + file_to_find + '.xml'
            #predicted_file = path + '\\plugins\\' + file_to_find + '.xml'
            predicted_file = Config.GetConfig()["TAG_XML_TEMPLATE_PATH"] + file_to_find + '.xml'

            if os.path.exists(predicted_file):
                xd = ET.parse(predicted_file)
                xn = xd.getroot()
                current_offset = 0
                current_offset = current_offset + self.the_switch_statement(xn, current_offset,("",""),
                                                                                poopdict)  # ref poopdict

            return poopdict

        def fill_general_extra_data(self, xn, extra_afl = {}):
            extra_afl.clear()
            self.add_atribute(xn, extra_afl, "hash")
            self.add_atribute(xn, extra_afl, "T1")
            self.add_atribute(xn, extra_afl, "T2")
            self.add_atribute(xn, extra_afl, "hashTR0")
            self.add_atribute(xn, extra_afl, "hashTR1")
            self.add_atribute(xn, extra_afl, "comp")
            self.add_atribute(xn, extra_afl, "ui6")
            self.add_atribute(xn, extra_afl, "aottr")
            self.add_atribute(xn, extra_afl, "size")
            self.add_atribute(xn, extra_afl, "ui2")
            self.add_atribute(xn, extra_afl, "ui3")
            self.add_atribute(xn, extra_afl, "ui4")
            self.add_atribute(xn, extra_afl, "au0")
            self.add_atribute(xn, extra_afl, "ul1")
            self.add_atribute(xn, extra_afl, "ul2")
            self.add_atribute(xn, extra_afl, "ul3")
            

        def add_atribute(self, xn, extra_afl, name):
            if xn.attrib.keys().__contains__(name):
                extra_afl[name] = xn.attrib[name]

        def get_path_of_element(self, xn:ET):
            path:str = xn.tag
            temp = xn
            #while temp. != null)
            #{
            #    temp = temp.ParentNode;
            #    path = temp.Name + "\\" + path;
            #}
            return path
            
        
        def get_path_of_element_named(self, xn:ET):
            path:str = xn.tag
            if xn.attrib.keys().__contains__("v"):
                path = xn.attrib["v"]
            temp = xn
            #while temp. != null)
            #{
            #    temp = temp.ParentNode;
            #    path = temp.Name + "\\" + path;
            #}
            return path

        def the_switch_statement(self, xn, offset, parent_path,pairs={}):
            s_p = self.get_path_of_element(xn)
            s_p_n = self.get_path_of_element_named(xn)
            child_path = (parent_path[0]+"\\"+s_p,parent_path[1]+"\\"+s_p_n)
            extra_afl = {}
            self.fill_general_extra_data(xn, extra_afl)
            t_size = 0 #TagLayouts.run_parse.group_lengths_dict[xn.tag]
            if xn.attrib.keys().__contains__("s"):
                t_size = int(xn.attrib["s"])
            if xn.tag == "root":
                extra_afl.clear()
                if len(xn) > 0:
                    subthings = {}
                    self.fill_general_extra_data(xn, extra_afl)
                    current_offset2 = 0
                    for xntwo2 in xn:
                        current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2, child_path, subthings)
                      
                    pairs[offset] = TagLayouts.P( xn.tag, "root", subthings, current_offset2, p_E=extra_afl, xmlPath = ("root", "root")  )
                    assert int(pairs[offset].E["size"]) == current_offset2
                    return current_offset2
                else:
                    pairs[offset] = TagLayouts.P("_40",  xn.attrib["v"], {},
                                                 p_S=20, p_E=extra_afl, xmlPath=child_path)
                return 0
            elif xn.tag == "_A": # char enum
                childdictionary1 = {}
                for iu in range(len(xn)):
                    childdictionary1[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(xn.tag, xn.attrib["v"], 1, childdictionary1, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_B": #  short enum
                childdictionary2 = {}
                for iu in range(len(xn)):
                    childdictionary2[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(xn.tag, xn.attrib["v"], 2, childdictionary2, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_C": # long enum
                childdictionary3 = {}
                for iu in range(len(xn)):
                    childdictionary3[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(xn.tag, xn.attrib["v"], 4, childdictionary3, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_D": # long flags
                childdictionary4 = {}
                for iu in range(len(xn)):
                    childdictionary4[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(xn.tag, xn.attrib["v"], 4, childdictionary4, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_E": # word flags
                childdictionary5 = {}
                for iu in range(len(xn)):
                    childdictionary5[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(xn.tag, xn.attrib["v"], 2, childdictionary5, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_F": # byte flags
                childdictionary6 = {}
                for iu in range(len(xn)):
                    childdictionary6[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(xn.tag, xn.attrib["v"], 1, childdictionary6, p_S = t_size, p_E=extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_34" or xn.tag == "_35":
                length = int(xn.attrib["length"])
                pairs[offset] = TagLayouts.C(xn.tag, xn.attrib["v"], p_S=length, p_E = extra_afl, xmlPath=child_path)
                return length
            elif xn.tag == "_36":
                if xn.attrib["v"] != '':
                    pairs[offset + self.evalutated_index_PREVENT_DICTIONARYERROR] = TagLayouts.C(xn.tag, xn.attrib["v"], p_E = extra_afl, xmlPath=child_path)
                    self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                else:
                    debug = 0  # debug
                return 0
            elif xn.tag == "_37":
                if xn.attrib["v"] != '':
                    pairs[offset + self.evalutated_index_PREVENT_DICTIONARYERROR] = TagLayouts.C(xn.tag, xn.attrib["v"],p_S=0, p_E = extra_afl, xmlPath=child_path)
                    self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                else:
                    debug = 0  # debug
                return 0
            elif xn.tag == "_38":  # //struct
                
                temp_index = offset #+ self.evalutated_index_PREVENT_DICTIONARYERROR
                
                #self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                current_offset1 = 0
                xnl1 = list(xn)
                sub_dic = {}
                for xntwo2 in xnl1:
                    current_offset1 = current_offset1 + self.the_switch_statement(xntwo2, current_offset1,child_path, sub_dic)
                
                pairs[temp_index] = TagLayouts.P(xn.tag, xn.attrib["v"], p_B=sub_dic,p_S=current_offset1, p_E=extra_afl, xmlPath=child_path)
                assert int(pairs[temp_index].E["size"]) == current_offset1
                return current_offset1
            elif xn.tag == "_39":
                if len(xn) > 0:
                    subthings = {}
                    current_offset3 = 0
                    for xntwo2 in xn:
                        current_offset3 = current_offset3 + self.the_switch_statement(xntwo2, current_offset3,child_path,
                                                                                      subthings)
                    count = 0
                    if xn.attrib.keys().__contains__("count"):
                        extra_afl["count"] = int(xn.attrib["count"])
                        count = extra_afl["count"]
                        # its gonna append that to the main, rather than our struct
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"], subthings, current_offset3*count, p_E= extra_afl, xmlPath=child_path)
                    assert int(pairs[offset].E["size"]) == current_offset3
                    return current_offset3 * count
                else:
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"],
                                                 p_S=t_size,  p_E= extra_afl, xmlPath=child_path)
                    return 0
            elif xn.tag == "_3B":
                return t_size
            elif xn.tag == "_40":
                if len(xn) > 0:
                    subthings = {}
                    current_offset2 = 0
                    for xntwo2 in xn:
                        current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2,child_path,
                                                                                      subthings)
                        # its gonna append that to the main, rather than our struct
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"], subthings, current_offset2,  p_E= extra_afl, xmlPath=child_path)
                    assert int(pairs[offset].E["size"]) == current_offset2
                else:
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"],
                                                 p_S=t_size, p_E= extra_afl, xmlPath=child_path)
                return t_size
            elif xn.tag == "_43":  #
                subthings = {}
                current_offset2 =  0
                if len(xn) > 0:
                    for xntwo2 in xn:
                        current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2,child_path,
                                                                                    subthings)
                        # its gonna append that to the main, rather than our struct
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"],
                                                subthings, current_offset2,  p_E= extra_afl, xmlPath=child_path)
                else:
                    pairs[offset] = TagLayouts.P(xn.tag, xn.attrib["v"],
                                                subthings, t_size,  p_E= extra_afl, xmlPath=child_path)
                return t_size
            else:  
                if (TagLayouts.GetElemntType(xn.tag) != TagElemntType.Undefined):
                    pairs[offset] = TagLayouts.C(xn.tag, xn.attrib["v"], p_S=t_size, p_E=extra_afl, xmlPath=child_path)
                    return t_size
                


        group_lengths_dict = {
            "root": 0,
            "_0": 32 , # _field_string
            "_1": 256 , # _field_long_string
            "_2": 4 , # _field_string_id
            "_3": 4 , # ## Not found in any tag type
            "_4": 1 , # _field_char_integer
            "_5": 2 , # _field_short_integer
            "_6": 4 , # _field_long_integer
            "_7": 8 , # _field_int64_integer
            "_8": 4 , # _field_angle
            "_9": 4 , # _field_tag
            "_A": 1 , # _field_char_enum
            "_B": 2 , # _field_short_enum
            "_C": 4 , # _field_long_enum
            "_D": 4 , # _field_long_flags
            "_E": 2 , # _field_word_flags
            "_F": 1 , # _field_byte_flags
            "_10": 4 , # _field_point_2d -- 2 2bytes?
            "_11": 8 , # _field_rectangle_2d
            "_12": 4 , # _field_rgb_color -- hex color codes --- rgb pixel 32 - it's technically only 3 bytes but the final byte is FF
            "_13": 4 , # _field_argb_color --- argb pixel 32
            "_14": 4 , # _field_real
            "_15": 4 , # _field_real_fraction
            "_16": 8 , # _field_real_point_2d
            "_17": 12 , # _field_real_point_3d
            "_18": 8 , # _field_real_vector_2d -- 
            "_19": 12 , # _field_real_vector_3d
            "_1A": 16 , # _field_real_quaternion
            "_1B": 8 , # _field_real_euler_angles_2d
            "_1C": 12 , # _field_real_euler_angles_3d
            "_1D": 12 , # _field_real_plane_2d
            "_1E": 16 , # _field_real_plane_3d
            "_1F": 12 , # _field_real_rgb_color
            "_20": 16 , # _field_real_argb_color
            "_21": 4 , # _field_real_hsv_colo
            "_22": 4 , # _field_real_ahsv_color
            "_23": 4 , # _field_short_bounds
            "_24": 8 , # _field_angle_bounds
            "_25": 8 , # _field_real_bounds
            "_26": 8 , # _field_real_fraction_bounds
            "_27": 4 , # ## Not found in any tag type
            "_28": 4 , # ## Not found in any tag type
            "_29": 4 , # _field_long_block_flags
            "_2A": 2 , # _field_word_block_flags
            "_2B": 1 , # _field_byte_block_flags
            "_2C": 1 , # _field_char_block_index
            "_2D": 1 , # _field_custom_char_block_index
            "_2E": 2 , # _field_short_block_index
            "_2F": 2 , # _field_custom_short_block_index
            "_30": 4 , # _field_long_block_index
            "_31": 4 , # _field_custom_long_block_index
            "_32": 4 , # ## Not found in any tag type
            "_33": 4 , # ## Not found in any tag type
            "_34": 4 , # _field_pad ## variable length
            "_35": 4 , # 'field_skip' ## iirc
            "_36": 0 , # _field_explanation
            "_37": 0 , # _field_custom
            "_38": 0 , # _field_struct
            "_39": 32 , # _field_array
            "_3A": 4 ,
            "_3B": 0 , # ## end of struct or something
            "_3C": 1 , # _field_byte_integer
            "_3D": 2 , # _field_word_integer
            "_3E": 4 , # _field_dword_integer
            "_3F": 8 , # _field_qword_integer
            "_40": 20 , # _field_block_v2
            "_41": 28 , # _field_reference_v2
            "_42": 24 , # _field_data_v2

            "_43": 16 , # ok _field_resource_handle

            "_44": 256, # revisar original 4 --- data path
            "_45": 16 ,
        }
