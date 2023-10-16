# 本模块是关于json数据结构的转换的结合

from json import dumps as _jec
from json import loads as _jdc

def encode(data) -> str:
    return(_jec(data))

def decode(jsontext : str):
    return(_jdc(jsontext))
