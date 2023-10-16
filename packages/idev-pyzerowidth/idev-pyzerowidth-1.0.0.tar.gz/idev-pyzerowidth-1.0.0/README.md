# **PyZeroWidth**
A simple set of functions in [**python**](https://www.python.org) for encoding messages into **zero-width** characters.
<br />
<br />
​<br />
# Installation
With `git` [GitHub](https://github.com):
```
git clone https://github.com/IrtsaDevelopment/PyZeroWidth.git
```
With `pip` [PyPi](https://pypi.org/project/idev-pyzerowidth/)
```
pip install idev-pyzerowidth
```
<br />
<br />
<br />
<br />
<br />

# Usage
To import:
```py
from PyZeroWidth import encode
from PyZeroWidth import decode
```
<br />
<br />
<br />
<br />

### Encoding Functions
```py
encode.binary8(message: str, secret: str, encoding: str = 'utf') -> str
encode.binary16(message: str, secret: str, encoding: str = 'utf') -> str
encode.binary24(message: str, secret: str, encoding: str = 'utf') -> str
# Encoding functions that encodes the 'secret' into binary, then into corresponding zero-width characters depending on the encoding provided.
# Binary8 can represent the first 256 (0-255) characters in the encoding codec provided.
# Binary16 can represent the first 65536 (0-65535) characters in the encoding codec provided.
# Binary24 can represent the first 16777216 (0-16777215) characters in the encoding codec provided.


encode.trinary6(message: str, secret: str, encoding: str = 'utf') -> str
encode.trinary11(message: str, secret: str, encoding: str = 'utf') -> str
encode.trinary16(message: str, secret: str, encoding: str = 'utf') -> str
# Encoding functions that encodes the 'secret' into trinary, then into corresponding zero-width characters depending on the encoding provided.
# Trinary6 can represent the first 256 (0-255) characters in the encoding codec provided.
# Trinary11 can represent the first 65536 (0-65535) characters in the encoding codec provided.
# Trinary16 can represent the first 16777216 (0-16777215) characters in the encoding codec provided.


encode.quaternary4(message: str, secret: str, encoding: str = 'utf') -> str
encode.quaternary8(message: str, secret: str, encoding: str = 'utf') -> str
encode.quaternary12(message: str, secret: str, encoding: str = 'utf') -> str
# Encoding functions that encodes the 'secret' into quaternary, then into corresponding zero-width characters depending on the encoding provided.
# Quaternary4 can represent the first 256 (0-255) characters in the encoding codec provided.
# Quaternary8 can represent the first 65536 (0-65535) characters in the encoding codec provided.
# Quaternary12 can represent the first 16777216 (0-16777215) characters in the encoding codec provided.
```
<br />

### Decoding Functions
```py
decode.binary8(message: str, encoding: str = 'utf') -> str
decode.binary16(message: str, encoding: str = 'utf') -> str
decode.binary24(message: str, encoding: str = 'utf') -> str
# Decoding functions that decodes the 'message' attempting to find zero-width characters encoded in a binary format.
# Binary8 will expect the message to be encoded using the binary8 encode function and as such characters being represented with 8 digits.
# Binary16 will expect the message to be encoded using the binary16 encode function and as such characters being represented with 16 digits.
# Binary24 will expect the message to be encoded using the binary24 encode function and as such characters being represented with 24 digits.


decode.trinary6(message: str, encoding: str = 'utf') -> str
decode.trinary11(message: str, encoding: str = 'utf') -> str
decode.trinary16(message: str, encoding: str = 'utf') -> str
# Decoding functions that decodes the 'message' attempting to find zero-width characters encoded in a trinary format.
# Trinary6 will expect the message to be encoded using the trinary6 encode function and as such characters being represented with 6 digits.
# Trinary11 will expect the message to be encoded using the trinary11 encode function and as such characters being represented with 11 digits.
# Trinary16 will expect the message to be encoded using the trinary16 encode function and as such characters being represented with 16 digits.


decode.quaternary4(message: str, encoding: str = 'utf') -> str
decode.quaternary8(message: str, encoding: str = 'utf') -> str
decode.quaternary12(message: str, encoding: str = 'utf') -> str
# Decoding functions that decodes the 'message' attempting to find zero-width characters encoded in a quaternary format.
# Quaternary4 will expect the message to be encoded using the quaternary4 encode function and as such characters being represented with 4 digits.
# Quaternary8 will expect the message to be encoded using the quaternary8 encode function and as such characters being represented with 8 digits.
# Quaternary12 will expect the message to be encoded using the quaternary12 encode function and as such characters being represented with 12 digits.
```
​
<br />
<br />
<br />
<br />
# Additional Notes
Only a few encoding formats are currently supported.
> UTF-8 (utf, utf8, utf-8, u8, cp65001)

> ASCII (ascii, us-ascii, 646)

> LATIN (latin, latin1, latin-1, iso-8859-1, iso8859-1, 8859, cp819)
