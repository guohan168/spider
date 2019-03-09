from .mySqlUtils import MySqlUtils
# 地址解析工具类
class AddressUtils(object):
    # 所有省字典，以省名称为key，以省代码为value
    provincesDict=None
    # 所有市字典，以市为key，以市代码为value
    citiesDict=None
    # 所有县字典，以县名称为key，以县代码为value
    countiesDict=None

    # 直辖市集合
    fourCitiesSet={'上海市','北京市','重庆市','天津市'}




    # 查询所有的省
    @classmethod
    def initProvinces(cls):
        if cls.provincesDict == None:
            provinceRes=MySqlUtils.query(MySqlUtils.sql_query_province_all)
            cls.provincesDict=MySqlUtils.parseToDict(provinceRes,0,1)


    # 查询所有的市
    @classmethod
    def initCities(cls):
        if cls.citiesDict == None:
            cityRes=MySqlUtils.query(MySqlUtils.sql_query_city_all)
            cls.citiesDict=MySqlUtils.parseToDict(cityRes,0,1)
            # 手动添加直辖市，以市名为key，以省代码为value
            cls.citiesDict.__setitem__('北京市','110000')
            cls.citiesDict.__setitem__('上海市','310000')
            cls.citiesDict.__setitem__('天津市','120000')
            cls.citiesDict.__setitem__('重庆市','500000')



    # 查询所有的县
    @classmethod
    def initCounties(cls):
        if cls.countiesDict == None:
            countyRes=MySqlUtils.query(MySqlUtils.sql_query_county_all)
            cls.countiesDict=MySqlUtils.parseToDict(countyRes,0,1)

    # 对于直辖市，则根据省代码查询当前直辖市有多少区县,返回以区县名为key，以(省名称，省代码，市名称，市代码，县名称，县代码)为value的字典
    @classmethod
    def queryCountyByProvince(cls,provinceCode):
        countyRes=MySqlUtils.query(MySqlUtils.sql_query_county_by_proid % provinceCode)
        countyDict=dict()
        for res in countyRes:
            countyDict.__setitem__(res[4],res[5])
        return countyDict

    # 当为直辖市时，根据区县查询市
    @classmethod
    def queryCityByCountyid(cls,countyid):
        # print(countyid)
        res=MySqlUtils.query(MySqlUtils.sql_query_city_by_countyid % countyid)
        # print(res)
        pro_name=res[0][0]
        pro_id=res[0][1]
        city_name=res[0][2]
        city_id=res[0][3]
        county_name=res[0][4]
        county_id=res[0][5]
        return city_name,city_id

    # 查询该省下面所有的市
    @classmethod
    def queryCityByProvinceCode(cls,provinceCode):
        provinceRes=MySqlUtils.query(MySqlUtils.sql_query_city_by_provinceid % provinceCode)
        cityDict=MySqlUtils.parseToDict(provinceRes,0,1)
        return cityDict








    # 给定一个字符串，解析出省名称和省代码
    @classmethod
    def parseProvince(cls,content):
        name=None
        code=None
        # 初始化省字典
        if cls.provincesDict == None:
            cls.initProvinces()
        # 到字符串中查询是否存在某省名称
        for provinceName in cls.provincesDict.keys():
            if provinceName in content or provinceName[:len(provinceName)-1] in content:
                name=provinceName
                code=cls.provincesDict.get(name)
                break
        return name,code


    # 给定一个字符串，解析出市及该市所在的省
    @classmethod
    def parseProvinceAndCity(cls,content,provinceCode):
        provinceName=None
        cityName=None
        cityCode=None
        cityDict=None
        # print(content)
        # 解析省，如果省没有解析成功再解析市，然后根据市反向推导省
        if provinceCode == None:
            provinceName,provinceCode=cls.parseProvince(content)
        else:
            # 查询该省下面的所有市
            # print("provinceCode %s" % provinceCode)
            cityDict=cls.queryCityByProvinceCode(provinceCode)
            #
            cityDict.__setitem__('北京市', '110000')
            cityDict.__setitem__('上海市', '310000')
            cityDict.__setitem__('天津市', '120000')
            cityDict.__setitem__('重庆市', '500000')
        if cityDict == None:
            cls.initCities()
            cityDict = cls.citiesDict
        if cityDict != None and cityDict.get("市") != None:
            cityDict.pop("市")
        if cityDict != None and cityDict.get("县") != None:
            cityDict.pop("县")
        if cityDict != None and cityDict.get("市辖区") != None:
            cityDict.pop("市辖区")
        # 解析市
        for name in cityDict.keys():
            # print(name,name[:len(name)-1] in content)
            # if name[:len(name)-1] in "枣庄":
            #     print(True)
            #     print(content)
            # if name[:len(name)-1] in content:
            #     print(name)
            #     print(len(name))
            #     print("zz")
            if name in content or (len(name) > 2 and name[:len(name)-1] in content):
                cityName=name
                cityCode=cityDict.get(name)
                # 根据cityCode查询provinceCode provinceName
                # 判断是否直辖市
                if name in cls.fourCitiesSet:
                    provinceName=name
                    provinceCode=cityCode
                    cityName=None
                    cityCode=None
                else:
                    provinceRes=MySqlUtils.query(MySqlUtils.sql_query_province_by_cityid % cityCode)
                    provinceName=provinceRes[0][0]
                    provinceCode=provinceRes[0][1]
                break
        # print(provinceName,provinceCode,cityName,cityCode)
        return provinceName,provinceCode,cityName,cityCode

    # 查询某市下面的区或县,type表示是直辖市还是非直辖市
    @classmethod
    def parseCounty(cls,provinceCode,cityCode,content,type):
        countyName=None
        countyCode=None
        countyDict=None
        if type == '1':
            # 直辖市，根据省代码查询县区
            countyDict=cls.queryCountyByProvince(provinceCode)
        else:
            # 根据cityCode查询该city下面的所有的区或县
            countyRes = MySqlUtils.query(MySqlUtils.sql_query_county_by_cityid % cityCode)
            countyDict=MySqlUtils.parseToDict(countyRes,0,1)
        for name in countyDict.keys():
            # 去掉name中的空格
            nameStr=name.replace(" ","")
            if nameStr in content or (len(nameStr) > 2 and name[:len(nameStr)-1] in content):
                countyName=name
                countyCode=countyDict.get(name)
                break
        return countyName,countyCode

    # 解析省市县
    @classmethod
    def parseProvinceCityCount(cls, title, content):
        pro_name = None
        pro_code = None
        city_name = None
        city_code = None
        county_name = None
        county_code = None
        pro_name, pro_code = cls.parseProvince(title)
        if pro_code == None:
            pro_name, pro_code, city_name, city_code = cls.parseProvinceAndCity(title, pro_code)
            if pro_code == None:
                pro_name, pro_code, city_name, city_code = cls.parseProvinceAndCity(content, pro_code)
        else:
            pro_name, pro_code, city_name, city_code = cls.parseProvinceAndCity(content, pro_code)
        # print("- - - - ")
        # print(pro_name, pro_code, city_name, city_code)

        # 分是否为直辖市来解析区县
        if pro_code and city_code:
            # 为省 查询区县
            county_name, county_code = cls.parseCounty(pro_code, city_code, content, '0')
            pass
        elif pro_code and city_code == None:
            # 为直辖市
            county_name, county_code = cls.parseCounty(pro_code, city_code, content, '1')
            # 再根据区县名称查询上一级名称和code
            if county_code:
                city_name, city_code = cls.queryCityByCountyid(county_code)

        print(pro_name, pro_code, city_name, city_code, county_name, county_code)
        return pro_name,pro_code,city_name,city_code,county_name,county_code







# title="十三年老店开发区捷通"
# content="秦皇岛市海港区秦皇西大街天成家境旁（森林公园西行5公"
# AddressUtils.parseProvinceCityCount(title,content)



# # 解析后的数据源
# pro_name = None
# pro_code = None
# city_name = None
# city_code = None
# county_name = None
# county_code = None

# 测试非直辖市
# title="十三年老店开发区捷通"
# content="秦皇岛市海港区秦皇西大街天成家境旁（森林公园西行5公"
# title="吉利汽车枣庄德源店"
# content="枣木高速转盘向南222米路西，迎宾汽车"
# title="上海冠松之星"
# content="上海市中环汶水路801号（原平路/真华路出口）"
# title="润华奔腾"
# content="济南市经十西路京福高速西口西行4公里路北（润华汽车"
# title="东风本田北京鑫伯龙"
# content="北京市丰台区西局西街298号（万丰路首航超市向北500米"
# title="东风本田博诚"
# content="北京市昌平区东三旗新北亚汽车交易市场院内3-9号"
# title="汕头宝悦MINI"
# content="广东省汕头市龙湖区泰山路116号 "
# title = "绵阳国顺 "
# content = "绵阳市经开区机场东路221号2栋1层"
# addr = content.split(" ")[0]
# # 通过标题解析省
# pro_name,pro_code=AddressUtils.parseProvince(title)
# if pro_name == None:
#     # 通过详细地址解析省
#     pro_name,pro_code=AddressUtils.parseProvince(addr)
#     if pro_name == None:
#         # 解析市，然后通过市方向解析省
#         pro_name,pro_code,city_name,city_code=AddressUtils.parseProvinceAndCity(addr)
#         # 如果省有值而市没有值，则证明是直辖市
#         if pro_name != None and city_name == None:
#             # 查询该直辖市下所有的区县
#             county_name,county_code=AddressUtils.parseCounty(provinceCode=pro_code,type='1',content=addr)
#             # 根据区县逆向查询市名称及代码
#             if county_code:
#                 city_name,city_code=AddressUtils.queryCityByCountyid(county_code)
# else:
#     # 查询该省下面所有的市
#     pass

#
#
# pro_name=None
# pro_code=None
# city_name=None
# city_code=None
# county_name=None
# county_code=None
# pro_name,pro_code=AddressUtils.parseProvince(title)
# if pro_code == None:
#     pro_name, pro_code, city_name, city_code = AddressUtils.parseProvinceAndCity(title, pro_code)
#     if pro_code == None:
#         pro_name,pro_code,city_name,city_code=AddressUtils.parseProvinceAndCity(content,pro_code)
# print("- - - - ")
# print(pro_name,pro_code,city_name,city_code)
#
#
# # 分是否为直辖市来解析区县
# if pro_code and city_code:
#     # 为省 查询区县
#     county_name,county_code=AddressUtils.parseCounty(pro_code,city_code,content,'0')
#     pass
# elif pro_code and city_code == None:
#     # 为直辖市
#     county_name,county_code=AddressUtils.parseCounty(pro_code, city_code, content,'1')
#     # 再根据区县名称查询上一级名称和code
#     if county_code:
#         city_name,city_code=AddressUtils.queryCityByCountyid(county_code)
#
#
# print(pro_name,pro_code,city_name,city_code,county_name,county_code)













