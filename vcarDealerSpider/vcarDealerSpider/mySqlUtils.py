import pymysql
class MySqlUtils(object):
    # 获取数据库链接
    vcar_host = "10.1.11.129"

    # 查询品牌表
    sql_query_brand = """
                        SELECT 
                            pinpaiID,name
                        FROM
                            vcar_vcyber_com.vcar_pinpai;
    """

    # 插入品牌表
    sql_insert_brand = """
                        INSERT INTO `vcar_vcyber_com`.`vcar_pinpai`
                    (`pinpaiID`,
                    `szm`,
                    `name`,
                    `imgUrl`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
    """

    # 查询车系表
    sql_query_chexi = """
                        SELECT 
                            chexiID
                        FROM
                            vcar_vcyber_com.vcar_chexi;
    """
    # 插入车系表
    sql_insert_chexi = """
                        INSERT INTO `vcar_vcyber_com`.`vcar_chexi`
                    (`chexiID`,
                    `pinpaiID`,
                    `chexiType`,
                    `name`,
                    `url`,
                    `maxMoney`,
                    `minMoney`,
                    `onSale`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s);
    """

    # 更新论坛id
    sql_update_chexi = """
                        UPDATE vcar_chexi 
                    SET 
                        bbsId = %s,
                        maxMoney=%s,
                        minMoney=%s
                    WHERE
                        chexiId = %s
    """

    # 查询用户
    sql_query_user = """
                    SELECT 
                        sid,
                        createTime
                    FROM
                        vcar_vcyber_com.vcar_qczj_user 
    """

    # 分页查询用户
    sql_query_user_page = """
                        SELECT 
                           sid 
                        FROM
                            vcar_vcyber_com.vcar_qczj_user
                        where  createTime >= '%s'
                        ORDER BY createTime ASC
                        limit %s , %s
    """

    # 查询单个用户
    sql_query_user_one = """
                        SELECT 
                            sid,
                            createTime
                        FROM
                            vcar_vcyber_com.vcar_qczj_user
                        WHERE sid = %s;
        """

    # 查询用户总数
    sql_query_user_count = """
                            SELECT 
                                COUNT(1)
                            FROM
                                vcar_vcyber_com.vcar_qczj_user
                            where  createTime >= '%s'
                            ORDER BY createTime ASC
    """
    # 更新用户
    sql_update_user = """
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_user`
                        SET
                            `headImg` = %s,
                            `sex` = %s,
                            `province` =  %s,
                            `provinceCode` = %s,
                            `city` =  %s,
                            `cityCode` = %s,
                            `level` = %s,
                            `focusNum` =  %s,
                            `fansNum` = %s,
                            `vStatus` = %s,
                            `updateTime` = %s
                        WHERE `sid` = %s;
    """
    # 插入用户认证车辆
    sql_insert_user_car = """
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user_car`
                            (`sid`,
                            `userId`,
                            `specId`)
                            VALUES(
                            %s,
                            %s,
                            %s);

    """
    # 更新用户认证车辆
    sql_update_user_car = """
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_user_car`
                        SET
                            `status` = %s,
                            `updateTime` = %s
                        WHERE `userId` = %s
                        AND   `specId` = %s;
    """
    # 查询用户认证车辆
    sql_query_user_car_in = """
                        SELECT 
                            userId,
                            specId
                        FROM
                            `vcar_vcyber_com`.`vcar_qczj_user_car`
                        WHERE
                            userId in (%s)
                        ORDER BY userId;
    """

    # 根据省名称模糊查询省
    sql_query_province_like = """
                            SELECT 
                                provinceid, province
                            FROM
                                vcar_vcyber_com.vcar_dist_provinces
                            WHERE
                                province LIKE '%%%s%%';
    """
    # 根据市名称模糊查询市
    sql_query_city_like = """
                            SELECT 
                                cityid, city
                            FROM
                                vcar_vcyber_com.vcar_dist_cities
                            WHERE
                                city LIKE '%%%s%%';
    """
    # 根据县名称模糊查询县
    sql_query_county_like = """
                            SELECT 
                                areaid, area
                            FROM
                                vcar_vcyber_com.vcar_dist_areas
                            WHERE
                                area LIKE '%%%s%%';
    """
    # 查询所有的省
    sql_query_province_all = """
                            SELECT 
                                province, provinceid
                            FROM
                                vcar_vcyber_com.vcar_dist_provinces;
    """
    # 查询所有的市
    sql_query_city_all = """
                            SELECT 
                                city, cityid
                            FROM
                                vcar_vcyber_com.vcar_dist_cities;
    """

    # 查询所有的县
    sql_query_county_all = """
                            SELECT 
                                area, areaid
                            FROM
                                vcar_vcyber_com.vcar_dist_areas;
    """
    # 根据市查询省名称及省代码
    sql_query_province_by_cityid = """
                            SELECT 
                                t2.province, t2.provinceid, t1.city, t1.cityid
                            FROM
                                vcar_vcyber_com.vcar_dist_cities t1
                                    LEFT JOIN
                                vcar_dist_provinces t2 ON t1.provinceid = t2.provinceid
                            WHERE
                                t1.cityid = %s;
    """
    # 查询该市下面所有的区县
    sql_query_county_by_cityid = """
                            SELECT 
                                area,areaid
                            FROM
                                vcar_vcyber_com.vcar_dist_areas
                            WHERE
                                cityid = %s
    """
    # 根据省代码查询直辖市下下面的区县
    sql_query_county_by_proid = """
                            SELECT 
                                t3.province,t3.provinceid,
                                t2.city,t2.cityid,
                                t1.area, t1.areaid
                            FROM
                                vcar_vcyber_com.vcar_dist_areas t1
                                    LEFT JOIN
                                vcar_dist_cities t2 ON t1.cityid = t2.cityid
                                    LEFT JOIN
                                vcar_dist_provinces t3 ON t2.provinceid = t3.provinceid
                            WHERE
                                t3.provinceid = %s
    """
    # 根据区县代码反向查询市代码
    sql_query_city_by_countyid = """  
                            SELECT 
                                t3.province,t3.provinceid,
                                t2.city,t2.cityid,
                                t1.area, t1.areaid
                            FROM
                                vcar_vcyber_com.vcar_dist_areas t1
                                    LEFT JOIN
                                vcar_dist_cities t2 ON t1.cityid = t2.cityid
                                    LEFT JOIN
                                vcar_dist_provinces t3 ON t2.provinceid = t3.provinceid
                            WHERE
                                t1.areaid = %s;
    """
    # 根据省代码查询该省下所有的市
    sql_query_city_by_provinceid = """
                            SELECT 
                                city, cityid
                            FROM
                                vcar_dist_cities
                            WHERE
                                provinceid = %s
    """

    # 查询数据库中已经存在的id集合
    sql_query_dealer_in="""
                            SELECT 
                                sid
                            FROM
                                vcar_qczj_dealer
                            WHERE
                                sid IN (%s)
    """
    # 插入经销商
    sql_insert_dealer="""
                            INSERT INTO `vcar_vcyber_com`.`vcar_qczj_dealer`
                               (`sid`,
                                `dealerName`,
                                `homepageUrl`,
                                `headImgUrl`,
                                `provinceCode`,
                                `province`,
                                `city`,
                                `cityCode`,
                                `county`,
                                `countyCode`,
                                `mainBrand`,
                                `mainBrandId`,
                                `tel`,
                                `detailAddr`,
                                `onSaleNum`,
                                `type`,
                                `badge`,
                                `limitAreaType`,
                                `limitAreaDetail`)
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
                                %s);
    """
    # 更新经销商
    sql_update_dealer="""
                            UPDATE `vcar_vcyber_com`.`vcar_qczj_dealer`
                            SET
                                `dealerName` = %s,
                                `homepageUrl` = %s,
                                `headImgUrl` = %s,
                                `provinceCode` = %s,
                                `province` = %s,
                                `city` = %s,
                                `cityCode` = %s,
                                `county` = %s,
                                `countyCode` = %s,
                                `mainBrand` = %s,
                                `mainBrandId` = %s,
                                `tel` = %s,
                                `detailAddr` = %s,
                                `onSaleNum` = %s,
                                `type` = %s,
                                `badge` = %s,
                                `limitAreaType` = %s,
                                `limitAreaDetail` = %s,
                                `updateTime` = %s
                            WHERE `sid` = %s;
    """

    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306,
                               charset='utf8')
        return conn

    @classmethod
    def query(cls, sql):
        try:
            # 获取链接
            conn = cls.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            # for item in res:
            # print(item)
            # self.log(item)
            # 返回的是列表，列表元素类型是元组[(),(),,]
            return res
        except Exception as e:
            print(e)
            print(sql)
        finally:
            cursor.close()
            conn.close()

    # 批量更新或保存
    @classmethod
    def updateList(cls, sql, paramsList):
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
    def updateOne(cls, sql, params):
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
    def parseToSet(cls, res, index):
        idSet = set()
        for item in res:
            idSet.add(item[index])
        return idSet

    # 解析成字典
    @classmethod
    def parseToDict(cls, res, keyIndex, valueIndex):
        d = dict()
        for item in res:
            d.__setitem__(item[keyIndex], item[valueIndex])
        return d

    # 解析成list
    @classmethod
    def parseToList(cls, res, index):
        l = list()
        for item in res:
            l.append(item[index])
        return l


# params=('t', '1', '1','1', '1','1', '1','1', '1','1','1', '1','1', '1','1', '1','1', '1')
# l=list()
# l.append(params)
# MySqlUtils.updateList(MySqlUtils.sql_insert_dealer,l)