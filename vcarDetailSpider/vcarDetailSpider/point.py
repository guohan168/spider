
import os,sys

# 断点管理类
class Point(object):
    # 正常爬取结束标识文件
    overFilePath=None
    # 断点记录文件
    pointFilePath=None

    @classmethod
    def init(cls):
        # 获取当前目录
        path = os.path.abspath(__file__)
        path = path[0:path.rfind("/")]
        # 获取当前目录下所有文件  (('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider', ['__pycache__', 'spiders', 'temp'], ['__init__.py', 'items.py', 'middlewares.py', 'mySqlUtils.py', 'pipelines.py', 'settings.py']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/__pycache__', [], ['__init__.cpython-36.pyc', 'items.cpython-36.pyc', 'mySqlUtils.cpython-36.pyc', 'pipelines.cpython-36.pyc', 'settings.cpython-36.pyc']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/spiders', ['__pycache__'], ['__init__.py', 'detailSpider.py']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/spiders/__pycache__', [], ['__init__.cpython-36.pyc', 'detailSpider.cpython-36.pyc']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/temp', [], ['1.txt']))
        tt = tuple(os.walk(path))
        # 获取当前目录
        currentDir = tt[0][0]
        # 系统文件分隔符
        sep = os.sep
        # 拼接目的文件
        Point.overFilePath = currentDir + sep + "temp" + sep + "over.txt"
        Point.pointFilePath = currentDir + sep + "temp" + sep + "point.txt"


    # 切入断点，返回待爬集合
    @classmethod
    def cutInto(cls,total):
        # 定义最终要爬取的数据集
        waitingCrawlIdSet=None
        # 判断当前目录中是否存在over.text文件
        hasOverFile = os.path.exists(Point.overFilePath)
        # 如果存在结束标识文件则证明上一次完整爬取，删除标识文件和断点文件
        if hasOverFile:
            os.remove(Point.overFilePath)
            # 清空断点文件的内容
            f = open(Point.pointFilePath, "w", encoding="utf-8")
            f.write("")
            f.flush()
            f.close()
            del f
            # 待爬数据就是查询出的全部
            waitingCrawlIdSet = total
        else:
            # 读取断点文件
            pointFile = open(Point.pointFilePath, "r+", encoding="utf-8")
            lines = pointFile.read()
            # 如果行末尾存在逗号，则消除逗号
            if len(lines) - 1 == lines.rfind(","):
                lines = lines[0:lines.rfind(",")]
            # 提取已爬取的车型id，封装成set集合
            crawledIdSet = set(lines.split(","))
            # 用全部爬取id集减去已爬取的的id集得出待爬取的id集
            waitingCrawlIdSet = total - crawledIdSet
            # print(len(DetailPipeline.waitingCrawlIdSet))
            pointFile.close()
            del pointFile
            print("总共需要爬取%s,上次已爬取%s,本次需爬取%s" % (len(total),len(total)-len(waitingCrawlIdSet),len(waitingCrawlIdSet)))
        return waitingCrawlIdSet

    # 记录断点
    @classmethod
    def savePoint(self,data):
        f = open(self.pointFilePath, "a", encoding="utf-8")
        f.write(data)
        f.flush()
        f.close()
        del f



    # 完成爬取
    @classmethod
    def complete(cls):
        overFile = open(cls.overFilePath, "w", encoding="utf-8")
        overFile.write("")
        overFile.flush()
        overFile.close()
        del overFile






