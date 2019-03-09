
# 论坛帖子列表爬取

#功能介绍
# 1、论坛断点爬取
# 2、分页断点续爬
# 3、采新设计：当一轮数据全部爬取完毕后再次爬取，只要采集每日新增的帖子即可，不必全部爬取

# 采集数据
# 1、论坛版主数据：版主用户ID，保存到版主表
# 2、论坛图标：更新到论坛表
# 3、合并的车系：保存到论坛车系表
# 4、帖子数据：发帖人、发布时间、帖子标题、点击量、回复量、推荐级别、帖子类型、帖子主页链接：保存到论坛帖子主表
# 5、用户数据：用户id、用户姓名、用户主页链接，保存到用户表


import time,json,re,random,datetime,traceback
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector

class BbsNoteListSelenium(object):
    # 访问某论坛帖子列表host
    bbsNoteHost="https://club.autohome.com.cn/bbs/%s.html"
    bbsNextPageUrl="https://club.autohome.com.cn%s"

    # 程序运行时已爬起的论坛
    crawlingBbsIdSet=set()
    # 断点文件中读取的已爬取论坛id
    crawledBbsIdSet=set()

    #某一论坛下已爬取帖子id集合
    crawledNoteIdSet=set()

    # 插入到论坛帖子主表集合
    insertNoteHeadList=list()
    # 更新到论坛帖子主表集合
    updateNoteHeadList=list()

    # 保存用户集合
    insertUserList=list()
    # 更新用户集合
    updateUserList=list()

    # 版主信息集合
    insertModerList=list()
    updateModerList=list()

    # 保存版主信息计数器
    saveModerCount=0
    updateModerCount=0

    # 保存论坛车系信息计数器
    saveChexiCount=0
    updateChexiCount=0

    # 保存论坛帖子主表计数器
    insertNoteHeadCount=0
    # 更新论坛帖子主表计数器
    updateNoteHeadCount=0

    # 新增用户计数器
    saveUserCount=0



    def __init__(self):
        # 初始化浏览器
        self.browser=webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

        # 初始化论坛表主键id集合
        bbsRes=MySqlUtils.query(MySqlUtils.sql_query_bbs)
        self.bbsIdSet=MySqlUtils.parseToSet(bbsRes,0)

        # 初始化帖子类型枚举值
        noteTypeRes=MySqlUtils.query(MySqlUtils.sql_query_dic % 'qczj_bbs_note_type')
        self.noteTypeDict=MySqlUtils.parseToDict(noteTypeRes,0,1)

        # 初始化帖子推荐级别枚举值
        tuijianLevelRes=MySqlUtils.query(MySqlUtils.sql_query_dic % 'qczj_bbs_note_tuijian_level')
        self.tuijianLevelDic=MySqlUtils.parseToDict(tuijianLevelRes,0,1)


        # 切入论坛断点
        Point.init()
        self.waitingCrawlIdList=Point.cutIntoPagePoint(self.bbsIdSet)



    # 爬虫入口
    def start_request(self):
        # for bbsId in self.bbsIdSet:
        isFirst=True
        for bbsId in self.waitingCrawlIdList:
            # 清空该论坛下已爬取帖子id集合
            self.crawledNoteIdSet.clear()
            # 初始化该论坛下帖子主表中已经存的帖子
            pageId=bbsId
            # 第一次请求可能读取到分页断点
            if isFirst:
                # 如果如果bbsId末尾不为1则为分页
                if bbsId[bbsId.rfind('-')+1:] != '1':
                    # 修改bbsId的值
                    bbsId = bbsId[:bbsId.rfind("-")+1] + "1"
                isFirst=False
            else:
                # 清理上一次积累的分页断点文件
                Point.clearPagePoint()

            print("bbsId:%s ,PageId:%s " % (bbsId,pageId))
            noteHeadRes=MySqlUtils.query(MySqlUtils.sql_query_bbs_note_head % bbsId)
            existNoteIdSet=MySqlUtils.parseToSet(noteHeadRes,0)
            # print(existNoteIdSet)
            url=self.bbsNoteHost % pageId
            # 论坛断点第一次爬取标识
            firstPage=True
            while True:
                try:
                    if not self.request(url):
                        continue

                    #取出page_source
                    page_source = self.browser.page_source
                    # 转selector取值
                    response = Selector(text=page_source)
                    # 解析
                    self.parse(response,bbsId,existNoteIdSet)

                    # 保存分页断点
                    Point.savePagePoint(url[url.rfind("/") + 1:url.rfind(".")]+",")
                    # 第一次进入改论坛，对于只需要解析一次，与分页无关的，过滤分页请求带来的重复解析
                    if firstPage and bbsId[len(bbsId)-1] == '1':
                        # 解析该论坛其它信息，如版主、论坛图标、合并车系
                        self.parseBbsOtherInfo(bbsId)
                        # 如果第一页爬取完成则保存论坛id到断点文件中
                        Point.savePoint(bbsId+",")
                        # 将第一次爬取标识置为false以免重复保存
                        firstPage = False
                    # 打印爬取信息
                    printParams=(self.saveModerCount,self.saveChexiCount,self.insertNoteHeadCount,self.updateNoteHeadCount,self.saveUserCount)
                    print("saveModerCount:%s ,saveChexiCount:%s ,insertNoteHeadCount:%s ,updateNoteHeadCount:%s ,saveUserCount:%s " % printParams)
                    print()
                    # 解析下一页链接
                    url = self.parseNextUrl(response)
                    # 如果存在,继续请求下一页，否则终止分页请求
                    if not url:
                        break
                except Exception as e:
                    print(traceback.format_exc())


        Point.complete()






    # 请求方法
    def request(self,url):
        print(url)
        success = True
        wait = None
        try:
            self.browser.get(url)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tcount')))
            time.sleep(random.randint(1,3))  # 若不加一个会发生页面没有完全渲染
            # print(self.browser.get_cookies())
        except Exception as e:
            print(e)
            success = False
        return success

    def parseNextUrl(self,response):
        # 取出下一页元素
        nextPage=response.css(".afpage")
        nextUrl=None
        if nextPage:
            nextUrl=nextPage.css("::attr(href)").extract_first()
            nextUrl=nextUrl[:nextUrl.rfind("#")]
            return self.bbsNextPageUrl % nextUrl


    # 解析
    def parse(self,response,bbsId,existNoteIdSet):
        contentDlList=response.css("#subcontent dl")

        pageNoteIdSet=set()
        # 用于拼接用户id集合，查询已经存在的用户id
        userIdStr= ""
        # 该页面下所有用户ID集合
        userIdSet=set()
        # 待插入到用户表的参数集合
        insertUserList=list()
        for contentDl in contentDlList:
            # 跳过非帖子内容
            dlClassName=contentDl.css("::attr(class)").extract_first()
            if dlClassName == "list_dl bluebg":
                continue
            # 解析帖子标题
            title=contentDl.css(".a_topic ::text").extract_first().strip()
            # 解析帖子主页链接
            noteLink=contentDl.css(".a_topic ::attr(href)").extract_first()
            # 解析基本信息
            lang=contentDl.css("::attr(lang)").extract_first()
            infoArr=lang.split("|")
            # 解析帖子id
            noteId=infoArr[2]
            # 解析回复量
            replyCount=infoArr[3]
            # 解析发表时间
            publicTime=infoArr[4]
            # 解析用户id
            userId=infoArr[5]
            userIdSet.add(userId)
            userIdStr += userId + ","
            # 解析用户姓名
            userName=infoArr[10]
            insertUserParams=(userId,userName,"//i.autohome.com.cn/%s" % userId,None,None,None)
            insertUserList.append(insertUserParams)

            # 判断当前帖子id是否已经解析过，若之前有解析过则跳过,否则添加集合中代表已解析过
            if noteId in self.crawledNoteIdSet:
                continue
            else:
                self.crawledNoteIdSet.add(noteId)

            # 解析帖子是否是视频
            dataVideo = contentDl.css("dt span ::attr(data-video)").extract_first().strip()
            noteType=None
            if dataVideo == "True":
                noteType = self.noteTypeDict['视频']
            else:
                # 其它类型判断
                # 取出第一个dt下的第一个span的classname
                spanClassName=contentDl.css("dt span ::attr(class)").extract_first()
                # print(spanClassName)
                # 如果不存在则是新贴
                if not spanClassName :
                    noteType=self.noteTypeDict['新贴']
                elif "jing" in spanClassName or "tu" in spanClassName or "jian" in spanClassName:
                    noteType=self.noteTypeDict['新贴']
                elif "wen" in spanClassName:
                    noteType=self.noteTypeDict['提问']
                elif "shou" in spanClassName:
                    noteType=self.noteTypeDict['出售']
                elif "you" in spanClassName:
                    noteType=self.noteTypeDict['游记']
                else:
                    noteType=self.noteTypeDict['新贴']


            # 解析推荐级别
            dtSpanArr=contentDl.css("dt span")
            tuijianLevel=None
            if len(dtSpanArr) >= 2:
                spanClassName=dtSpanArr[1].css("::attr(class)").extract_first()
                if spanClassName:
                    if "zuan" in spanClassName:
                        tuijianLevel=self.tuijianLevelDic['钻石']
            else:
                spanClassName=dtSpanArr[0].css("::attr(class)").extract_first()
                if spanClassName:
                    if "jing" in spanClassName:
                        tuijianLevel=self.tuijianLevelDic['精华']
                    elif 'jian' in spanClassName:
                        tuijianLevel=self.tuijianLevelDic['推荐']

            # 解析是否置顶
            setTopStatus='0'
            spanClassName=contentDl.css("dt span ::attr(class)").extract_first()
            if spanClassName and "0" in spanClassName:
                setTopStatus='1'

            # 解析点击量
            clickCount=contentDl.css(".tcount ::text").extract_first()
            # 解析最后回复时间
            replyTime=contentDl.css('.ttime ::text').extract_first()

            # 将参数封装到集合中
            if noteId not in existNoteIdSet:
                insertParams = (
                noteId, bbsId, userId, title, publicTime, clickCount, replyCount, setTopStatus, noteType, noteLink,
                replyTime,tuijianLevel)
                self.insertNoteHeadList.append(insertParams)
            else:
                updateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updateParams=(clickCount,replyCount,setTopStatus,replyTime,tuijianLevel,updateTime,noteId)
                self.updateNoteHeadList.append(updateParams)

            # print("noteId:%s,bbsId:%s,userId:%s,title:%s,publicTime:%s,clickCount:%s,replyCount:%s,setTopStatus:%s,noteType:%s,noteLink:%s,replyTime:%s" % insertParams)
        # 判重：用户id
        userIdStr = userIdStr[:len(userIdStr)-1]
        userIdRes=MySqlUtils.query(MySqlUtils.sql_query_user_in % userIdStr )
        unexistUserIdSet=None
        if userIdRes:
            existUserIdSet=MySqlUtils.parseToSet(userIdRes,0)
            # 用解析的用户id集合减去已经存在的id集合就是不存在数据库中的用户ID集合
            unexistUserIdSet=userIdSet - existUserIdSet
        else :
            unexistUserIdSet=userIdSet
        # 保存用户
        unExistUserList=list()
        for userId in unexistUserIdSet:
            for params in insertUserList:
                if userId == params[0]:
                    unExistUserList.append(params)
                    break
        MySqlUtils.updateList(MySqlUtils.sql_insert_user,unExistUserList)
        self.saveUserCount += len(unExistUserList)
        # print("saveUserCount-------------------->%s" % self.saveUserCount)



        # 保存到数据库
        self.save()


    # 解析该论坛合并的车系
    def parseBbsOtherInfo(self,bbsId):
        # 查询数据库中已存在的有效版主
        bbsModerRes=MySqlUtils.query(MySqlUtils.sql_query_bbs_moder % (bbsId,'1'))
        existMdoerSet=MySqlUtils.parseToSet(bbsModerRes,0)

        # 取出page_source
        page_source = self.browser.page_source
        # 转selector取值
        response = Selector(text=page_source)
        # 解析论坛图标
        bbsHeadImg=response.css("#_club_logo ::attr(src)").extract_first()
        # 解析论坛版主
        if response.css(".moder span ::text").extract_first().strip() == "版主：":
            # 解析版主信息
            moderList=response.css(".moder a")

            for moderLink in moderList:
                moderName=moderLink.css("::text").extract_first().strip()
                moderHref=moderLink.css("::attr(href)").extract_first().strip()
                if "申请版主" in moderName:
                    break
                userid=re.search(r'\d+',moderHref).group()
                # 解析任职时间
                tenureTime=moderLink.css("::attr(title)").extract_first()
                tenureTime=tenureTime[tenureTime.find(":")+1:]
                tenureTime=tenureTime.replace("/","-")
                # 如果存在于数据库中，且状态为有效，则无需插入或更新，将已存在的版主用户id集合从中删除
                if userid in existMdoerSet:
                    existMdoerSet.remove(userid)
                    continue
                else:
                    # 新增版主
                    sid="%s_%s_%s" % (bbsId,userid,random.randint(10000,99999))
                    insertModerParams=(sid,bbsId,userid,tenureTime)
                    self.insertModerList.append(insertModerParams)
                    # print("sid:%s, bbsId:%s, userId:%s ,tenureTime:%s" % insertModerParams)
            # 若已存在数据中的版主用户id集合中仍有数据，则证明剩下的用户现在已经不是版主了，则改变其版主状态为无效
            if len(existMdoerSet) > 1:
                for existBbsUserId in existMdoerSet:
                    updateParams=('0',bbsId,existBbsUserId)
                    self.updateModerList.append(updateParams)
        else:
            # 该论坛还没有版主
            pass

        # 解析该论坛包含合并的车系
        chexiHrefList=response.css(".clball_pop li a ::attr(href)")
        # 查询该论坛下数据库中已存在的车系集合
        bbsChexiIdRes=MySqlUtils.query(MySqlUtils.sql_query_bbs_chexi % (bbsId,'1'))
        bbsChexiIdSet=MySqlUtils.parseToSet(bbsChexiIdRes,0)
        # 插入论坛车系表集合
        insertBbsChexiList=list()
        updateBbsChexiList=list()
        # 若存在多个链接则证明是多个车系合并，否则就是一个车系
        if len(chexiHrefList) > 1:
            for i,chexiHref in enumerate(chexiHrefList):
                if i != len(chexiHrefList)-1:
                    # 提取车系id
                    href=chexiHref.extract()
                    chexiId=re.search(r'\d+',href).group()
                    if chexiId in bbsChexiIdSet:
                        bbsChexiIdSet.remove(chexiId)
                        continue
                    else:
                        sid="%s_%s_%s" % (bbsId,chexiId,random.randint(10000,99999))
                        insertBbsChexiParams=(sid,bbsId,chexiId)
                        insertBbsChexiList.append(insertBbsChexiParams)
            # 若已存在的车系id集合仍存在车系id，则证明此车系已经不属于该论坛了，则更改其状态
            if len(bbsChexiIdSet) > 0 :
                updateBbsChexiParams=('0',chexiId,bbsId)
                updateBbsChexiList.append(updateBbsChexiParams)
        elif len(chexiHrefList) > 0:
            href=chexiHrefList[0].extract()
            chexiId=re.search(r'\d+',href).group()
            if chexiId not in bbsChexiIdSet:
                sid="%s_%s_%s" % (bbsId,chexiId,random.randint(10000,99999))
                insertBbsChexiParams=(sid,bbsId,chexiId)
                insertBbsChexiList.append(insertBbsChexiParams)

        # 保存车系论坛表
        if len(insertBbsChexiList) > 0:
            self.saveChexiCount += 1
            MySqlUtils.updateList(MySqlUtils.sql_insert_bbs_chexi,insertBbsChexiList)
            insertBbsChexiList.clear()
        if len(updateBbsChexiList) > 0:
            self.updateChexiCount += 1
            MySqlUtils.updateList(MySqlUtils.sql_update_bbs_chexi,updateBbsChexiList)
            updateBbsChexiList.clear()

        # 更新论坛定义表论坛头像
        updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updateBbsImgParams=(bbsHeadImg, updateTime, bbsId)
        MySqlUtils.updateOne(MySqlUtils.sql_update_bbs, updateBbsImgParams)

        # 保存版主信息
        self.saveBbsModer()








    # 保存帖子主表信息到数据库
    def save(self):
        if len(self.insertNoteHeadList) > 0 :
            self.insertNoteHeadCount += len(self.insertNoteHeadList)
            MySqlUtils.updateList(MySqlUtils.sql_insert_bbs_note_head,self.insertNoteHeadList)
            self.insertNoteHeadList.clear()
        if len(self.updateNoteHeadList) > 0:
            self.updateNoteHeadCount += len(self.updateNoteHeadList)
            MySqlUtils.updateList(MySqlUtils.sql_update_bbs_note_head,self.updateNoteHeadList)
            self.updateNoteHeadList.clear()

        # print("insertNoteHeadCount:%s, updateNoteHeadCount:%s" % (self.insertNoteHeadCount,self.updateNoteHeadCount))


    # 保存或更新版主到数据库
    def saveBbsModer(self):
        if len(self.insertModerList) > 0:
            self.saveModerCount += len(self.insertModerList)
            MySqlUtils.updateList(MySqlUtils.sql_insert_bbs_mdoer,self.insertModerList)
            self.insertModerList.clear()

        if len(self.updateModerList) > 0:
            self.updateModerCount += len(self.updateModerList)
            MySqlUtils.updateList(MySqlUtils.sql_update_bbs_moder,self.updateModerList)
            self.updateModerList.clear()
        # print("saveChexiCount:%s,updateChexiCount:%s,saveMdoerCount:%s,updateModerCount:%s" % (self.saveChexiCount,self.updateChexiCount,self.saveModerCount,self.updateModerCount))















import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"


    # 查询用户
    sql_query_user="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_user;
    """
    sql_query_user_in="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_user
                        WHERE
                            sid 
                            in (%s)
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

    # 查询论坛主表
    sql_query_bbs="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_bbs;
    """
    # 插入论坛主表
    sql_insert_bbs="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs`
                            (`sid`,
                            `bbsUrl`,
                            `bbsName`)
                            VALUES(
                            %s,
                            %s,
                            %s);
    """
    # 更新论坛表
    sql_update_bbs="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_bbs`
                        SET
                            `bbsImgUrl` =%s,
                            `updateTime` = %s
                        WHERE `sid` = %s;
    """

    # 查询字典表
    sql_query_dic="""
                        SELECT 
                        optionName, optionValue
                    FROM
                        vcar_vcyber_com.vcar_dic
                    WHERE
                        labelCd = '%s'
    """

    # 插入论坛帖子主表
    sql_insert_bbs_note_head="""
                                INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs_note_head`
                                    (`sid`,
                                    `bbsId`,
                                    `userId`,
                                    `title`,
                                    `publicTime`,
                                    `clickCount`,
                                    `replyCount`,
                                    `setTopStatus`,
                                    `noteType`,
                                    `detaiUrl`,
                                    `lastReplyTime`,
                                    `tuijianLevel`)
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
                                    %s);
    """
    # 更新论坛帖子主表
    sql_update_bbs_note_head="""   
                                UPDATE `vcar_vcyber_com`.`vcar_qczj_bbs_note_head`
                                SET
                                    `clickCount` = %s,
                                    `replyCount` = %s,
                                    `setTopStatus` = %s,
                                    `lastReplyTime` = %s,
                                    `tuijianLevel` = %s,
                                    `updateTime` =%s
                                WHERE `sid` = %s;
    
    """


    # 查询论坛版主
    sql_query_bbs_moder="""
                            SELECT 
                                userId
                            FROM
                                vcar_vcyber_com.vcar_qczj_bbs_moder
                            WHERE
                                bbsId = '%s'
                                and status= '%s';
    """

    # 出入论坛版主
    sql_insert_bbs_mdoer="""
                            INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs_moder`
                        (`sid`,
                        `bbsId`,
                        `userId`,
                        `tenureTime`)
                        VALUES
                        (%s,
                         %s,
                         %s,
                         %s);
    """
    # 更新论坛版主
    sql_update_bbs_moder="""
                            UPDATE vcar_vcyber_com.vcar_qczj_bbs_moder 
                            SET 
                                status = '%s'
                            WHERE
                                bbsId = '%s' AND userId = '%s'
    """

    # 查询论坛车系表
    sql_query_bbs_chexi="""
                            SELECT 
                                chexiId
                            FROM
                                `vcar_vcyber_com`.`vcar_qczj_bbs_chexi`
                            WHERE
                                bbsId = '%s'
                            AND status = '%s'
    """

    # 插入论坛车系表
    sql_insert_bbs_chexi="""
                            INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs_chexi`
                                (`sid`,
                                `bbsId`,
                                `chexiId`)
                                VALUES
                                (%s,
                                %s,
                                %s);
    """
    # 更新论坛车系表
    sql_update_bbs_chexi="""     
                            UPDATE `vcar_vcyber_com`.`vcar_qczj_bbs_chexi` 
                            SET 
                                status = '%s'
                            WHERE
                                chexiId = '%s' AND bbsId = '%s'
    """

    # 查询某论坛下已经存在的帖子id集
    sql_query_bbs_note_head="""
                            SELECT 
                                sid
                            FROM
                                vcar_vcyber_com.vcar_qczj_bbs_note_head
                            WHERE
                                bbsId = '%s'
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


import os,sys
# 断点管理类
class Point(object):
    # 正常爬取结束标识文件
    overFilePath=None
    # 断点记录文件
    pointFilePath=None
    # 分页断点文件
    pagePointPath=None

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
        Point.pagePointPath = currentDir + sep + "temp" + sep + "pagePoint.txt"


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
    def savePoint(cls,data):
        f = open(cls.pointFilePath, "a", encoding="utf-8")
        f.write(data)
        f.flush()
        f.close()
        del f

    # 记录分页断点
    @classmethod
    def savePagePoint(cls,pageId):
        f = open(cls.pagePointPath, "a", encoding="utf-8")
        f.write(pageId)
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

    # 读取分页断点文件，返回分页断点id
    @classmethod
    def getPagePoint(cls):
        pageId=None
        pointFile = open(Point.pagePointPath, "r+", encoding="utf-8")
        lines = pointFile.read()
        # 如果行末尾存在逗号，则消除逗号
        if len(lines) - 1 == lines.rfind(","):
            lines = lines[0:lines.rfind(",")]
            pageIdList=lines.split(",")
            pageId=pageIdList.pop()
        return pageId

    # 清理分页断点文件
    @classmethod
    def clearPagePoint(cls):
        pagePointFile = open(cls.pagePointPath, "w", encoding="utf-8")
        pagePointFile.write("")
        pagePointFile.flush()
        pagePointFile.close()
        del pagePointFile

    # 切入分页断点
    @classmethod
    def cutIntoPagePoint(cls,total):
        idSet=cls.cutInto(total)
        pagePoint=cls.getPagePoint()
        print("切入分页断点--> %s" % pagePoint)
        if pagePoint:
            waitingCrawlIdList=list(idSet)
            # 将分页断点插入到集合第一个元素位置
            waitingCrawlIdList.insert(0,pagePoint)
            return waitingCrawlIdList
        else:
            return idSet




# ids='%s,%s,%s' % ('10000018','10000064','10000098')
# res=MySqlUtils.query(MySqlUtils.sql_query_user_in % ids)
# print(res)
bbsNote=BbsNoteListSelenium()
bbsNote.start_request()

