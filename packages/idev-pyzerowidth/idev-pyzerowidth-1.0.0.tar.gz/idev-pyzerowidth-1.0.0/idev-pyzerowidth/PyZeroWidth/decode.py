#PyZeroWidth | Decoding Functions






#Global Variables
ZWCharacterSelections = [
    ['utf8','utf-8','u8','utf', 'cp65001'],
    ['ascii','us-ascii','646'],
    ['latin', 'latin1', 'latin_1', 'iso-8859-1', 'iso8859-1', '8859', 'cp819']
]

ZWCharacters = [
    ['\u200c','\u200d','\u2060','\ufeff'],
    ['\x00', '\x07', '\x08', '\x09'],
    ['\x80', '\x81', '\x82', '\x83']
]






#Private Functions
def __decodeBase(message: str, base: str, encoding: str, fillAmount: int) -> str:
    global ZWCharacterSelections
    global ZWCharacters

    if not any([encoding in alis for alis in ZWCharacterSelections]): return None
    localZWCharacters = ZWCharacters[[encoding in alis for alis in ZWCharacterSelections].index(True)]

    secret = [i for i in list(message) if i in localZWCharacters]
    secret = ''.join([str(localZWCharacters.index(i)) for i in secret])
    secret = [secret[i:i+fillAmount] for i in range(0, len(secret), fillAmount)]

    base = {'bin' : 2, 'tri' : 3, 'qua' : 4}.get(base)
    secret = [chr(int(i, base)) for i in secret]

    return ''.join(secret)
    


def __binaryFill(message: str, encoding: str, fillAmount: int) -> str:
    return __decodeBase(message, 'bin', encoding, fillAmount)



def __trinaryFill(message: str, encoding: str, fillAmount: int) -> str:
    return __decodeBase(message, 'tri', encoding, fillAmount)



def __quaternaryFill(message: str, encoding: str, fillAmount: int) -> str:
    return __decodeBase(message, 'qua', encoding, fillAmount)





#Public Functions
def binary8(message: str, encoding: str = 'utf') -> str:
    return __binaryFill(message, encoding, 8)



def binary16(message: str, encoding: str = 'utf') -> str:
    return __binaryFill(message, encoding, 16)



def binary24(message: str, encoding: str = 'utf') -> str:
    return __binaryFill(message, encoding, 24)



def trinary6(message: str, encoding: str = 'utf') -> str:
    return __trinaryFill(message, encoding, 6)



def trinary11(message: str, encoding: str = 'utf') -> str:
    return __trinaryFill(message, encoding, 11)



def trinary16(message: str, encoding: str = 'utf') -> str:
    return __trinaryFill(message, encoding, 16)



def quaternary4(message: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(message, encoding, 4)



def quaternary8(message: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(message, encoding, 8)



def quaternary12(message: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(message, encoding, 12)