
import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
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
            SELECT  `vcar_pinpai`.`pinpaiID`,`vcar_pinpai`.`name`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            # for item in res:
            #     print(item)
                # self.log(item)
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


    # 将品牌id元组集合转换为品牌id集合
    @classmethod
    def parseBrandTupleListToBrandList(cls,res):
        brandIdSet=set()
        for item in res:
            brandIdSet.add(item[0])
        # print(brandIdSet)
        return brandIdSet




my = MySqlUtils()
# res=my.queryBrandId()
# print(res)
# my.parseBrandTupleListToBrandList(res)
# res=my.queryExistChexingId()
# my.parseChexingIdTupeListToList(res)
# specList=[('1', 'h', 't', '2018款 118i 时尚型', 'https://www.autohome.com.cn/spec/33409/#pvareaid=2042128'), ('2', 'h', 't', '2018款 118i 运动型', 'https://www.autohome.com.cn/spec/33410/#pvareaid=2042128'), ('3', 'h', 't', '2018款 118i 设计套装型', 'https://www.autohome.com.cn/spec/32582/#pvareaid=2042128'), ('4', 'h', 't', '2018款 120i 设计套装型', 'https://www.autohome.com.cn/spec/33411/#pvareaid=2042128'), ('5', 'h', 't', '2018款 125i 运动型', 'https://www.autohome.com.cn/spec/33412/#pvareaid=2042128')]
# MySqlUtils.insertSpecItemList(specList)