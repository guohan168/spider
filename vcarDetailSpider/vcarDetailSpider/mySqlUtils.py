
import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    var_password="12345"
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



    #查询车型链接信息
    @classmethod
    def querySpecLink(self):
        sql="""
                SELECT `vcar_chexing`.`chexingID`,
                        `vcar_chexing`.`pinpaiID`,
                        `vcar_chexing`.`chexiID`,
                        `vcar_chexing`.`name`,
                        `vcar_chexing`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexing`;
        """
        try:
            conn=self.getConnection()
            cursor=conn.cursor()
            cursor.execute(sql)
            res=cursor.fetchall()
            # for item in res:
            #     print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def parseToSpecIdSet(self,res):
        idSet=set()
        for item in res:
            idSet.add(item[0])
        return idSet

# my = MySqlUtils()
# res=my.querySpecLink()
# idSet=my.parseToSpecIdSet(res)
# print(idSet)
