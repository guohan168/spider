-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: vcar_vcyber_com
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sys_city`
--

DROP TABLE IF EXISTS `sys_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_city` (
  `id` varchar(10) NOT NULL COMMENT 'id',
  `name` varchar(50) DEFAULT NULL COMMENT '城市名',
  `pid` varchar(10) DEFAULT NULL COMMENT '父id',
  `level` char(1) DEFAULT NULL COMMENT '级别',
  `merger_name` varchar(50) DEFAULT NULL COMMENT '省市县全称',
  `province_id` varchar(10) DEFAULT NULL COMMENT '省id',
  `province_initial` varchar(10) DEFAULT NULL COMMENT '省首字母',
  `city_initial` varchar(10) DEFAULT NULL COMMENT '市首字母',
  PRIMARY KEY (`id`),
  FULLTEXT KEY `name_FULLTEXT` (`name`),
  FULLTEXT KEY `pid_FULLTEXT` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='省市区三级表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_chexi`
--

DROP TABLE IF EXISTS `vcar_chexi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_chexi` (
  `chexiID` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `pinpaiID` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,品牌表ID',
  `chexiType` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '车系类型',
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '车系名称',
  `url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '车系URL',
  `minMoney` decimal(18,2) DEFAULT '0.00' COMMENT '指导价小',
  `maxMoney` decimal(18,2) DEFAULT '0.00' COMMENT '指导价大',
  `score` decimal(18,2) DEFAULT '0.00' COMMENT '用户评分',
  `jibie` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '级别：跑车SUV小型中型',
  `state` int(11) DEFAULT '1' COMMENT '状态(0 冻结,1 激活)',
  `onSale` char(1) DEFAULT NULL COMMENT '0 停售\n1 在售\n2 即将销售',
  `img` varchar(150) DEFAULT NULL COMMENT '车系代表图片地址',
  `info` varchar(500) DEFAULT NULL COMMENT '车系概要信息',
  `bbsId` varchar(45) DEFAULT NULL COMMENT '论坛id',
  `createdTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '行创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`chexiID`),
  KEY `Index_1` (`chexiID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_chexing`
--

DROP TABLE IF EXISTS `vcar_chexing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_chexing` (
  `chexingID` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `pinpaiID` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,品牌表ID',
  `chexiID` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,车系表ID',
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '车型名称',
  `url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '车型URL',
  `money` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '指导价',
  `score` decimal(18,2) NOT NULL DEFAULT '0.00' COMMENT '车型口碑得分',
  `gzd` int(11) NOT NULL DEFAULT '0' COMMENT '车系关注度',
  `avgFuel` decimal(8,2) DEFAULT NULL COMMENT '平均百公里油耗 ',
  `powerType` varchar(2) DEFAULT NULL COMMENT '能源类型\n1 汽油 \n2 柴油 \n3 纯电动\n4 油电混合 \n5 插电式混合动力  \n6 增程式',
  `numPeople` int(11) DEFAULT NULL COMMENT '参与评分人数',
  `imgUrlS` varchar(150) DEFAULT NULL COMMENT '车型小图',
  `imgUrlM` varchar(150) DEFAULT NULL COMMENT '车型中图',
  `state` int(11) DEFAULT '1' COMMENT '状态(0 冻结,1 激活)',
  `createdTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '行创建时间',
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`chexingID`),
  KEY `Index_1` (`chexingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_chexingshuxing`
--

DROP TABLE IF EXISTS `vcar_chexingshuxing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_chexingshuxing` (
  `chexingshuxingID` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `chexingID` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,车型表ID',
  `shuxingID` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,属性表ID',
  `shuxingName` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '属性名称',
  `shuxingValue` varchar(300) CHARACTER SET utf8 DEFAULT NULL COMMENT '属性值',
  `state` int(11) NOT NULL DEFAULT '1' COMMENT '状态(0 冻结,1 激活)',
  `createdTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行创建时间',
  PRIMARY KEY (`chexingshuxingID`),
  KEY `Index_1` (`chexingshuxingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车型-属性 中间表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_dic`
--

DROP TABLE IF EXISTS `vcar_dic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_dic` (
  `sid` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` varchar(45) DEFAULT '0' COMMENT '父类主键',
  `labelCd` varchar(45) DEFAULT NULL COMMENT '标签编号',
  `labelName` varchar(45) DEFAULT NULL COMMENT '标签名称',
  `optionName` varchar(45) DEFAULT NULL COMMENT '属性名',
  `optionValue` varchar(45) DEFAULT NULL COMMENT '属性值',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间	',
  `updateTime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_dist_areas`
--

DROP TABLE IF EXISTS `vcar_dist_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_dist_areas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `areaid` varchar(20) NOT NULL,
  `area` varchar(50) NOT NULL,
  `cityid` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3145 DEFAULT CHARSET=utf8 COMMENT='行政区域县区信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_dist_cities`
--

DROP TABLE IF EXISTS `vcar_dist_cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_dist_cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cityid` varchar(20) NOT NULL,
  `city` varchar(50) NOT NULL,
  `provinceid` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=346 DEFAULT CHARSET=utf8 COMMENT='行政区域地州市信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_dist_provinces`
--

DROP TABLE IF EXISTS `vcar_dist_provinces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_dist_provinces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provinceid` varchar(20) NOT NULL,
  `province` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8 COMMENT='省份信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_pinpai`
--

DROP TABLE IF EXISTS `vcar_pinpai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_pinpai` (
  `pinpaiID` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `szm` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '品牌首字母',
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '品牌名称',
  `imgUrl` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '品牌图片地址',
  `url` varchar(500) CHARACTER SET utf8 DEFAULT NULL COMMENT '品牌连接地址',
  `state` int(11) NOT NULL DEFAULT '1' COMMENT '状态(0 冻结,1 激活)',
  `createdTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行插入时间',
  PRIMARY KEY (`pinpaiID`),
  KEY `Index_1` (`pinpaiID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_bbs`
--

DROP TABLE IF EXISTS `vcar_qczj_bbs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_bbs` (
  `sid` varchar(70) NOT NULL,
  `bbsUrl` varchar(45) DEFAULT NULL,
  `bbsName` varchar(45) DEFAULT NULL,
  `bbsImgUrl` varchar(200) DEFAULT NULL,
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_bbs_chexi`
--

DROP TABLE IF EXISTS `vcar_qczj_bbs_chexi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_bbs_chexi` (
  `sid` varchar(45) NOT NULL COMMENT '主键',
  `bbsId` varchar(45) DEFAULT NULL COMMENT '论坛id',
  `chexiId` varchar(45) DEFAULT NULL COMMENT '车系id',
  `status` char(1) DEFAULT '1' COMMENT '1、有效\n0、无效',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_bbs_moder`
--

DROP TABLE IF EXISTS `vcar_qczj_bbs_moder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_bbs_moder` (
  `sid` varchar(45) NOT NULL,
  `bbsId` varchar(45) DEFAULT NULL,
  `userId` varchar(45) DEFAULT NULL,
  `tenureTime` datetime DEFAULT NULL,
  `status` char(1) DEFAULT '1' COMMENT '1、有效\n0、无效',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_bbs_note_head`
--

DROP TABLE IF EXISTS `vcar_qczj_bbs_note_head`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_bbs_note_head` (
  `sid` varchar(45) NOT NULL COMMENT '帖子主键',
  `bbsId` varchar(45) DEFAULT NULL COMMENT '论坛id',
  `userId` varchar(45) DEFAULT NULL COMMENT '用户id',
  `title` varchar(250) DEFAULT NULL COMMENT '论坛标题',
  `src` varchar(45) DEFAULT NULL COMMENT '来源',
  `publicTime` datetime DEFAULT NULL COMMENT '发布时间',
  `clickCount` int(11) DEFAULT NULL COMMENT '点击量',
  `replyCount` int(11) DEFAULT NULL COMMENT '回复量',
  `setTopStatus` char(1) DEFAULT '0' COMMENT '是否置顶\n0、否\n1、是',
  `noteType` char(1) DEFAULT NULL COMMENT '帖子类型\n1、新贴\n2、视频\n3、游记\n4、提问\n5、出售',
  `detaiUrl` varchar(100) DEFAULT NULL COMMENT '帖子url',
  `lastReplyTime` datetime DEFAULT NULL COMMENT '最后回复时间',
  `tuijianLevel` char(1) DEFAULT NULL COMMENT '推荐级别\n钻石 1\n精华 2\n推荐 3',
  `status` char(1) DEFAULT '1' COMMENT '状态',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_ciyun`
--

DROP TABLE IF EXISTS `vcar_qczj_ciyun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_ciyun` (
  `sid` varchar(45) NOT NULL COMMENT '主键',
  `chexingID` varchar(45) DEFAULT NULL COMMENT '车型id',
  `ciYunType` varchar(2) DEFAULT NULL COMMENT '评价分类\n1 外观\n2 内饰\n3 舒适性\n4 空间\n5 动力\n6 操控\n7 油耗\n8 性价比',
  `word` varchar(45) DEFAULT NULL COMMENT '评价词语',
  `peopleCount` int(11) DEFAULT NULL COMMENT '评价人数',
  `affectiveType` char(1) DEFAULT NULL COMMENT '语义情感\n0 负面\n1 正面',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_dealer`
--

DROP TABLE IF EXISTS `vcar_qczj_dealer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_dealer` (
  `sid` varchar(45) NOT NULL COMMENT '经销商id',
  `dealerName` varchar(45) DEFAULT NULL COMMENT '经销商全称',
  `homepageUrl` varchar(150) DEFAULT NULL COMMENT '经销商店铺主页',
  `headImgUrl` varchar(200) DEFAULT NULL COMMENT '经销商店铺图片',
  `provinceCode` varchar(45) DEFAULT NULL,
  `province` varchar(45) DEFAULT NULL COMMENT '经销商所在省',
  `city` varchar(45) DEFAULT NULL COMMENT '经销商所在市',
  `cityCode` varchar(45) DEFAULT NULL,
  `county` varchar(45) DEFAULT NULL COMMENT '经销商所在县',
  `countyCode` varchar(45) DEFAULT NULL,
  `mainBrand` varchar(45) DEFAULT NULL COMMENT '经销商主营品牌',
  `mainBrandId` varchar(45) DEFAULT NULL COMMENT '主营品牌id',
  `tel` varchar(45) DEFAULT NULL COMMENT '电话',
  `mobile` varchar(45) DEFAULT NULL COMMENT '手机',
  `detailAddr` varchar(200) DEFAULT NULL COMMENT '详细地址',
  `onSaleNum` varchar(45) DEFAULT NULL COMMENT '在售车型数量',
  `type` varchar(45) DEFAULT NULL COMMENT '经销商类型，如4s店',
  `badge` varchar(45) DEFAULT NULL COMMENT '徽章，常见金银铜',
  `limitAreaType` varchar(45) DEFAULT NULL COMMENT '销售区域类型 全国 本地 多地',
  `limitAreaDetail` varchar(1000) DEFAULT NULL COMMENT '具体销售地域范围',
  `status` char(1) DEFAULT '1' COMMENT '状态',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_keep_value`
--

DROP TABLE IF EXISTS `vcar_qczj_keep_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_keep_value` (
  `sid` varchar(50) NOT NULL COMMENT '主键\n格式：车系id＋_年份_时间',
  `chexiID` varchar(45) DEFAULT NULL COMMENT '车系id',
  `year` int(11) DEFAULT NULL COMMENT '年份',
  `keepValue` decimal(18,4) DEFAULT '0.0000' COMMENT '保值率',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_score_chexing`
--

DROP TABLE IF EXISTS `vcar_qczj_score_chexing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_score_chexing` (
  `sid` varchar(100) NOT NULL COMMENT '主键',
  `chexingID` varchar(45) DEFAULT NULL COMMENT '车型id',
  `scoreType` varchar(2) DEFAULT NULL COMMENT '评分类别\n1、空间\n2、动力\n3、操控\n4、油耗\n5、舒适性\n6、外观\n7、内饰\n8、性价比\n9、平均油耗\n',
  `score` varchar(45) DEFAULT NULL COMMENT '分数',
  `compareScore` varchar(45) DEFAULT NULL COMMENT '与同级别比较高于多少分或低于多少分，低于用负数表示',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user`
--

DROP TABLE IF EXISTS `vcar_qczj_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user` (
  `sid` varchar(100) NOT NULL COMMENT '用户主键',
  `userName` varchar(45) DEFAULT NULL COMMENT '用户昵称',
  `homepageUrl` varchar(150) DEFAULT NULL COMMENT '用户主页',
  `headImg` varchar(200) DEFAULT NULL COMMENT '头像url',
  `sex` char(1) DEFAULT NULL COMMENT '性别',
  `provinceCode` varchar(45) DEFAULT NULL COMMENT '省代码',
  `province` varchar(45) DEFAULT NULL COMMENT '省名称',
  `cityCode` varchar(45) DEFAULT NULL COMMENT '市代码',
  `city` varchar(45) DEFAULT NULL COMMENT '市名称',
  `countyCode` varchar(45) DEFAULT NULL COMMENT '县代码',
  `county` varchar(45) DEFAULT NULL COMMENT '县名称',
  `level` varchar(45) DEFAULT NULL COMMENT '用户等级',
  `registerTime` datetime DEFAULT NULL COMMENT '注册时间',
  `lastLogin` datetime DEFAULT NULL COMMENT '最后登录时间',
  `focusNum` int(11) DEFAULT NULL COMMENT '关注人数',
  `fansNum` int(11) DEFAULT NULL COMMENT '粉丝数',
  `kmValue` int(11) DEFAULT NULL COMMENT '里程值',
  `bestNoteNum` int(11) DEFAULT NULL COMMENT '精华帖数量',
  `mainNoteNum` int(11) DEFAULT NULL COMMENT '主帖数量',
  `prize` varchar(45) DEFAULT NULL COMMENT '勋章，多个之间用逗号隔开',
  `status` varchar(45) DEFAULT '1',
  `vStatus` char(1) DEFAULT '0' COMMENT '车主认证 \n0 未认证\n1 已认证',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_car`
--

DROP TABLE IF EXISTS `vcar_qczj_user_car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_car` (
  `sid` varchar(45) NOT NULL,
  `userId` varchar(45) DEFAULT NULL,
  `specId` varchar(45) DEFAULT NULL,
  `status` char(1) DEFAULT '1' COMMENT '1、有效\n2、无效',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_koubei_detail`
--

DROP TABLE IF EXISTS `vcar_qczj_user_koubei_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_koubei_detail` (
  `sid` varchar(100) NOT NULL COMMENT '主键',
  `koubeiSid` varchar(100) DEFAULT NULL COMMENT '口碑主表主键',
  `koubeiType` varchar(45) DEFAULT NULL COMMENT '口碑类别',
  `koubeiContent` varchar(45) DEFAULT NULL COMMENT '口碑内容',
  `publicTime` datetime DEFAULT NULL COMMENT '发表时间',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_koubei_head`
--

DROP TABLE IF EXISTS `vcar_qczj_user_koubei_head`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_koubei_head` (
  `sid` varchar(100) NOT NULL COMMENT '口碑表主键',
  `title` varchar(150) DEFAULT NULL COMMENT '口碑主题，即题目',
  `publicTime` datetime DEFAULT NULL COMMENT '发表时间',
  `userSid` varchar(45) DEFAULT NULL COMMENT '用户主键',
  `chexingID` varchar(45) DEFAULT NULL COMMENT '车型id',
  `buyTime` datetime DEFAULT NULL COMMENT '购买时间',
  `price` decimal(8,2) DEFAULT NULL COMMENT '价格',
  `dealerId` varchar(45) DEFAULT NULL COMMENT '经销商id',
  `province` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL COMMENT '购买地点：城市',
  `county` varchar(45) DEFAULT NULL COMMENT '购买地点：县／区',
  `currentKm` int(11) DEFAULT NULL COMMENT '当前行驶距离',
  `fuel` double DEFAULT NULL COMMENT '油耗',
  `koubeiLink` varchar(150) DEFAULT NULL COMMENT '口碑链接',
  `favorNum` int(11) DEFAULT NULL COMMENT '支持人数',
  `readNum` int(11) DEFAULT NULL COMMENT '阅读人数',
  `commentNum` int(11) DEFAULT NULL COMMENT '评论人数',
  `koubeiSrc` varchar(45) DEFAULT NULL COMMENT '口碑来源\n手机汽车之家\n汽车之家Android版',
  `lastUpdateTime` datetime DEFAULT NULL COMMENT '追后一次追加时间',
  `mjjh` varchar(45) DEFAULT NULL COMMENT '满级精华级别，空表示无，多个用逗号隔开\n1、三级精华\n2、二级精华\n4、推荐\n0、首页推荐',
  `status` char(1) DEFAULT '1',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '爬虫记录创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '爬虫记录修改时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_koubei_img`
--

DROP TABLE IF EXISTS `vcar_qczj_user_koubei_img`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_koubei_img` (
  `sid` varchar(100) NOT NULL COMMENT '主键',
  `koubeiSid` varchar(100) DEFAULT NULL,
  `koubeiType` varchar(45) DEFAULT NULL,
  `imgUrl` varchar(200) DEFAULT NULL,
  `instruction` varchar(70) DEFAULT NULL,
  `publicTime` datetime DEFAULT NULL,
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_koubei_purpose`
--

DROP TABLE IF EXISTS `vcar_qczj_user_koubei_purpose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_koubei_purpose` (
  `sid` varchar(100) NOT NULL COMMENT '主键',
  `koubeiSid` varchar(100) DEFAULT NULL COMMENT '用户id',
  `purpose` varchar(45) DEFAULT NULL COMMENT '购车用途',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_qczj_user_koubei_score`
--

DROP TABLE IF EXISTS `vcar_qczj_user_koubei_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_qczj_user_koubei_score` (
  `sid` varchar(100) NOT NULL COMMENT '主键',
  `koubeiSid` varchar(100) DEFAULT NULL,
  `scoreType` varchar(2) DEFAULT NULL COMMENT '评分类目',
  `score` int(11) DEFAULT NULL COMMENT '分值',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_shuxing`
--

DROP TABLE IF EXISTS `vcar_shuxing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_shuxing` (
  `shuxingID` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `shuxingTypeID` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '外键,属性类型表ID',
  `name` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '属性名称',
  `state` int(11) NOT NULL DEFAULT '1' COMMENT '状态(0 冻结, 1 激活)',
  `createdTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行创建时间',
  PRIMARY KEY (`shuxingID`),
  KEY `Index_1` (`shuxingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='属性表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_shuxingtype`
--

DROP TABLE IF EXISTS `vcar_shuxingtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_shuxingtype` (
  `shuxingTypeID` varchar(100) CHARACTER SET utf8 NOT NULL COMMENT '主键ID',
  `name` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '车型属性名称',
  `state` int(11) NOT NULL DEFAULT '1' COMMENT '状态(0 冻结,1 激活)',
  `createdTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行创建时间',
  PRIMARY KEY (`shuxingTypeID`),
  KEY `Index_1` (`shuxingTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='属性类别表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_souhu_chexi`
--

DROP TABLE IF EXISTS `vcar_souhu_chexi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_souhu_chexi` (
  `chexiID` varchar(45) NOT NULL COMMENT '车系id',
  `pinpaiID` varchar(45) DEFAULT NULL COMMENT '品牌id',
  `chexiType` varchar(45) DEFAULT NULL COMMENT '车系厂商类别',
  `chexiTypeID` varchar(45) DEFAULT NULL COMMENT '车系厂商类别id',
  `name` varchar(45) DEFAULT NULL COMMENT '车系名称',
  `url` varchar(200) DEFAULT NULL COMMENT '车系主页链接',
  `minMoney` decimal(8,2) DEFAULT NULL COMMENT '价格区间最小',
  `maxMoney` decimal(8,2) DEFAULT NULL COMMENT '价格区间最低',
  `score` decimal(8,2) DEFAULT NULL COMMENT '平均评分',
  `jibie` varchar(45) DEFAULT NULL COMMENT '级别',
  `guobie` varchar(45) DEFAULT NULL COMMENT '国别 ',
  `chechang` varchar(45) DEFAULT NULL COMMENT '车厂\n自主 合资 进口',
  `onSale` varchar(45) DEFAULT NULL COMMENT '是否在售',
  `imgS` varchar(200) DEFAULT NULL COMMENT '车系代表图片小图',
  `imgM` varchar(200) DEFAULT NULL COMMENT '车系代表图片大图',
  `status` char(1) DEFAULT '1' COMMENT '状态',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`chexiID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_souhu_chexi_sales`
--

DROP TABLE IF EXISTS `vcar_souhu_chexi_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_souhu_chexi_sales` (
  `sid` varchar(45) NOT NULL COMMENT '主键',
  `chexiId` varchar(45) DEFAULT NULL COMMENT '车系id',
  `salesNum` varchar(45) DEFAULT NULL COMMENT '销售数量',
  `countDate` datetime DEFAULT NULL COMMENT '统计日期',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_souhu_chexi_type`
--

DROP TABLE IF EXISTS `vcar_souhu_chexi_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_souhu_chexi_type` (
  `chexiTypeID` varchar(45) NOT NULL COMMENT '车系类别id',
  `chexiType` varchar(45) DEFAULT NULL COMMENT '车系名称',
  `pinpaiID` varchar(45) DEFAULT NULL COMMENT '品牌id',
  `chechang` varchar(45) DEFAULT NULL COMMENT '车厂分类 自主、合资、进口',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`chexiTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_souhu_chexing`
--

DROP TABLE IF EXISTS `vcar_souhu_chexing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_souhu_chexing` (
  `chexingID` varchar(45) NOT NULL COMMENT '车型id',
  `pinpaiID` varchar(45) DEFAULT NULL COMMENT '品牌id',
  `chexiID` varchar(45) DEFAULT NULL COMMENT '车系id',
  `name` varchar(45) DEFAULT NULL COMMENT '车型名称',
  `url` varchar(200) DEFAULT NULL COMMENT '车型主页url',
  `money` decimal(8,2) DEFAULT NULL COMMENT '价格',
  `score` decimal(8,2) DEFAULT NULL COMMENT '平均评分',
  `gzd` int(11) DEFAULT NULL COMMENT '关注度',
  `avgFuel` decimal(8,2) DEFAULT NULL COMMENT '平均油耗',
  `powerType` varchar(45) DEFAULT NULL COMMENT '能源类型',
  `numPeple` int(11) DEFAULT NULL COMMENT '参与评论人数',
  `imgUrlS` varchar(200) DEFAULT NULL COMMENT '车型小图URL',
  `imgUrlM` varchar(200) DEFAULT NULL COMMENT '车型大图URL',
  `status` char(1) DEFAULT '1',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`chexingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vcar_souhu_pinpai`
--

DROP TABLE IF EXISTS `vcar_souhu_pinpai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vcar_souhu_pinpai` (
  `pinpaiID` varchar(45) NOT NULL COMMENT '品牌id',
  `szm` char(1) DEFAULT NULL COMMENT '首字母',
  `name` varchar(45) DEFAULT NULL COMMENT '品牌名称',
  `imgUrl` varchar(200) DEFAULT NULL COMMENT '品牌log图片',
  `url` varchar(200) DEFAULT NULL COMMENT '品牌主页',
  `guobie` varchar(45) DEFAULT NULL COMMENT '国别',
  `status` char(1) DEFAULT '1' COMMENT '状态',
  `createTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`pinpaiID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-09 15:07:58
