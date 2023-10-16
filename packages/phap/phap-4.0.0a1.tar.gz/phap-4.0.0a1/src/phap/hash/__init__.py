# 本包是关于一些哈希算法的集合

# 从本包重要模块导入
from .sha import *
from .sm import *

# md5算法的实现
from hashlib import md5 as _m5

def md5(data:bytes) -> str:
    return(_m5(data).hexdigest())

def text_md5(text:str, encoding:str="utf-8") -> str:
    return(md5(text.encode(encoding)))
t_md5 = text_md5
