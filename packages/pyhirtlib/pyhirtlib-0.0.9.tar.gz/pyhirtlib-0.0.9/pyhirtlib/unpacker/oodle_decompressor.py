from enum import IntFlag
import os
from ctypes import cdll, c_char_p, create_string_buffer

from configs.config import Config

class OodleLZ_Compressor(IntFlag):
    Invalid = -1
    LZH = 0
    LZHLW = 1
    LZNIB = 2
    NONE = 3
    LZB16 = 4
    LZBLW = 5
    LZA = 6
    LZNA = 7
    Kraken = 8
    Mermaid = 9
    BitKnit = 10
    Selkie = 11
    Hydra = 12
    Leviathan = 13

class OodleLZ_Decode_ThreadPhase(IntFlag): 
    ThreadPhase1 = 1
    ThreadPhase2 = 2
    Unthreaded = 3

class OodleLZ_Verbosity(IntFlag): 
    NONE = 0
    Max = 3
    

class OodleLZ_CheckCRC(IntFlag): 
    No = 0
    Yes = 1

class OodleLZ_FuzzSafe(IntFlag):
    No = 0
    Yes = 1

class OodleLZ_CompressionLevel(IntFlag):
    HyperFast4 = -4
    HyperFast3 = -3
    HyperFast2 = -2
    HyperFast1 = -1
    NONE = 0
    SuperFast = 1
    VeryFast = 2
    Fast = 3
    Normal = 4
    Optimal1 = 5
    Optimal2 = 6
    Optimal3 = 7
    Optimal4 = 8
    Optimal5 = 9
    Min = -4
    Max = 9
    

class OodleDecompressor:
    """
    Oodle decompression implementation.
    Requires Windows and the external Oodle library.
    """
    
    def __init__(self, library_path: str = None) -> None:
        """
        Initialize instance and try to load the library.
        """
        if library_path is None:
            conf = Config.GetConfig()
            
            oodp = ""
            if conf.keys().__contains__("OODLE_PATH"):
                oodp = conf["OODLE_PATH"]
            if oodp =="":
                ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
                library_path = ROOT_DIR + "\\unpacker\\oo2core_8_win64.dll"
            else:
                library_path = oodp

        if not os.path.exists(library_path):
            print(f'Looking in {library_path}')
            raise Exception("Could not open Oodle DLL, make sure it is configured correctly.")

        try:
            self.handle = cdll.LoadLibrary(library_path)
        except OSError as e:
            raise Exception(
                "Could not load Oodle DLL, requires Windows and 64bit python to run."
            ) from e

    def decompress(self, payload: bytes, output_size) -> bytes:
        """
        Decompress the payload using the given size.
        """
        output = create_string_buffer(output_size)
        try:
            self.handle.OodleLZ_Decompress(
                c_char_p(payload), len(payload), output, output_size,
                0, 0, 0, None, None, None, None, None, None, 3)
        except OSError:
            return False
        return output.raw
    
    def compress(self, buffer: bytes, size:int, c_size:int ,format: OodleLZ_Compressor = OodleLZ_Compressor.Kraken, level: OodleLZ_CompressionLevel = OodleLZ_CompressionLevel.Optimal5) -> bytes:
        """
        Decompress the payload using the given size.
        """
        
        try:
            skBuffer: bytes = b''
            skBufferSize = len(skBuffer)
            if c_size == 0:
                compressedBufferSize = self.GetCompressionBound(size)
                c_size = compressedBufferSize
            compressedBuffer = create_string_buffer(c_size)

            self.handle.OodleLZ_Compress(format,c_char_p(buffer), len(buffer), compressedBuffer, level, None, None, None,skBufferSize)
        except Exception as err:
            return False
        return compressedBuffer.raw
    
    def  GetCompressionBound(self, bufferSize: int)-> int:
        return int(bufferSize + 274 * ((bufferSize + 0x3FFFF) / 0x40000))
    
class InstanceOodle:
    oodle: OodleDecompressor = None
    

    @staticmethod
    def get(library_path: str = None, forcenew = False):
        if InstanceOodle.oodle is None or forcenew:
            InstanceOodle.oodle = OodleDecompressor(library_path)
        return InstanceOodle.oodle