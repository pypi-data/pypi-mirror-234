# 本包是对日常编码中用到的算法的简便方式的封装
# 可能大部分的代码看起来无用
# 但目的是为了提高编码效率，使一些常用算法不用再费劲去再实现一遍
# 部分可能是在互联网中收集到的（如：商密算法系列）

from .base import *
from .json import *

# 16进制的文本转换为整数的算法实现
def hex_to_int(text:str) -> int:
    odata = 0; text = text.upper();
    for c in text:
        tmp = ord(c)
        if tmp <= ord('9'):
            odata = odata << 4; odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4; odata += tmp - ord('A') + 10
    return odata
