# -*- coding: utf-8 -*-

class OriObj(object):
    
    def __init__(self):
        self.s = 0
    
    def some_method(self, arg):
        print('这是原始方法:', arg)
        
    def step(self, a):
        print('s before step:', self.s)
        self.s += a
        print('s after step:', self.s)
        
        
class Wrapper(object):
    
    def __init__(self, ori_obj):
        self.ori_obj = ori_obj
        
    def some_method(self, arg):
        print('这是Wrapper中的方法')
        
        # 调用原始对象的方法
        self.ori_obj.some_method(arg)
        
    def step(self, a):
        return self.ori_obj.step(a)


# 使用包装器对原始对象进行包装
wrapobj = Wrapper(OriObj())

# 调用包装对象的方法
wrapobj.some_method('参数')

# 调用step
wrapobj.step(1)
# 手动修改s
wrapobj.s = 3
# 再次调用step查看修改的s是否有效
wrapobj.step(6)
# 手动修改原始obj的s
wrapobj.ori_obj.s = 4
# 再次调用查看修改的s是否有效
wrapobj.step(5)









