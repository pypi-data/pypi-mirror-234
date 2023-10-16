from typing import Any
from phapbm import ErrorTemplate

class ValueTypeError(ErrorTemplate):  # 从phapbm包继承错误类模板，具体可见phapbm/__init__.py
    message = "The value's type must not be treenode."
    info_list = ['Try to change the type to "str" or "int".']

class treenode:  # 二叉树类
    '''This class is used to make treenode easier to call and use'''
    def __init__(self,
                object:object = None,
                list:list = None,
                value:Any = None,
                left:Any = None,
                right:Any = None
                ) -> None:
        if object != None:
            self.set_from_object(value=object)
        elif list != None:
            self.set_from_list(value=list)
        elif ((value != None) and (left != None)) and right != None:
            self.setup(value=value, left=left, right=right)
        else:
            self.reset()

    def reset(self) -> None:
        self.value = 0
        self.left = 0
        self.right = 0

    def setup(self, value:Any = 0, left:Any = 0, right:Any = 0) -> None: # 参数分别是，初始节点参数，初始节点左边和右边的值
        self.__t = [str(self.__class__)]  # 定义一个保护类型的变量，用于识别构造函数参数的类型，用列表方便后期扩展以及其他类继承
        if str(type(value)) in self.__t:  # 如果初始节点参数是二叉树类，则报错
            self.value = 0
            raise ValueTypeError()
        else:
            self.value = value
        self.left = left  # 将本类初始节点的左右侧分别赋值
        self.right = right

    def set_from_object(self, value:object) -> None:
        self.value = object.value
        self.left = object.left
        self.right = object.right

    def set_from_list(self, value:list) -> None:  # 支持从列表设置本二叉树的函数，结构为[参数,左,右]，可嵌套
        '''To set the node from list'''
        self.value = value[0]  # 设置本类初始节点参数
        if str(type(value[1])) == str(type([])):  # 如果初始节点左侧是嵌套的列表
            tmpo = treenode()  # 则创建一个新的本类实例，并将所得列表传参给实例的本函数，并将本类左侧参数赋值
            tmpo.set_from_list(value[1])
            self.left = tmpo
        else:
            self.left = value[1]
        if str(type(value[2])) == str(type([])):  # 原理同上
            tmpo = treenode()
            tmpo.set_from_list(value[2])
            self.right = tmpo
        else:
            self.right = value[2]

    def get_list(self) -> list:  # 从本类获得列表（结构同上）
        l = []  # 定义一个临时的列表
        l.append(self.value)  # 将初始节点参数加入列表
        if str(type(self.left)) in self.__t:  # 如果本类左值的类型也是本类
            l.append(self.left.get_list())  # 则调用该类的本函数取得列表，并加入临时列表
        else:
            l.append(self.left)  # 否则直接加入
        if str(type(self.right)) in self.__t:  # 设置右值原理同上
            l.append(self.right.get_list())
        else:
            l.append(self.right)
        return(l)

    def get_depth(self) -> int:  # 对于depth只读属性的函数封装
        ld = 0
        if str(type(self.left)) in self.__t:  # 统计左树深度，如果左数类型是二叉树，则调用该类统计深度的属性
            ld += self.left.get_depth() + 1
            #print(ld)
        else:  # 否则加一
            ld += 1
        rd = 0
        if str(type(self.right)) in self.__t:  # 原理同上
            rd += self.right.get_depth() + 1
            #print(rd)
        else:
            rd += 1
        return(max(ld, rd))  # 返回左右中的最大值

    def get_node(self) -> str:  # 返回一个简洁明了的二叉树字符串
        #l = self.get_list()
        #return("")
        return(str(self.listdata))  # 临时如此实现，后续改进

    #def get_list_from_depth(self, depth:int) -> list:  # 获取特定深度上的所有内容
    #    if self.depth > depth:
    #        pass
    #    elif self.depth == depth:
    #        pass
    #    else:
    #        return(None)

    #def __eq__(self, value:object) -> bool:  # 简化赋值的运算符重载
    #    try:
    #        if str(type(value)) in self.__t:  # 如果赋值表达式的右值为二叉树类
    #            self.value = value.value  # 从该类获取必要信息并赋值本类
    #            self.left = value.left
    #            self.right = value.right
    #        else:  # 否则调用setfromlist函数
    #            self.set_from_list(value)
    #    except:
    #        return(False)
    #    else:
    #        return(True)
    
    #def __setattr__(self, __name: str, __value: Any) -> None:  # 用于对一些关键的常量禁止赋值
    #    pass

    def set_from_obj(self, value:object) -> None:
        return(self.set_from_object(value=value))

    def setfromobject(self, value:object) -> None:
        return(self.set_from_object(value=value))

    def setfromobj(self, value:object) -> None:
        return(self.set_from_object(value=value))

    def set_up(self, value:Any = 0, left:Any = 0, right:Any = 0) -> None:
        return(self.setup(value=value, left=left, right=right))

    def setfromlist(self, value:list) -> None:
        return(self.set_from_list(value=value))

    @property
    def listdata(self) -> list:  # 用于获取数的列表信息的只读属性
        return(self.get_list())
    
    @property
    def list_data(self) -> list:
        return(self.get_list())

    def getlist(self) -> list:
        return(self.get_list())

    #def __getitem__(self, key:int) -> list:
    #    return(self.get_list_from_depth(key))

    @property
    def depth(self) -> int:  # 用于获取数的深度信息的只读属性
        return(self.get_depth())
    
    def getdepth(self) -> int:
        return(self.get_depth())

    @property
    def node(self) -> str:
        return(self.get_node())

    def getnode(self) -> str:
        return(self.get_node())

    def __str__(self) -> str:  # 使开发者可以直接使用print函数打印二叉树
        return(self.get_node())
