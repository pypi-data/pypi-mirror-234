#PyZeroWidth | Encoding Functions






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
def __convertBase(number: int, base: int) -> str:
    if number == 0: return '0'
    digits = []
    while number:
        digits.append(int(number%base))
        number //= base
    return ''.join([str(i) for i in digits[::-1]])



def __qua(number: int) -> str:
    return __convertBase(number, 4)



def __tri(number: int) -> str:
    return __convertBase(number, 3)



def __encodeBase(text: str, secret: str, base: str, encoding: str, fillAmount: int):
    global ZWCharacters

    if not any([encoding.lower() in alis for alis in ZWCharacterSelections]): return None
    localZWCharacters = ZWCharacters[[encoding.lower() in alis for alis in ZWCharacterSelections].index(True)]

    match base:
        case 'bin': secret = ''.join([bin(ord(i))[2:].zfill(fillAmount) for i in secret])
        case 'tri': secret = ''.join([__tri(ord(i)).zfill(fillAmount) for i in secret])
        case 'qua': secret = ''.join([__qua(ord(i)).zfill(fillAmount) for i in secret])
    
    secret = ''.join([localZWCharacters[int(i)] for i in secret])

    splitLength = max(int(round(len(secret) / len(text))), 1)
    secret = [secret[i:i+splitLength] for i in range(0, len(secret), splitLength)]

    text = list(text) + ['' for i in range(max(0, len(secret) - len(text)))]
    secret += [''  for i in range(max(0, len(text) - len(secret)))]

    return ''.join([text[i] + secret[i] for i in range(len(text))])



def __binaryFill(text: str, secret: str, encoding: str, fillAmount: int) -> str:
    return __encodeBase(text, secret, 'bin', encoding, fillAmount)



def __trinaryFill(text: str, secret: str, encoding: str, fillAmount: int) -> str:
    return __encodeBase(text, secret, 'tri', encoding, fillAmount)



def __quaternaryFill(text: str, secret: str, encoding: str, fillAmount: int) -> str:
    return __encodeBase(text, secret, 'qua', encoding, fillAmount)






#Public Functions
def binary8(text: str, secret: str, encoding: str = 'utf') -> str:
    return __binaryFill(text, secret, encoding, 8)



def binary16(text: str, secret: str, encoding: str = 'utf') -> str:
    return __binaryFill(text, secret, encoding, 16)



def binary24(text: str, secret: str, encoding: str = 'utf') -> str:
    return __binaryFill(text, secret, encoding, 24)



def trinary6(text: str, secret: str, encoding: str = 'utf') -> str:
    return __trinaryFill(text, secret, encoding, 6)



def trinary11(text: str, secret: str, encoding: str = 'utf') -> str:
    return __trinaryFill(text, secret, encoding, 11)



def trinary16(text: str, secret: str, encoding: str = 'utf') -> str:
    return __trinaryFill(text, secret, encoding, 16)



def quaternary4(text: str, secret: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(text, secret, encoding, 4)



def quaternary8(text: str, secret: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(text, secret, encoding, 8)



def quaternary12(text: str, secret: str, encoding: str = 'utf') -> str:
    return __quaternaryFill(text, secret, encoding, 12)