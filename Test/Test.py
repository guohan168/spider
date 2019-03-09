class Foo(object):

    @staticmethod
    def spam(x,y,z):
        print(x,y,z)
"""
print(type(Foo.spam))
Foo.spam(3,4,5)
f1=Foo()
f1.spam(1,2,3)
"""

class A(object):
    x=1
    @classmethod
    def test(cls):
        print(cls,cls.x)

class B(A):
    x=2
    y=3

B.test()