def readStringInPlace(f, start, inplace=False):
    toBack = f.tell()
    f.seek(start)
    string = []
    while True:
        char = f.read(1)
        if char == b'\x00':
            if inplace:
                f.seek(toBack)
            return "".join(string)
        try:
            string.append(char.decode("utf-8"))
        except:
            try:
                char += f.read(1)
                string.append(char.decode("utf-8"))
            except:
                if inplace:
                    f.seek(toBack)
                return "".join(string)