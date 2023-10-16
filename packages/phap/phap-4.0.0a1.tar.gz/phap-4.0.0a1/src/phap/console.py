# 本包是用于实现一些有利于控制台应用编程的算法

# 本函数用于将输入的命令行参数序列化为标准的键值字典
def cut_args(
        argv:list,  # 用于传入参数集合列表
        cmd_begin:list = ["-", "--", "/"],  # 用于定义参数开关符的列表
        max_begin_long:int = 2,  # 参数开关符的最长长度
        self_tip:str = "@self",  # 用于存放程序本体路径参数
        notiparg_tip:str = "@noname"  # 用于定义没有键的值所用列表的键名
    ) -> dict:
    d = {}
    d = d | {self_tip : argv[0], notiparg_tip:[]}
    del argv[0]
    i = 0
    while i < len(argv):
        s = ""
        t = False
        for j in range(len(cmd_begin)):
            if j in argv[i][0:max_begin_long:]:
                s = j
                t = True
        tmp = argv[i]
        if t:
            tmp = s.join(tmp.split(s))
            try:
                d = d | {tmp:argv[i+1]}
            except:
                d[tmp] = argv[i+1]
            i += 1
        else:
            d[notiparg_tip] = d[notiparg_tip] + [argv[i]]
        i += 1
    return(d)
