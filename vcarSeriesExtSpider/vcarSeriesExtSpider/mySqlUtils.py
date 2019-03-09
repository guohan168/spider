
import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host='10.1.11.129'
    vcar_password='12345'
    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

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

    # 查询车系id集合
    @classmethod
    def querySeries(cls):
        sql="""
            SELECT chexiID,name 
            FROM vcar_vcyber_com.vcar_chexi;
        """
        try:
            conn = cls.getConnection()
            cur = conn.cursor()
            cur.execute(sql)
            res=cur.fetchall()
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    # 查询保值率表中的车系id
    @classmethod
    def queryKeepValueCheixId(cls):
        sql="""
                SELECT distinct(chexiID) 
                FROM vcar_vcyber_com.vcar_qczj_keep_value;
        """
        try:
            conn = cls.getConnection()
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            # 返回的是列表，列表元素类型是元组[(),(),,]
            return res
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    # 查询已爬取过车系图片且不为空的id集合
    @classmethod
    def querySavedImgChexi(cls):
        sql="""
                SELECT 
                    chexiID, img
                FROM
                    vcar_vcyber_com.vcar_chexi
                WHERE
                    img IS NOT NULL
        """
        try:
            conn = cls.getConnection()
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            # 返回的是列表，列表元素类型是元组[(),(),,]
            return res
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    # 将车系id转为车系id的set集合
    @classmethod
    def parseToChexiIdSet(cls,res):
        chexiIdSet=set()
        for item in res:
            chexiIdSet.add(item[0])
        return chexiIdSet

    # 将查询结果中的ID转为set集合
    @classmethod
    def parseToIdSet(cls,res):
        idSet=set()
        for item in res:
            idSet.add(item[0])
        return idSet





my = MySqlUtils()
# res=my.querySeries()
# chexiSet=my.parseToChexiIdSet(res)
# print(chexiSet)
#my.querySeriesUrls()