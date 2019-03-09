import os
i=0   # 全局变量
class Man(object):
    gender = 'male'          #类变量
    avg_height = 1.75        #类变量
    lis =  ['hello','world'] #类变量

    def __init__(self,name):
        self.name=name       # 实例变量

    @classmethod
    def showLsit(cls):
        print(cls.lis)

    def addV(self):
        self.age=13

a = Man("json")
b = Man('tom')
a.addV()
print(a.age)
print(Man.__dict__)
a.gender='female'    # gender原本是类变量，通过实例变量来取用就变成来实例变量，由于是inmutable不可修改，因此改变值后是实例变量的值，变不会影响到类变量的值
a.sex = '1'          # 实例中不存在sex变量，通过这种形式新增实例变量
b.lis.append('china') # 由于lis是mutable变量，因此改变的就是类变量的值


print(a.__dict__)
print(a.sex)
print("----------")
print(b.__dict__)

print(b.gender)
b.age=30
print(b.age)
print(a.age)
print(Man.gender)
print(Man.lis)
i+=1
print(i)
Man.showLsit()
Man.gender="male888"
print(Man.gender)
b.gender="female888"
print(Man.gender)

os.system('cd /Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarBrandSpider   \n ls  \n scrapy list \n scrapy crawl brandSpider')
