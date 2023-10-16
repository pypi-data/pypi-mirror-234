#PyZeroWidth | Decoding Functions






#Global Variables
ZWCharacterSelections = [
    [
        'utf_7', 'u7', 'unicode-1-1-utf-7'
        'utf8','utf-8','u8','utf', 'cp65001',
        'utf16', 'utf_16', 'u16'
        'utf_16_be', 'utf-16be',
        'utf_16_le', 'utf-16le',
        'utf32', 'utf_32', 'u32',
        'utf_32_be', 'utf-32be',
        'utf_32_le', 'utf-32le'
    ],

    [
        'ascii','us-ascii','646'
    ],
    
    [
        'latin', 'latin1', 'latin_1', 'iso-8859-1', 'iso8859-1', '8859', 'cp819',
        'latin2', 'iso8859_2', 'iso-8859-2', 'l2',
        'latin3', 'iso8859_3', 'iso-8859-3', 'l3',
        'latin4', 'iso8859_4', 'iso-8859-4', 'l4',
        'latin5', 'iso8859_9', 'iso8859-9', 'l5',
        'latin6', 'iso8859_10', 'iso8859-10', 'l6'
        'latin7', 'iso8859_13', 'iso8859-13', 'l7',
        'latin8', 'iso8859_14', 'iso8859-14', 'l8',
        'latin9', 'iso8859_15', 'iso8859-15', 'l9',
        'latin10', 'iso8859_16', 'iso8859-16', 'l10'
        'cyrillic', 'iso8859_5', 'iso8859-5',
        'arabic', 'iso8859_6', 'iso8859-6',
        'greek', 'greek8', 'iso8859_7', 'iso8859-7',
        'hebrew', 'iso8859_8', 'iso8859-8',
        'thai', 'iso8859_11', 'iso8859-11'
    ],
    
    [
        'big5', 'big5-tw', 'csbig5', 'big5hkscs', 'big5-hkscs', 'hkscs', 
        'cp037', 'ibm037', 'ibm039', 
        'cp273', '273', 'ibm273', 'csibm273',
        'cp424', 'ebcdic-cp-he', 'ibm424',
        'cp437', '437', 'ibm437',
        'cp500', 'ebcdic-cp-be', 'ebcdic-cp-ch', 'ibm500',
        'cp720',
        'cp737',
        'cp775', 'ibm775',
        'cp850', '850', 'ibm855',
        'cp852', '852', 'ibm852',
        'cp855', '855', 'ibm855',
        'cp856',
        'cp857', '857', 'ibm857',
        'cp858', '858', 'ibm858',
        'cp860', '860', 'ibm860',
        'cp861', '861', 'ibm861', 'cp-is',
        'cp862', '862', 'ibm862',
        'cp863', '863', 'ibm863',
        'cp864', 'ibm863',
        'cp865', '865', 'ibm865',
        'cp866', '866', 'ibm866',
        'cp869', '869', 'ibm869', 'cp-gr',
        'cp874',
        'cp875',
        'cp932', '932', 'ms932', 'mskanji', 'ms-kanji',
        'cp949', '949', 'ms949', 'uhc',
        'cp950', '950',
        'cp1006',
        'cp1026', 'ibm1026',
        'cp1125', '1125', 'ibm1125', 'cp866u', 'ruscii',
        'cp1140', 'ibm1140',
        'cp1250', 'windows-1250',
        'cp1251', 'windows-1251',
        'cp1252', 'windows-1252',
        'cp1253', 'windows-1253',
        'cp1254', 'windows-1254',
        'cp1255', 'windows-1255',
        'cp1256', 'windows-1256',
        'cp1257', 'windows-1257',
        'cp1258', 'windows-1258',
        'euc_jp', 'eucjp', 'ujis', 'u-jis',
        'euc_jis_2004', 'jsix0213', 'eucjis2004',
        'euc_jisx0213', 'eucjisx0213',
        'korean', 'euc_kr', 'euckr', 'ksc5601', 'ks_c-5601', 'ks_c-5601-1987', 'ksx1001', 'ksx1001', 'ks_x-1001',
        'chinese', 'gb2312', 'csiso58gb231280', 'euc-cn', 'euccn', 'eucgb2312-cn', 'gb2312-1980', 'gb2312-80', 'iso-ir-58',
        'cp936', '936', 'gbk', 'ms936',
        'gb18030', 'gb18030-2000',
        'hz', 'hzgb', 'hz-gb', 'hz-gb-2312',
        'iso2022_jp', 'csiso2022jp', 'iso2022jp', 'iso-2022-jp',
        'iso2022_jp_1', 'iso2022jp-1', 'iso-2022-jp-1',
        'iso2022_jp_2', 'iso2022jp-2', 'iso-2022-jp-2',
        'iso2022_jp_3', 'iso2022jp-3', 'iso-2022-jp-3',
        'iso2022_jp_2004', 'iso2022jp-2004', 'iso-2022-jp-2004',
        'iso2022_jp_ext', 'iso2022jp-etx', 'iso-2022-jp-ext',
        'iso2022_kr', 'csiso2022kr', 'so2022kr', 'iso-2022-kr',
        'johab', 'cp1361', 'ms1361',
        'koi8_r',
        'koi8_t',
        'koi8_u',
        'kz1048', 'kz_1048', 'strk1048_2002', 'rk1048',
        'mac_cyrillic', 'maccyrillic',
        'mac_greek', 'macgreek',
        'mac_iceland', 'maciceland',
        'mac_latin2', 'maclatin2', 'maccentraleurope', 'mac_centeuro',
        'mac_roman', 'macroman', 'macintosh',
        'mac_turkish', 'macturkish',
        'ptcp154', 'csptcp154', 'pt154', 'cp154', 'cyrillic-asian',
        'shift_jis', 'csshiftjis', 'shiftjis', 'sjis', 's_jis',
        'shift_jis_2004', 'shiftjis2004', 'sjis_2004', 'sjis2004',
        'shift_jisx0213', 'shiftjsix0213', 'sjisx0213', 's_jisx0213'
    ]
]

ZWCharacters = [
    ['\u200c','\u200d','\u2060','\ufeff'],
    ['\x00', '\x07', '\x08', '\x09'],
    ['\x80', '\x81', '\x82', '\x83'],
    ['\x00','\x07', '\x0e', '\x0f']
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