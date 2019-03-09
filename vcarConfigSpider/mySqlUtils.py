
import pymysql,timeit
class MySqlUtils(object):
    errorModel = "{count:%s,class:%s,method:%s,errorInfo:%s}"
    errorCount=0
    vcar_host="10.1.11.129"
    var_password='12345'
    #获取数据库链接
    @classmethod
    def getConnection(cls):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

    @classmethod
    def queryBrandId(cls):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = cls.getConnection()
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
    def querySeriesLink(cls):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=cls.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
            #    print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 查询车型链接信息
    @classmethod
    def querySpecLink(self):
        sql = """
                SELECT `vcar_chexing`.`chexingID`,
                        `vcar_chexing`.`pinpaiID`,
                        `vcar_chexing`.`chexiID`,
                        `vcar_chexing`.`name`,
                        `vcar_chexing`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexing`;
        """
        try:
            conn = self.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            # for item in res:
            #     print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()


    #返回一个以属性id为key，属性名为value的字典
    @classmethod
    def queryShuxing(cls):
        sql="""
                SELECT `vcar_shuxing`.`shuxingID`,
                       `vcar_shuxing`.`name`
                FROM `vcar_vcyber_com`.`vcar_shuxing`;
            """
        try:
            if id:
                conn=cls.getConnection()
                cursor=conn.cursor()
                cursor.execute(sql)
                res=cursor.fetchall()
                #转为Dic数据类型
                shuxingDic=dict()
                for item in res:
                    shuxingDic.setdefault(item[1],item[0])
                return shuxingDic
            else:
                return None
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()


    # 查询属性类型表返回以属性名作为key，属性id为value的字典
    @classmethod
    def queryShuxingType(cls):
        sql="""
                SELECT 
                    `vcar_shuxingtype`.`name`,
                    `vcar_shuxingtype`.`shuxingTypeID`
                  FROM `vcar_vcyber_com`.`vcar_shuxingtype`;
        """
        try:
            conn=cls.getConnection()
            cursor=conn.cursor()
            cursor.execute(sql)
            res=cursor.fetchall()
            #转Dict数据类型
            typeDict=dict()
            for item in res:
                typeDict.setdefault(item[0],item[1])
            return typeDict
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 查询属性type下的属性集合{shuxingType:{shuxingName:shuxingValue,,,},,,}
    @classmethod
    def queryTypeShuxingDic(cls):
        typeDic=cls.queryShuxingType()
        sql="""
                 SELECT `vcar_shuxing`.`shuxingID`,
                       `vcar_shuxing`.`name`
                 FROM `vcar_vcyber_com`.`vcar_shuxing` 
                 where shuxingTypeID=%s       
        """
        typeShuxingDic=dict()
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            for key in typeDic.keys():
                typeId=typeDic.get(key)
                cursor.execute(sql,typeId)
                res=cursor.fetchall()
                shuxingDic=dict()
                for item in res:
                    shuxingDic.setdefault(item[1],item[0])
                typeShuxingDic.setdefault(key,shuxingDic)
            return typeShuxingDic
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 插入到属性表
    @classmethod
    def insertIntoShuxing(cls,params):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_shuxing`
                    (`shuxingID`,
                    `shuxingTypeID`,
                    `name`)
                    VALUES
                    (%s,
                    %s,
                    %s);
        """
        try:
            conn=cls.getConnection()
            cursor=conn.cursor()
            res=cursor.executemany(sql, params)
            conn.commit()
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()


    @classmethod
    def queryChexingShuxingById(cls,id):
        startTime=timeit.default_timer()
        sql="""
                SELECT 
            `vcar_chexingshuxing`.`chexingID`
        FROM `vcar_vcyber_com`.`vcar_chexingshuxing`
        where chexingID=%s;
        """
        try:
            conn=cls.getConnection()
            cursor=conn.cursor()
            cursor.execute(sql,id)
            res=cursor.fetchone()
            endTime=timeit.default_timer()
            print("queryIsInsertCastTime------------------->: %s" % str(endTime-startTime))
            if res:
                return True
            else:
                return False
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertOneShuxing(cls,params):
        sql="""
            INSERT INTO `vcar_vcyber_com`.`vcar_shuxing`
                (`shuxingID`,
                `shuxingTypeID`,
                `name`)
                VALUES
                (%s,
                 %s,
                 %s);
        """
        try:
            conn=cls.getConnection()
            cursor=conn.cursor()
            i=cursor.execute(sql, params)
            conn.commit()
            return i
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    #向车型属性表中插入数据
    @classmethod
    def insertChexingShuxing(cls, paramsList):
        startTime=timeit.default_timer()
        sql="""
                INSERT INTO 
                    `vcar_vcyber_com`.`vcar_chexingshuxing`
                    (`chexingshuxingID`,
                    `chexingID`,
                    `shuxingID`,
                    `shuxingName`,
                    `shuxingValue`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            #print(paramsList)
            res =cursor.executemany(sql,paramsList)
            conn.commit()
            endTime = timeit.default_timer()
            print("insertChexingShuxingCastTime------------------------>:%s" % str(endTime-startTime))
        except Exception as e:
            print(e)
            cls.errorCount+=1
            filename = "/Users/guohan/DeskTop/mySqlError.txt"
            error=cls.errorModel % (cls.errorCount,"MySqlUtils","insertChexingShuxing",str(e))
            with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(error)
                f.flush()
                f.close()
        finally:
            conn.close()
            cursor.close()


    # 查询已爬取过配置的车型id
    @classmethod
    def queryExistChexingId(cls):
        sql="""     
            SELECT distinct(t.chexingID) 
            FROM vcar_vcyber_com.vcar_chexingshuxing t 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            # 提交
            conn.commit()
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 将上一个查询车型id方法返回值转换为list
    @classmethod
    def parseChexingIdTupeListToSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        print(chexingIdSet)
        
        
    
#
# my = MySqlUtils()
# res=my.queryExistChexingId()
# my.parseChexingIdTupeListToSet(res)
# name="基本参数"
# typeDict=my.queryShuxingType()
# keys=typeDict.keys()
# # for key in keys:
# #     print(key,typeDict[key])
# shuxingDict=my.queryShuxing()
# shuxingKeys=shuxingDict.keys()
# for key in shuxingKeys:
#     print(key,shuxingDict[key])
# typeDic=MySqlUtils.queryShuxingType()
# print(typeDic)
# print(MySqlUtils.queryTypeShuxingDic())
