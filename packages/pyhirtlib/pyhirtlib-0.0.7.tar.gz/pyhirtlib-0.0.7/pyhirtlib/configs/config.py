import os


class Config:
    ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    CONFIG = f"{ROOT_DIR}\\configs\\config.cfg" 
    OODLE_PATH = ""
    TAG_XML_TEMPLATE_PATH = "D:\\HaloInfiniteStuft\\Extracted\\UnPacked\\s4\\TagXml\\2023-08-11\\"
    #BASE_UNPACKED_PATH = "D:\\HaloInfiniteStuft\\Extracted\\UnPacked\\winter_update\\"
    BASE_UNPACKED_PATH = "D:\\HaloInfiniteStuft\\Extracted\\UnPacked\\emulate\\E\\"
    BASE_UNPACKED_PATH_CAMPAIGN = "D:\\HaloInfiniteStuft\\Extracted\\UnPacked\\campaign\\"
    # BASE_UNPACKED_PATH = BASE_UNPACKED_PATH_CAMPAIGN
    MODEL_EXPORT_PATH = "D:\\HaloInfiniteStuft\\Extracted\\Converted\\RE_OtherGames\\HI\\models\\"
    INFOS_PATH = 'C:\\Users\\Jorge\\Downloads\\Mover\\infos\\'
    EXPORT_JSON = 'J:\\Games\\Halo Infinite Stuf\\Extracted\\HI\\json\\'
    EXPORT_SHADERS = 'J:\\Games\\Halo Infinite Stuf\\Extracted\\shaderdis\\'
    SPARTAN_STYLE_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\UnPacked\\season2\\__chore\\gen__\\objects\\characters\\spartan_armor\\coatings\\"
    WEB_DOWNLOAD_DATA = "J:\\Games\\Halo Infinite Stuf\\Web-Json\\"
    UE5_PROJECT_IMPORTED_PC_PATH = "H:\\UE4\\Unreal_Projects\\HaloInfinities " \
                                   "5.0\\Content\\__chore\\gen__\\pc__\\"
    DEPLOY_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo Infinite\\deploy\\"
    DEPLOY_PATH_CAMPAIGN = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Halo Infinite\\deploy\\"
    EXPORTED_TEXTURE_PATH = "J:\\Games\\Halo Infinite Stuf\\Extracted\\Converted\\Textures\\TGA\\pc__\\"
    EXPORTED_TEXTURE_PATH_BASE = "J:\\Games\\Halo Infinite Stuf\\Extracted\\Converted\\Textures\\"

    VERBOSE = True

    def GetConfig():
        path = Config.CONFIG
        paths = {}

        with open(path,"r") as file:
            for line in file:
                entry = line.split('=')
                paths[entry[0].strip()] = entry[1].strip()
        return paths
        
        
    def SetConfEntry(key:str, value):
            update_val = Config.GetConfig()
            update_val[key] = value
            with open(Config.CONFIG, 'w') as f:
                for key in update_val.keys():
                    f.write(f"{key} = {update_val[key]}\n")

if not os.path.isfile(f"{Config.ROOT_DIR}\\configs\\config.cfg" ):
    with open(f"{Config.CONFIG}" ,"xt") as file:
        file.write(f"ROOT_DIR = {Config.ROOT_DIR}\n")
        file.write(f"CONFIG = {Config.CONFIG}\n")
        file.write(f"DEPLOY_PATH = {Config.DEPLOY_PATH}\n")
        file.write(f"DEPLOY_PATH = {Config.DEPLOY_PATH_CAMPAIGN}\n")
        file.write(f"OODLE_PATH = {Config.OODLE_PATH}\n")
        file.write(f"TAG_XML_TEMPLATE_PATH = {Config.TAG_XML_TEMPLATE_PATH}\n")
     

