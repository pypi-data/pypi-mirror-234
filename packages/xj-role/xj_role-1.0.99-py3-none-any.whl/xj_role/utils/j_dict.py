# _*_coding:utf-8_*_

class JDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    # 是否允许点操作符
    def allow_dotting(self, state=True):
        print("> allow_dotting:", self, state)
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()

    # 属性引用。当值不存在时返回None
    def __getattr__(self, *args):
        pass

    # 索引。当索引不存在时返回None
    def __getitem__(self, item):
        # print("> __getitem__:", self, item, getattr(self, item, None))
        return getattr(self, item, None)

    # 索引赋值。不需要，默认已经赋值了
    def __setitem__(self, key, value):
        # print("> __setitem__:", self, key, value, type(value))
        if type(value) == dict:
            value = JDict(value)
        setattr(self, key, value)
