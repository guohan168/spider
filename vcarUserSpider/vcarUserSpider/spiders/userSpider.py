
import scrapy,pymysql,re,time,requests,datetime,random
from ..mySqlUtils import MySqlUtils
from ..point import Point
from ..items import UserItem
from ..pipelines import UserPipeline
from ..addressUtils import AddressUtils
class UserSpider(scrapy.Spider):

    name = "userSpider"
    userHomeLink="https://i.autohome.com.cn/%s"

    # 更新用户集合
    updateUserList=list()

    # 用户认证车辆集合
    userCarDict=dict()

    # 保存认证车型计数器
    saveVCarCount=0
    # 更新认证车型计数器
    updateVCarCount=0

    # 统计一共需要请求的用户数
    userCount=0





    # 请求入口
    def start_requests(self):
        # 读取断点文件，读取最后一个爬取的用户id
        Point.init()
        lastUserId=Point.cutIntoLastElement()
        self.log("----------------->lastUserId: %s" % lastUserId)
        # 如果存在userid，则从该userid的日期处开始统计剩余爬取用户
        createTime=None
        if lastUserId:
            createTime=MySqlUtils.query(MySqlUtils.sql_query_user_one % lastUserId)[0][1]
            print("---------------->createTime:%s" % createTime)
            UserPipeline.initUserCount=MySqlUtils.query(MySqlUtils.sql_query_user_count % createTime)[0][0]
        else:
            # 若断点文件中不存在用户id则证明第一次爬取或则已经爬取结束重头再爬
            createTime='2000-01-01'
            UserPipeline.initUserCount=MySqlUtils.query(MySqlUtils.sql_query_user_count % createTime)[0][0]

        # 计算分页
        pageCount=round(UserPipeline.initUserCount/10000) +1
        pageEnd=0
        for page in range(1,pageCount):
            pageStart=pageEnd
            pageEnd=page * 10000
            # 查询当前页所有用户ID
            userIdRes=MySqlUtils.query(MySqlUtils.sql_query_user_page % (createTime,pageStart,pageEnd))
            userIdList=MySqlUtils.parseToList(userIdRes,0)
            # 一次性查询该10000个用户的所有认证车辆，返回以用户id为key，认证车辆list集合为value的字典
            self.userCarDict=self.queryUserCar(userIdList)
            for userId in userIdList:
                # 请求当前用户主页
                url = self.userHomeLink % userId
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['userId']=userId
                time.sleep(0.1)
                yield request




    # 解析
    def parse(self, response):
        userId = response.meta['userId']
        # 解析用户昵称
        userName=response.css(".user-name b ::text").extract_first()
        # 解析用户头像
        headImg=response.css(".userHead a img ::attr(src)").extract_first()
        # 解析用户等级
        levelImg=response.css(".member-level a img ::attr(src)").extract_first()
        # self.log("levelImg:::::::::: %s" % levelImg)
        level=re.search(r'\d+',levelImg).group()
        # 解析用户性别
        sex=None
        if len(response.css(".man")) > 0:
            sex= 'm'
        if len(response.css(".woman")) > 0:
            sex = 'f'
        # 解析关注人数
        attentionNum=response.css(".state-mes span ::text")[0].extract()
        # 解析粉丝人数
        fansNum=response.css(".state-mes span ::text")[1].extract()
        # 解析用户地点
        pos=response.css(".state-pos ::text").extract_first()
        province,provinceCode,city,cityCode = self.getFullAddr(pos)

        # 解析用户车库,车库采用ajax异步加载，因此需要调用ajax获取车库信息
        carCount,carSet=self.sendAjaxToGetCars(userId)
        # 保存认证车辆

        # 判断是否车主认证
        vStatus = '0'
        if int(carCount) > 0:
            vStatus = '1'
        # 更新时间
        updateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 封装参数
        item = UserItem()
        item['sid']=userId
        item['headImg']=headImg
        item['sex']=sex
        item['province']=province
        item['provinceCode']=provinceCode
        item['city']=city
        item['cityCode']=cityCode
        item['level']=level
        item['focusNum']=attentionNum
        item['fansNum']=fansNum
        item['vStatus']=vStatus
        item['updateTime']=updateDate
        # self.log(item)

        # 保存或更新用户车辆认证
        self.saveUserCar(userId,carSet)


        yield item





    # 发送ajax获取车库信息
    def sendAjaxToGetCars(self,userId):
        params = {"appname": "Car", "TuserId": userId}
        url = "https://i.autohome.com.cn/ajax/home/OtherHomeAppsData"
        headers = self.setRequestHeaders(userId)
        r = requests.get(url=url, params=params, headers=headers)
        j = r.json()
        carCount=j['ConcernCount']
        carSet=set()
        if int(carCount) > 0:
            # 取出车型id
            for item in j['ConcernInfoList']:
                chexinId=item['SpecId']
                carSet.add(chexinId)
        return carCount,carSet


    # 设置请求头
    def setRequestHeaders(self,userId):
        headers = dict()
        headers.__setitem__("Host", "i.autohome.com.cn")
        headers.__setitem__("User-Agent",
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:64.0) Gecko/20100101 Firefox/64.0")
        headers.__setitem__("Accept", "*/*")
        headers.__setitem__("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
        headers.__setitem__("Accept-Encoding", "gzip, deflate, br")
        headers.__setitem__("Referer", "https://i.autohome.com.cn/%s" % userId)
        headers.__setitem__("X-Requested-With", "XMLHttpRequest")
        headers.__setitem__("Connection", "keep-alive")
        headers.__setitem__("Pragma", "no-cache")
        headers.__setitem__("Cache-Control", "no-cache")
        return headers

    def getFullAddr(self,pos):
        province=None
        provinceCode=None
        city=None
        cityCode=None
        # pos的值可能是类似安徽 合肥，也可能是 北京，规律为第一个是省，第二个如果不为空则为市，没有县
        posArr=pos.strip().split(" ")
        # 为省市组合,第一个为省，第二个为市，根据省查询省代码
        province, provinceCode, city, cityCode=AddressUtils.parseProvinceAndCity(pos,None)
        # if len(posArr) > 1:
        #     province,provinceCode,city,cityCode,countyName,countyCode=AddressUtils.parseProvinceCityCount(title=pos,content=pos)
        # provinceRes = MySqlUtils.query(MySqlUtils.sql_query_province_like % posArr[0])
        # if provinceRes:
        #     provinceCode=provinceRes[0][0]
        #     province = provinceRes[0][1]
        # # 查询市
        # if len(posArr) > 1:
        #     cityRes=MySqlUtils.query(MySqlUtils.sql_query_city_like % posArr[1])
        #     if cityRes:
        #         cityCode=cityRes[0][0]
        #         city=cityRes[0][1]
        # print(province,provinceCode,city,cityCode)
        return province,provinceCode,city,cityCode






    # 根据用户id集合一次性查询用户认证车辆,返回一个以用户id为key，用户车型idList为value的字典
    def queryUserCar(self,userIdList):
        # 拼接查询参数字符串
        userIds=""
        for userId in userIdList:
            userIds += userId + ","
        # 去除逗号
        userIds=userIds[:userIds.rfind(",")]
        # in查询
        userCarRes = MySqlUtils.query(MySqlUtils.sql_query_user_car_in % userIds)
        userCarDict=dict()
        if userCarRes:
            for userCar in userCarRes:
                userId=userCar[0]
                specId=userCar[1]
                # 如果字典中已经存在该key了，则在已经存在的value值中追加
                if userCarDict.get(userId):
                    userCarDict.setdefault(userId,userCarDict.get(userId).add(specId))
                else:
                    # 若字典中不存在，则新建集合为value值，插入值后添加到字典中
                    carSet = set()
                    carSet.add(specId)
                    userCarDict.__setitem__(userId,carSet)
        return userCarDict

    # 保存或更新用户车辆认证
    def saveUserCar(self,userId,carSet):
        # 定义更新认证车型集合和插入认证车型集合
        updateSpecList=None
        insertSpecList=None


        # 如果存在于用户字典表中用户id，则比较是否有取消认证和新增认证的车辆
        existCarSet=self.userCarDict.get(userId)

        for newSpecId in carSet:
            find=False

            if existCarSet:

                for existSpecId in existCarSet:
                    if int(existSpecId) == int(newSpecId) :
                        find=True
                        existCarSet.remove(existSpecId)
                        break

            if not find:
                # 如果没有找到证明是新增
                sid="%s_%s_%s" % (userId,newSpecId,random.randint(10000,99999))
                insertParams=(sid,userId,newSpecId)
                if insertSpecList == None:
                    insertSpecList=list()
                    insertSpecList.append(insertParams)
                else:
                    insertSpecList.append(insertParams)
        # 如果已存在的认证车型集合中仍有数据，则代表用户已经取消该车型认证，修改该车型认证状态为0
        if existCarSet and len(existCarSet) > 0:
            for existSpecId in existCarSet:
                updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updateParams=('0',updateTime,userId,existSpecId)
                if updateSpecList == None:
                    updateSpecList = list()
                    updateSpecList.append(updateParams)
                else:
                    updateSpecList.append(updateParams)
        # 保存认证车型
        if insertSpecList:
            MySqlUtils.updateList(MySqlUtils.sql_insert_user_car,insertSpecList)
            self.saveVCarCount += len(insertSpecList)
            self.log("saveVcar=========================> %s" % self.saveVCarCount)
        # 更新认证车型
        if updateSpecList:
            MySqlUtils.updateList(MySqlUtils.sql_update_user_car,updateSpecList)
            self.updateVCarCount += len(updateSpecList)
            self.log("updateVCarCount>>>>>>>>>>>>>>>>>>> %s" % self.updateVCarCount)











   






