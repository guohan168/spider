


class UserKouBeiSelenium(object):

    # 爬虫初始化
    def __init__(self):
        # 爬取链接


        pass

    # 爬虫入口
    def start(self):

        pass

    # 请求
    def request(self):

        pass

    # 解析
    def parse(self):

        pass





import pymysql
class MySqlUtils(object):
    # 获取数据库链接
    vcar_host = "10.1.11.129"
    # 查询车型sql
    sql_query_spec="""
                     SELECT 
                            chexingID,
                            chexiID,
                            pinpaiID,
                            name 
                     FROM vcar_vcyber_com.vcar_chexing 
    """

    # 查询字典表
    sql_query_dict="""
                        SELECT 
                            t.optionName, t.optionValue
                        FROM
                            vcar_vcyber_com.vcar_dic t
                        WHERE
                            t.labelCd = '%s'
    """

    # 查询词云表中已爬取的车型
    sql_query_crawled_ciyun="""
                        SELECT DISTINCT
                            (t.chexingId) AS chexingId
                        FROM
                            vcar_vcyber_com.vcar_qczj_ciyun t
    """

    # 插入词云
    sql_insert_ciyun="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_ciyun`
                            (`sid`,
                            `chexingID`,
                            `ciYunType`,
                            `word`,
                            `peopleCount`,
                            `affectiveType`)
                            VALUES
                            (%s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s);
    """

    # 更新词云
    sql_update_ciyun="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_ciyun`
                        SET
                        `ciYunType` =%s,
                        `word` = %s,
                        `peopleCount` = %s,
                        `affectiveType` = %s,
                        `updateTime` = %s
                        WHERE `chexingID`=%s and `ciYunType`=%s;
    """

    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306,
                               charset='utf8')
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

    @classmethod
    def parseToDict(cls,res,keyIndex,valueIndex):
        d=dict()
        for item in res:
            d.__setitem__(item[keyIndex],item[valueIndex])
        return d







