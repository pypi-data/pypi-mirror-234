from phapbm import ErrorTemplate

class phap_numalgo_deskcheck_DataNotTrueError(ErrorTemplate):  # 从phapbm包导入错误类模板，具体可见phapbm/__init__.py
    message = "The value is not true."
    info_list = ["Try to change a new value."]

def deskcheck(
        array : list = None,
        start_group : list = [0,0],  # [(0在上 | 1从下), (从左往右数的组数)]
        direction : int = 0,  # 0顺序 1倒回
        group_w : int = 2,
        group_h : int = 2,
        ):  # 一个用于按特定顺序打乱多维数组的函数，暂时不作具体实现
    pass
