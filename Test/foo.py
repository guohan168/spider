class Foo:
    def __init__(self,val,age):
        self.__NAME=val
        self.__AGE=age

    @property
    def name(self):
        return self.__NAME;
    @property
    def age(self):
        return self.__AGE

    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError('%s must be str' % value)
        self.__NAME=value

    @age.setter
    def age(self,value):
        if not isinstance(value,int):
            raise TypeError("%s must be int" % value)
        self.__AGE=value

    @name.deleter
    def name(self):
        raise TypeError('Can not delete')




# f=Foo('guohan',30)
# print(f.name)
# f.name="hanhan"
# print(f.name)
# f.age=25
# print(f.age)
# del f.name


class Foo2(object):
      def __init__(self,val):
          self.__NAME=val #将所有的数据属性都隐藏起来

      def getname(self):
          return self.__NAME #obj.name访问的是self.__NAME(这也是真实值的存放位置)

      def setname(self,value):
          if not isinstance(value,str):  #在设定值之前进行类型检查
             raise TypeError('%s must be str' %value)
          self.__NAME=value #通过类型检查后,将值value存放到真实的位置self.__NAME

      def delname(self):
         raise TypeError('Can not delete')

      name=property(getname,setname,delname) #不如装饰器的方式清晰

f2=Foo2("guohan")
f2.setname("hanhan")
print(f2.name)