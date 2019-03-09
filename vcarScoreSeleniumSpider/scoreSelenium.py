

import time,json,re,random,datetime
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector

class AutoSelenium(object):
    requestCount=0
    # 爬取链接,占位符为车型id
    kouBeiUrl = "https://k.autohome.com.cn/spec/%s"
    # 分页url
    nextPageUrl="https://k.autohome.com.cn/spec/%s%s"
    # 全部车型id
    chexingIdSet=None
    # 批量保存到数据库
    scoreSaveList=list()
    # 批量更新到数据库
    scoreUpdateList=list()
    # 已保存过的车型id集合
    savedChexingIdSet=None
    # 用于更新车型表平均能耗的数据集合
    updateSpecAvgFuelList=list()

    # 更新用户集合
    updateUserList=list()
    # 插入用户集合
    insertUserList=list()
    # 运行时保存的用户集合
    crawlingUserIdSet=set()

    # 插入经销商集合
    insertDealerList=list()
    # 正在爬取中的经销商id集合
    crawlingDealerIdSet=set()
    # 插入用户评分集合
    insertUserScoreList=list()


    # 插入口碑主表集合
    insertKoubeiHeadList=list()
    # 更新口碑主标集合
    updateKoubeiHeadList=list()
    # 已经保存到数据库的口碑id集合
    existKoubeiHeadIdSet=set()

    # 插入购车用途集合
    insertCarPurposeList=list()

    # 断点功能用待爬取车型id集合
    waitingCrawlIdSet=None
    # 断点功能用已爬取车型id集合
    crawledIdSet=set()


    # 车型爬取计数器
    specCount=0
    # 保存用户统计
    userCount=0
    # 保存经销商统计
    dealerCount=0
    # 保存口碑主表统计
    koubeiHeadCount=0
    # 更新口碑主表统计
    updateKoubeiCount=0
    # 保存用户评分统计
    userScoreCount=0
    # 保存购车目的统计
    purposeCount=0


    # 评分类别元组，与scoreItem对应：(spaceScore, powerScore, operateScore, fuelScore, comfortScore, appearanceScore, interiorScore, costScore)
    scoreTupe=()


    def __init__(self):
        # 初始化seleniume
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        # 初始化全部车型id集合
        specRes=MySqlUtils.querySpec()
        self.chexingIdSet=MySqlUtils.parseToChexingIdSet(specRes)
        # 初始化分数类型枚举
        scoreTypeRes=MySqlUtils.queryEnum('qczj_score')
        self.scoreType=MySqlUtils.parseEnum(scoreTypeRes)
        self.scoreType.__setitem__("能耗",4)
        self.scoreType.__setitem__("电耗",4)
        self.scoreType.__setitem__("耗电量",4)
        # 初始化已爬取车型id
        savedScoreRes=MySqlUtils.querySavedScoreSepc()
        self.savedChexingIdSet=MySqlUtils.parseToChexingIdSet(savedScoreRes)
        # 初始化购车类型字典
        carPurposeRes=MySqlUtils.queryEnum('qczj_car_purpose')
        self.carPurposeDict=MySqlUtils.parseEnum(carPurposeRes)

        # 查询所有的用户，用于判重
        userRes=MySqlUtils.query(MySqlUtils.sql_query_user)
        self.existUserIdSet=MySqlUtils.parseToSet(userRes,0)

        # 初始化已经存在于经销商表中的经销商id集合
        dearlerRes=MySqlUtils.query(MySqlUtils.sql_query_dealer)
        self.existDealerIdSet=MySqlUtils.parseToSet(dearlerRes,0)

        # 初始化已经存在于数据库中的口碑主表id
        koubeiHeadRes=MySqlUtils.query(MySqlUtils.sql_query_koubei_head)
        self.existKoubeiId=MySqlUtils.parseToSet(koubeiHeadRes,0)

        # 初始化已经存在于用户评分表中的口碑id
        userScoreRes=MySqlUtils.query(MySqlUtils.sql_query_user_score)
        self.existUserScoreKoubeiIdSet = MySqlUtils.parseToSet(userScoreRes,0)


        # 初始化断点
        Point.init()
        # 切入断点
        self.waitingCrawlIdSet=Point.cutInto(self.chexingIdSet)


    def start_requests(self):
        for chexingId in self.waitingCrawlIdSet:
        # for chexingId in ['23009']:
            # 已爬取的id保存到已爬取的id集合中
            self.crawledIdSet.add(chexingId)
            self.specCount += 1
            # 拼接请求链接
            url = self.kouBeiUrl % chexingId
            while True:
                # 请求链接
                if not self.requestConfigLink(url):
                    # 请求超时，证明没有数据，返回请求下一个
                    print("请求超时")
                    # 超时原因是由于验证没有通过而导致，可以不保存到已爬集合中，当爬完结束后并不会生成over断点文件，因此再次启动时就会将超时的车型再爬一遍，从而提高数据的完整度
                    self.crawledIdSet.remove(chexingId)
                    self.specCount -= 1
                    break
                # 解析
                # 取出page_source
                page_source = self.browser.page_source
                # 转selector取值
                response = Selector(text=page_source)
                # 解析平均分
                # self.parseAvgScore(response,chexingId)
                # 解析用户、购买信息、经销商、评分、购车用途
                self.parse(response,chexingId)
                # self.parseUserCar(response,chexingId)
                # self.parseDealer(response)
                # self.parseScoreDetail(response,chexingId)
                # 解析下一页
                url=self.parseNextPageUrl(response,chexingId)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~url:%s" % url)
                if url == None:
                    break
            # 将爬取过的车型id记录到断点文件中,每爬取10个车型保存一次
            if len(self.crawledIdSet) > 10:
                crawledIdSetCopy = self.crawledIdSet.copy()
                self.crawledIdSet.clear()
                Point.savePointFromSet(crawledIdSetCopy)
        # 出循环爬取结束，完成断点，关闭浏览器
        Point.savePointFromSet(self.crawledIdSet)
        if self.specCount >= len(self.waitingCrawlIdSet):
            Point.complete()
        self.browser.close()



    def requestConfigLink(self, url):
        success=True
        wait=None
        try:
            #configUrl="https://car.autohome.com.cn/config/spec/20211.html" #该请求没有配置数据
            self.requestCount+=1
            self.browser.get(url)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.date-ul.fn-left')))
            time.sleep(random.randint(1,3))  # 若不加一个会发生页面没有完全渲染
        except Exception as e:
            print(e)
            success=False
        if not success:
            try:
                ele = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
                ele.click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.date-ul.fn-left')))
                success=True
            except Exception as e:
                success = False
        return success



    # 解析所有用户对车型的平均评分
    def parseAvgScore(self, response,chexingId):
        # 取出参与评分人数:font-arial red font-16
        numPeople = response.css(".font-arial.red.font-16 ::text").extract_first()
        # 取出平均油耗:font-arial font-number
        avgPower=response.css(".font-arial.font-number ::text").extract_first()
        # 取出车型代表图片小图
        imgUrlS = response.css(".appraise-cont-dl.fn-left img::attr(src)").extract_first()

        # 添加到待保存的集合中
        if avgPower or numPeople or imgUrlS:
            updateDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.updateSpecAvgFuelList.append((avgPower,numPeople,updateDate,imgUrlS,chexingId))

        # 取出评分明细类目
        ulArr = response.css(".date-ul.fn-left")
        for ul in ulArr:
            for i, li in enumerate(ul.css("li")):
                if i == 0:
                    continue
                # 取出当前类别值
                optionName = li.css(".width-01 ::text").extract_first()
                optionName = optionName.rstrip()
                optionName = optionName.lstrip()

                # 取出当前类别的评分
                optionValue = li.css(".width-02 ::text").extract_first()
                optionValue = optionValue.rstrip()
                optionValue = optionValue.lstrip()
                if optionValue == "-":
                    optionValue = None
                    break


                # 取出当前类别的高于／低于
                # 取值
                cpValue = li.css(".width-03").xpath("string(.)").extract_first()
                cpValue = cpValue.rstrip()
                cpValue = cpValue.lstrip()
                cpValue = re.search(r'\d+(\.\d+)?', cpValue)
                if cpValue:
                    cpValue = cpValue.group()
                # 判断是否存在子元素i
                if li.css(".width-03 i"):
                    # 根据css名称 判断高于低于
                    cssClassName = li.css(".width-03 i::attr(class)").extract_first()
                    pcssName, subCssName = cssClassName.split(" ")
                    if subCssName == 'icon-dy':
                        cpValue = -1 * float(cpValue)


                scoreType=self.scoreType[optionName]
                sid=chexingId + "_" + str(random.randint(100000, 999999))
                if chexingId in self.savedChexingIdSet:
                    updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.scoreUpdateList.append((optionValue,cpValue,updateTime,chexingId,scoreType))
                else:
                    self.scoreSaveList.append((sid,chexingId,scoreType,optionValue,cpValue))

            # 保存到数据库,当爬取接近尾声时，每个车型保存一次，否则多个车型批量保存
            if self.specCount > len(self.chexingIdSet) - 100:
                self.updateSpecScore()

            else:
                if len(self.scoreSaveList) >= 100 or len(self.scoreUpdateList) >= 100 :
                    self.updateSpecScore()


    # 解析入口
    def parse(self,response,chexingId):
        updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 解析平均分
        # self.parseAvgScore(response,chexingId)

        # 一个页面多条口碑，解析口碑div集合
        mouthconDivs=response.css(".mouthcon")
        for mouthDiv in mouthconDivs:

            # 解析用户信息 # print("userid:%s,name:%s,homepage:%s,img:%s" % (userid, userName, userPage, headImgUrl))
            userid, userName, userPage ,headImgUrl = self.parseUserInfo(mouthDiv)

            # 解析经销商信息 # print("city:%,county:%s,dealerName:%s,dealerId:%s,dealerHomePage:%s" % (city,county,dealerName,dealerId,dealerHomePage))
            city, county, dealerName, dealerId, dealerHomePage = self.parseDealer(mouthDiv)

            # 解析购买时间、购买价格、油耗、行驶里程;空间、动力、操控、油耗、舒适性、外观、内饰、性价比;购车目的集合
            # carItem = (price, buyTime, fuel, currentKm)
            # scoreItem = (spaceScore, powerScore, operateScore, fuelScore, comfortScore, appearanceScore, interiorScore, costScore)
            carItem, scoreItem, carPurposeList = self.parseScoreItem(mouthDiv)

            # 解析口碑主键、口碑链接、口碑主题、口碑第一次发表时间、口碑来源 、阅读人数、评论人数、支持人数、满级精华标识
            koubeiSid, koubeiTitle, publicTime, koubeiLink, koubeiSrc, readNum, commentNum, favorNum,mjjh = self.parseKoubei(mouthDiv)


            # 保存口碑主表,若已存在则更新
            if koubeiSid not in self.existKoubeiId:
                insertKoubeiParams = (
                koubeiSid, koubeiTitle, publicTime, userid, chexingId, carItem[1], carItem[0], dealerId, city, county,
                carItem[3], carItem[2], koubeiLink, favorNum, readNum, commentNum, koubeiSrc,mjjh)
                self.insertKoubeiHeadList.append(insertKoubeiParams)
            else:
                self.updateKoubeiCount += 1
                updateKoubeiParams = (
                carItem[3], carItem[2], favorNum, readNum, commentNum, updateTime, mjjh, koubeiSid)
                self.updateKoubeiHeadList.append(updateKoubeiParams)


            # 保存用户信息
            if userid not in self.existUserIdSet and userid not in self.crawlingUserIdSet:
                insertUserParams = (userid, userName, userPage, headImgUrl, city, county)
                self.insertUserList.append(insertUserParams)
                self.crawlingUserIdSet.add(userid)

            # 保存用户评分和购车用途信息
            if scoreItem or carPurposeList:
                if koubeiSid not in self.existUserScoreKoubeiIdSet:
                    # 保存用户评分
                    for item in scoreItem:
                        userScoreSid=userid+"_"+chexingId+"_"+koubeiSid+"_"+str(random.randint(100000,999999))
                        insertUserScoreParams=(userScoreSid,koubeiSid,item[0],item[1])
                        self.insertUserScoreList.append(insertUserScoreParams)
                    # 保存购车用途
                    for purposeVal in carPurposeList:
                        purposeSid=userid+"_"+chexingId+"_"+koubeiSid+"_"+str(random.randint(100000,999999))
                        insertPurposeParams=(purposeSid,koubeiSid,purposeVal)
                        self.insertCarPurposeList.append(insertPurposeParams)

            # 保存经销商信息集合中
            if dealerId:
                if dealerId not in self.existDealerIdSet and dealerId not in self.crawlingDealerIdSet:
                    insertDealerParams = (dealerId,dealerName,dealerHomePage,city,county)
                    self.insertDealerList.append(insertDealerParams)
                    self.crawlingDealerIdSet.add(dealerId)
            # print("buyTime:%s,price:%s,fuel:%s,currentKm:%s" % (
            # buyTime.strftime("%Y-%m-%d %H:%M:%S"), price, fuel, currentKm))
            # print("spaceScore:%s,powerScore:%s,operateScore:%s,fuelScore:%s,comfortScore:%s,appearanceScore:%s,interiorScore:%s,costScore:%s" % (
            #     spaceScore, powerScore, operateScore, fuelScore, comfortScore, appearanceScore, interiorScore,
            #     costScore))


            # print("koubeiSid:%s,koubeiTitle%s,publicTime:%s,koubeiSrc:%s,koubeiLink:%s" % (koubeiSid,koubeiTitle,publicTime,koubeiSrc,koubeiLink))
            # print("favorNum:%s,readNum:%s,commentNum:%s" % (favorNum,readNum,commentNum))

            # 存入用户集合
            userParams=(userid,userName,userPage,headImgUrl,city,county)
            # self.saveToUserList(userParams)

        # 出循环一个页面解析完成，当爬到末尾时逐条保存，否则批量保存
        self.save()








    # 解析用户信息
    def parseUserInfo(self,mouthDiv):
        nameText = mouthDiv.css(".name-text")
        userName = nameText.xpath("string(.)").extract_first().strip()
        userPage = nameText.css("a ::attr(href)").extract_first().strip()
        userid = userPage[userPage.rfind("/") + 1:]
        headImgUrl = mouthDiv.css(".name-pic img::attr(data-src)").extract_first()
        return userid,userName,userPage,headImgUrl


    # 解析经销商信息
    def parseDealer(self,mouthDiv):
        # 解析地带呢
        county = None
        city = None
        place = mouthDiv.css(".c333 ::text").extract_first().strip()
        placeSplit = place.split(" ")
        if len(placeSplit) > 1:
            city = placeSplit[0]
            county = placeSplit[1]
        else:
            city = place

        # 解析经销商
        dealerLink = mouthDiv.css(".js-dearname ::attr(href)").extract_first()
        # print("dealerLink:%s" % dealerLink)
        dealerId = None
        dealerName=None
        dealerHomePage = None
        if dealerLink:
            # 获取经销商id
            dealerId = dealerLink[dealerLink.rfind("/") + 1:dealerLink.rfind("#")]
            # # 经销商主页
            dealerHomePage = dealerLink[:dealerLink.rfind("#")]
            dealerName=mouthDiv.css(".js-dearname ::text").extract_first().strip()

        return city,county,dealerName,dealerId,dealerHomePage


    # 解析口碑概要信息
    def parseKoubei(self,mouthDiv):
        koubeiSrc = None
        titleItem = mouthDiv.css(".title-name.name-width-01")
        # 解析口碑来源
        koubeiSrcText = titleItem.css("span ::text").extract_first()
        if koubeiSrcText:
            koubeiSrc = koubeiSrcText.split("：")[1]
        # 解析发表时间
        publicTime = titleItem.css("b a::text").extract_first()
        # 解析口碑链接
        koubeiLink = titleItem.css("b a::attr(href)").extract_first()
        # 解析口碑id
        koubeiSid = koubeiLink[koubeiLink.rfind("_") + 1:koubeiLink.rfind(".")]
        # 解析口碑主题
        koubeiTitle = None
        if len(titleItem.css("a ::text")) > 1:
            koubeiTitle=titleItem.css("a ::text")[1].extract()
        helpDiv = mouthDiv.css(".help")
        # 解析评论人数
        commentNum = helpDiv.css(".font-arial.CommentNumber ::text").extract_first().strip()
        # 解析支持人数
        favorNum = helpDiv.css(".supportNumber ::text").extract_first().strip()
        # 解析阅读人数
        readNum = helpDiv.css(".orange ::text").extract_first().strip()
        # 解析满级精华
        mjjh=mouthDiv.css(".mjjh-icon ::attr(src)").extract_first()
        # 解析首页推荐
        sytj=mouthDiv.css(".sytj-icon ::attr(src)").extract_first()
        if mjjh:
            # 截取精华数字
            mjjh=mjjh[mjjh.rfind("-")+1:mjjh.rfind(".")]
        if sytj:
            # 转换首页推荐为数字
            sytj=0
        if mjjh and sytj:
            mjjh=mjjh+","+sytj



        return koubeiSid,koubeiTitle,publicTime,koubeiLink,koubeiSrc,readNum,commentNum,favorNum,mjjh


    # 解析购买价格、评分明细、及购车用途信息
    def parseScoreItem(self,mouthDiv):
        buyTime = None
        price = None
        fuel = None
        currentKm = None

        spaceScore = None
        powerScore = None
        operateScore = None
        fuelScore = None
        comfortScore = None
        appearanceScore = None
        interiorScore = None
        costScore = None

        carPurposeList = list()
        dlArr = mouthDiv.css(".choose-dl")
        for dl in dlArr:
            # 解析左侧标签名称
            labelName = dl.css("dt ::text").extract_first().strip()
            # print(labelName)
            # print("type:",type(labelName))
            # 如果没有取到标签名则证明是油耗及行驶里程二合一标签
            if labelName == None or labelName == "":
                doubleLabel = dl.css("dt p::text")
                doubleValue = dl.css("dd p::text")
                # print("doubleLabelLength:%s" % len(doubleLabel))
                # print(doubleLabel)
                # print("doubleValueLength:%s" % len(doubleValue))
                # print(doubleValue)
                for i, label in enumerate(doubleLabel):
                    labelText = label.extract().strip()
                    if "油耗" == labelText or "能耗" == labelText or "电耗" == labelText:
                        fuel = doubleValue[i].extract().strip()
                    if "目前行驶" == labelText:
                        currentKm = doubleValue[i].extract().strip()
                continue

            labelName.strip()
            if "购买时间" == labelName:
                dateStr = dl.css("dd ::text").extract_first().strip()
                buyTime = datetime.datetime.strptime(dateStr, '%Y年%m月')  # 若出现插入数据库报错，需要格式化成字符串
                continue
            if "裸车购买价" == labelName:
                price = dl.css("dd ::text").extract_first().strip()
                continue

            scoreValue = dl.css(".font-arial.c333 ::text").extract_first()
            if scoreValue:
                labelName = labelName.strip()
                scoreValue.strip()
                # print("labelName:%s" % labelName)
                # print(labelName == "油耗")
                if "空间" == labelName:
                    spaceScore =(self.scoreType['空间'], scoreValue)
                if "动力" == labelName:
                    powerScore = (self.scoreType['动力'], scoreValue)
                if "操控" == labelName:
                    operateScore = (self.scoreType['操控'], scoreValue)
                if "油耗" == labelName or "能耗" == labelName or "电耗" == labelName or "耗电量" == labelName:
                    fuelScore = (self.scoreType['油耗'],scoreValue)
                if "舒适性" == labelName:
                    comfortScore = (self.scoreType['舒适性'],scoreValue)
                if "外观" == labelName:
                    appearanceScore = (self.scoreType['外观'],scoreValue)
                if "内饰" == labelName:
                    interiorScore = (self.scoreType['内饰'],scoreValue)
                if "性价比" == labelName:
                    costScore = (self.scoreType['性价比'],scoreValue)

            # 解析购车目的
            if "购车目的" == labelName:
                purposeArr = dl.css("p ::text")
                for purpose in purposeArr:
                    purpose=purpose.extract().strip()
                    purposeVal=self.carPurposeDict[purpose]
                    carPurposeList.append(purposeVal)

        carItem = (price, buyTime, fuel, currentKm)
        scoreItem = (spaceScore, powerScore, operateScore, fuelScore, comfortScore, appearanceScore, interiorScore, costScore)
        return carItem,scoreItem,carPurposeList


    # 保存入口
    def save(self):
        # 当爬取接近尾声时，每次保存一次，否则为集合中的元素大于100时再做批量保存
        if self.requestCount > len(self.waitingCrawlIdSet) -100:
            self.saveAll()
        else:
            # 保存或更新用户
            if len(self.insertUserList) > 100 or len(self.updateUserList) > 100:
                self.userCount += len(self.insertUserList)
                self.saveList(insertList=self.insertUserList,updateList=self.updateUserList,insertSql=MySqlUtils.sql_insert_user,updateSql=MySqlUtils.sql_update_user)
            # 保存经销商
            if len(self.insertDealerList) > 100 :
                self.dealerCount += len(self.insertDealerList)
                self.saveList(insertList=self.insertDealerList,updateList=None,insertSql=MySqlUtils.sql_insert_dealer,updateSql=None)
            # 保存或更新口碑主表
            if len(self.updateKoubeiHeadList) > 100 or len(self.insertKoubeiHeadList) > 100:
                self.koubeiHeadCount += len(self.insertKoubeiHeadList)
                self.saveList(insertList=self.insertKoubeiHeadList,updateList=self.updateKoubeiHeadList,insertSql=MySqlUtils.sql_insert_koubei_head,updateSql=MySqlUtils.sql_update_koubei_head)
            # 保存用户口碑评分
            if len(self.insertUserScoreList) > 100:
                self.userScoreCount += len(self.insertUserScoreList)
                self.saveList(insertList=self.insertUserScoreList,updateList=None,insertSql=MySqlUtils.sql_insert_koubei_score,updateSql=None)
            #  保存用户购车目的
            if len(self.insertCarPurposeList) > 100:
                self.purposeCount += len(self.insertCarPurposeList)
                self.saveList(insertList=self.insertCarPurposeList,updateList=None,insertSql=MySqlUtils.sql_insert_koubei_purpose,updateSql=None)

    # 批量保存
    def saveList(self,insertList,updateList,insertSql,updateSql):
        flag=False
        if insertList and len(insertList) > 0:
            MySqlUtils.updateList(insertSql,insertList)
            insertList.clear()
            flag=True
        if updateList and len(updateList) > 0:
            MySqlUtils.updateList(updateSql,updateList)
            updateList.clear()
            flag=True
        print("userCount:%s,dealerCount:%s,koubeiHeadCount:%s,userScoreCount:%s,purposeCount:%s,updateKoubeiCount:%s" % (
            self.userCount, self.dealerCount, self.koubeiHeadCount, self.userScoreCount, self.purposeCount,self.updateKoubeiCount))
        return flag


    # 按次保存
    def saveAll(self):
        # 保存用户
        if len(self.insertUserList) > 0:
            self.userCount += len(self.insertUserList)
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_user,paramsList=self.insertUserList)
            self.insertUserList.clear()
        # 更新用户
        if len(self.updateUserList) > 0:
            MySqlUtils.updateList(sql=MySqlUtils.sql_update_user,paramsList=self.updateUserList)
            self.updateUserList.clear()

        # 保存经销商
        if len(self.insertDealerList) > 0 :
            self.dealerCount += len(self.insertDealerList)
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_dealer,paramsList=self.insertDealerList)
            self.insertDealerList.clear()

        # 保存用户口碑主表
        if len(self.insertKoubeiHeadList) >0:
            self.koubeiHeadCount += len(self.insertKoubeiHeadList)
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_koubei_head,paramsList=self.insertKoubeiHeadList)
            self.insertKoubeiHeadList.clear()
        # 更新用户口碑主表
        if len(self.updateKoubeiHeadList) >0:
            MySqlUtils.updateList(sql=self.updateKoubeiHeadList,paramsList=self.updateKoubeiHeadList)
            self.updateKoubeiHeadList.clear()

        # 保存用户口碑评分
        if len(self.insertUserScoreList) > 0:
            self.userScoreCount += len(self.insertUserScoreList)
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_koubei_score,paramsList=self.insertUserScoreList)
            self.insertUserScoreList.clear()

        # 保存购车目的
        if len(self.insertCarPurposeList) > 0:
            self.purposeCount += len(self.insertCarPurposeList)
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_koubei_purpose,paramsList=self.insertCarPurposeList)
            self.insertCarPurposeList.clear()

        print("userCount:%s,dealerCount:%s,koubeiHeadCount:%s,userScoreCount:%s,purposeCount:%s,updateKoubeiCount:%s" % (self.userCount,self.dealerCount,self.koubeiHeadCount,self.userScoreCount,self.purposeCount,self.updateKoubeiCount))


    # 解析下一页链接
    def parseNextPageUrl(self,response,chexingId):
        nexPageUrl=response.css(".page-item-next ::attr(href)").extract_first()
        if nexPageUrl:
            page=nexPageUrl[nexPageUrl.rfind("/"):nexPageUrl.rfind("#")]
            if page != '':
                return self.nextPageUrl % (chexingId, page)
        return None



    # 更新车型平均评分表；更新车型表车型缩略图、油耗、评论人数
    def updateSpecScore(self):
        print("--------------------->save:%s,update:%s,updateAvg:%s" % (len(self.scoreSaveList),len(self.scoreUpdateList),len(self.updateSpecAvgFuelList)))
        # 插入评分表
        if len(self.scoreSaveList) > 0:
            scoreListCopy = self.scoreSaveList.copy()
            self.scoreSaveList.clear()
            MySqlUtils.saveSpecDetailScore(scoreListCopy)

        # 更新评分表
        if len(self.scoreUpdateList) > 0:
            scoreUpdateListCopy = self.scoreUpdateList.copy()
            self.scoreUpdateList.clear()
            MySqlUtils.updateSpecDetailScore(scoreUpdateListCopy)

        # 更新车型表平均油耗、评论人数、车型缩略图
        if len(self.updateSpecAvgFuelList) > 0:
            avgFuelListCopy = self.updateSpecAvgFuelList.copy()
            self.updateSpecAvgFuelList.clear()
            MySqlUtils.updateSpecAvgFuel(avgFuelListCopy)


    # 判重方法
    def verify(self,idStr,idSet,paramsList,idIndex,sql):
        idStr = idStr[:len(idStr) - 1]
        idRes = MySqlUtils.query(sql % idStr)
        unexistIdSet = None
        if idRes:
            existIdSet = MySqlUtils.parseToSet(idRes, 0)
            # 用解析的用户id集合减去已经存在的id集合就是不存在数据库中的用户ID集合
            unexistIdSet = idSet - existIdSet
        else:
            unexistIdSet = idSet
        # 保存用户
        unExistParamsList = list()
        for id in unexistIdSet:
            for params in paramsList:
                if id == params[idIndex]:
                    unExistParamsList.append(params)
                    break
        return unExistParamsList




import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    # 更新车型表中平均油耗、车型缩略图、评论人数
    sql_update_chexing_imgs_fuel_num="""
    UPDATE `vcar_vcyber_com`.`vcar_chexing`
                SET
                    `avgFuel` =  %s,
                    `numPeople` = %s,
                    `updateTime` = %s,
                    `imgUrlS` = %s
                WHERE `chexingID` = %s;
    """

    # 查询用户评分
    sql_query_user_score="""
                            SELECT 
                                koubeiSid
                            FROM
                                vcar_vcyber_com.vcar_qczj_user_koubei_score;
    """

    # 插入用户平均评分
    sql_insert_avg_score="""
                         INSERT INTO `vcar_vcyber_com`.`vcar_qczj_score_chexing`
                                        (`sid`,
                                        `chexingID`,
                                        `scoreType`,
                                        `score`,
                                        `compareScore`)
                                        VALUES
                                        (%s,
                                        %s,
                                        %s,
                                        %s,
                                        %s);
    """
    # 更新用户平均评分
    sql_update_avg_score="""
                         UPDATE `vcar_vcyber_com`.`vcar_qczj_score_chexing`
                         SET
                               `score` = %s,
                               `compareScore` = %s,
                               `updateTime` = %s
                         WHERE `chexingID` = %s and scoreType= %s;
    """

    # 查询用户
    sql_query_user="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_user;
    """
    # 更新用户
    sql_update_user="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_user`
                        SET
                            `userName` = %s,
                            `headImg` = %s,
                            `updateTime` = %s
                        WHERE `sid` = %s;
    """
    # 插入用户
    sql_insert_user="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user`
                        (`sid`,
                        `userName`,
                        `homepageUrl`,
                        `headImg`,
                        `city`,
                        `county`)
                        VALUES
                        (%s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s);
    """

    # 查询经销商表
    sql_query_dealer="""
                        SELECT 
                            sid 
                        FROM vcar_vcyber_com.vcar_qczj_dealer;
    """

    # 插入经销商表
    sql_insert_dealer="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_dealer`
                        (`sid`,
                        `dealerName`,
                        `homepageUrl`,
                        `city`,
                        `county`)
                        VALUES
                        (%s,
                        %s,
                        %s,
                        %s,
                        %s
                        );
    """

    # 查询口碑主表
    sql_query_koubei_head="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_user_koubei_head;
    """

    # 插入口碑主表
    sql_insert_koubei_head="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_head`
                        (`sid`,
                        `title`,
                        `publicTime`,
                        `userSid`,
                        `chexingID`,
                        `buyTime`,
                        `price`,
                        `dealerId`,
                        `city`,
                        `county`,
                        `currentKm`,
                        `fuel`,
                        `koubeiLink`,
                        `favorNum`,
                        `readNum`,
                        `commentNum`,
                        `koubeiSrc`,
                        `mjjh`)
                        VALUES
                        (%s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s);
    """
    # 更新口碑主表
    sql_update_koubei_head="""
                            UPDATE `vcar_vcyber_com`.`vcar_qczj_user_koubei_head`
                            SET
                                `currentKm` = %s,
                                `fuel` = %s,
                                `favorNum` = %s,
                                `readNum` = %s,
                                `commentNum` = %s,
                                `updateTime` = %s,
                                `mjjh` = %s
                            WHERE `sid` = %s;
    """

    # 插入购车用途
    sql_insert_koubei_purpose="""
                                INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_purpose`
                                    (`sid`,
                                    `koubeiSid`,
                                    `purpose`)
                                    VALUES
                                    (%s,
                                    %s,
                                    %s);
    """

    # 插入评分明细表
    sql_insert_koubei_score="""
                                INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_score`
                                    (`sid`,
                                    `koubeiSid`,
                                    `scoreType`,
                                    `score`)
                                    VALUES
                                    (%s,
                                    %s,
                                    %s,
                                    %s);
    """

    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn


    @classmethod
    def query(cls,sql):
        try:
            # 获取链接
            conn = cls.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res=cursor.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 批量更新或保存
    @classmethod
    def updateList(cls,sql,paramsList):
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql, paramsList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 只更新一个
    @classmethod
    def updateOne(cls,sql,params):
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql, params)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 将查询结果解析成id集合
    @classmethod
    def parseToSet(cls,res,index):
        idSet=set()
        for item in res:
            idSet.add(item[index])
        return idSet
    # 解析成字典
    @classmethod
    def parseToDict(cls,res,keyIndex,valueIndex):
        d=dict()
        for item in res:
            d.__setitem__(item[keyIndex],item[valueIndex])
        return d


    @classmethod
    def queryBrandId(self):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            sql="""
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            #print(e)
            #self.log(e)
            #self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        #self.log("end query ----------------------------------")


    #查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(self):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=self.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
                #print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertSpecItemList(cls,itemList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                    (`chexingID`,
                    `pinpaiID`,
                    `chexiID`,
                    `name`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
            """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,itemList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def querySpec(cls):
        sql="""
            SELECT 
                chexingID,
                chexiID,
                pinpaiID,
                name 
            FROM vcar_vcyber_com.vcar_chexing 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 查询枚举表
    @classmethod
    def queryEnum(cls,labelCd):
        sql="""
                SELECT 
                    optionName, optionValue
                FROM
                    vcar_vcyber_com.vcar_dic
                WHERE
                    labelCd = '%s';
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql % labelCd)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 将车型评分批量保存到数据库
    @classmethod
    def saveSpecDetailScore(cls,scoreList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_qczj_score_chexing`
                    (`sid`,
                    `chexingID`,
                    `scoreType`,
                    `score`,
                    `compareScore`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,scoreList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 更新车型评分
    @classmethod
    def updateSpecDetailScore(cls,updateList):
        sql="""
                UPDATE `vcar_vcyber_com`.`vcar_qczj_score_chexing`
                SET
                `score` = %s,
                `compareScore` = %s,
                `updateTime` = %s
                WHERE `chexingID` = %s and scoreType= %s;
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,updateList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 查询车型评分表，查询出所有的已保存的车型id
    @classmethod
    def querySavedScoreSepc(cls):
        sql="""
                SELECT DISTINCT
                    (chexingID) AS chexingID
                FROM
                    vcar_vcyber_com.vcar_qczj_score_chexing;
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 更新车型平均油耗
    @classmethod
    def updateSpecAvgFuel(cls,paramsList):
        # (None, None, '2018-10-12 16:54:11', 'https:https://car2.autoimg.cn/cardfs/product/g30/M0A/D3/4C/t_autohomecar__ChsEf1uEBSuAHcMXAAj-04onwvc092.jpg', '1006690'
        sql=""" 
                UPDATE `vcar_vcyber_com`.`vcar_chexing`
                SET
                    `avgFuel` =  %s,
                    `numPeople` = %s,
                    `updateTime` = %s,
                    `imgUrlS` = %s
                WHERE `chexingID` = %s;
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,paramsList)
            # 提交
            conn.commit()
        except Exception as e:
            print("error:updateSpecAvgFuel")
            print(e)
        finally:
            cursor.close()
            conn.close()





    # 将车型元组集合转换为车型IDset集合
    @classmethod
    def parseToChexingIdSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        return chexingIdSet

    # 将车系元组集合转换成车系ID集合
    @classmethod
    def parseToSeriesIdSet(cls,res):
        seriesIdSet=set()
        for item in res:
            seriesIdSet.add(item[1])
        return seriesIdSet

    # 查询车系id集合中的车系数据
    @classmethod
    def findChexiInChexiSet(cls,seriesItems,seriesIdSet):
        waitingCrawlItems=list()
        for id in seriesIdSet:
             for item in seriesItems:
                 if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        return waitingCrawlItems;

    @classmethod
    def parseEnum(cls,res):
        enumDic=dict()
        for item in res:
            enumDic.__setitem__(item[0],item[1])
        return enumDic








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
        print("--------------------cutInto--------------")

        # 定义最终要爬取的数据集
        waitingCrawlIdSet=None
        # 判断当前目录中是否存在over.text文件
        hasOverFile = os.path.exists(Point.overFilePath)
        # 如果存在结束标识文件则证明上一次完整爬取，删除标识文件和断点文件
        if hasOverFile:
            print(Point.overFilePath)
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

    # 记录断点，传入一个集合
    @classmethod
    def savePointFromSet(cls,setData):
        data=""
        for id in setData:
            data += id + ","
        Point.savePoint(data)



    # 完成爬取
    @classmethod
    def complete(cls):
        overFile = open(cls.overFilePath, "w", encoding="utf-8")
        overFile.write("")
        overFile.flush()
        overFile.close()
        del overFile










se=AutoSelenium()
se.start_requests()

