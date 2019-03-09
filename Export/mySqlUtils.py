import pymysql
class MySqlUtilsLocal(object):
    #获取数据库链接
    vcar_host="10.1.11.129"

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
            print(sql)
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
            print(sql)
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
            print(sql)
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

    # 解析成list
    @classmethod
    def parseToList(cls,res,index):
        l=list()
        for item in res:
            l.append(item[index])
        return l


class MySqlUtilsRemot(object):
    #获取数据库链接
    vcar_host="10.1.11.129"

    @classmethod
    def getConnection(cls):
        conn = pymysql.connect(host=cls.vcar_host, user='root', passwd='12345', db='vcar_vcyber_com', port=3306, charset='utf8')
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
            print(sql)
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
            print(sql)
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
            print(sql)
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

    # 解析成list
    @classmethod
    def parseToList(cls,res,index):
        l=list()
        for item in res:
            l.append(item[index])
        return l

sql_query="""
select * from %s
"""
sql_insert_bbs_note_head="""
INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs_note_head`
(`sid`,
`bbsId`,
`userId`,
`title`,
`src`,
`publicTime`,
`clickCount`,
`replyCount`,
`setTopStatus`,
`noteType`,
`detaiUrl`,
`lastReplyTime`,
`tuijianLevel`,
`status`,
`createTime`,
`updateTime`)
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
%s
%s
%s
%s);
"""

sql_insert_user="""
INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user`
(`sid`,
`userName`,
`homepageUrl`,
`headImg`,
`sex`,
`provinceCode`,
`province`,
`cityCode`,
`city`,
`countyCode`,
`county`,
`level`,
`registerTime`,
`lastLogin`,
`focusNum`,
`fansNum`,
`kmValue`,
`bestNoteNum`,
`mainNoteNum`,
`prize`,
`status`,
`vStatus`,
`createTime`,
`updateTime`)
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
%s,
%s,
%s,
%s,
%s,
%s,
%s);
"""

sql_insert_qczj_koubei_head="""
INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_head`
(`sid`,
`title`,
`publicTime`,
`userSid`,
`chexingID`,
`buyTime`,
`price`,
`dealerId`,
`province`,
`city`,
`county`,
`currentKm`,
`fuel`,
`koubeiLink`,
`favorNum`,
`readNum`,
`commentNum`,
`koubeiSrc`,
`lastUpdateTime`,
`mjjh`,
`status`,
`createTime`,
`updateTime`)
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
%s,
%s,
%s,
%s,
%s);

"""
sql_insert_qczj_koubei_purpose="""
INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_purpose`
(`sid`,
`koubeiSid`,
`purpose`,
`createTime`,
`updateTime`)
VALUES
(%s,
%s,
%s,
%s,
%s);

"""

sql_insert_qczj_koubei_score="""
INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_koubei_score`
(`sid`,
`koubeiSid`,
`scoreType`,
`score`,
`createTime`,
`updateTime`)
VALUES
(%s,
%s,
%s,
%s,
%s,
%s);

"""
sql_insert_vcar_shuxing="""

"""


# 要导入的表
waitForExportTable=["vcar_qczj_bbs_note_head","vcar_qczj_user","vcar_qczj_user_car","vcar_qczj_koubei_head","vcar_qczj_koubei_purpose","vcar_qczj_koubei_score","vcar_shuxing"]
for tableName in waitForExportTable:
    pass





