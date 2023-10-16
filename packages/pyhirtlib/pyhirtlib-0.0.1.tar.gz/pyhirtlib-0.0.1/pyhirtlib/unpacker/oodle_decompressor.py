import os
from ctypes import cdll, c_char_p, create_string_buffer


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
           ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
           library_path = ROOT_DIR + "\\unpacker\\oo2core_8_win64.dll"

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