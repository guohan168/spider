import json,re




s="""
<script type="text/javascript">var levelId = 7;
      var keyLink = {
        "message": "<span class='hs_kw24_baikeeJ'></span>",
        "result": {
          "total": 218,
          "items": [{
            "name": "车型<span class='hs_kw88_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_567.html",
            "id": 567
          },
          {
            "name": "厂<span class='hs_kw68_baikeeJ'></span><span class='hs_kw55_baikeeJ'></span><span class='hs_kw107_baikeeJ'></span><span class='hs_kw52_baikeeJ'></span>(<span class='hs_kw65_baikeeJ'></span>)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_219.html",
            "id": 219
          },
          {
            "name": "厂<span class='hs_kw68_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_218.html",
            "id": 218
          },
          {
            "name": "级别",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_220.html",
            "id": 220
          },
          {
            "name": "发动机",
            "link": "http://car.autohome.com.cn/shuyu/detail_8_9_555.html",
            "id": 555
          },
          {
            "name": "长*宽*高(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_222.html",
            "id": 222
          },
          {
            "name": "车身结构",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_4_281.html",
            "id": 281
          },
          {
            "name": "最高车速(km/h)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_267.html",
            "id": 267
          },
          {
            "name": "官方0-100km/h加速(s)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_225.html",
            "id": 225
          },
          {
            "name": "<span class='hs_kw79_baikeeJ'></span>0-100km/h加速(s)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_272.html",
            "id": 272
          },
          {
            "name": "<span class='hs_kw79_baikeeJ'></span>100-0km/h制动(m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_273.html",
            "id": 273
          },
          {
            "name": "<span class='hs_kw79_baikeeJ'></span><span class='hs_kw19_baikeeJ'></span>(L/100km)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_243.html",
            "id": 243
          },
          {
            "name": "工信部<span class='hs_kw25_baikeeJ'></span><span class='hs_kw19_baikeeJ'></span>(L/100km)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_271.html",
            "id": 271
          },
          {
            "name": "<span class='hs_kw79_baikeeJ'></span><span class='hs_kw3_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_306.html",
            "id": 306
          },
          {
            "name": "整车<span class='hs_kw91_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_19_274.html",
            "id": 274
          },
          {
            "name": "<span class='hs_kw59_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_275.html",
            "id": 275
          },
          {
            "name": "<span class='hs_kw23_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_276.html",
            "id": 276
          },
          {
            "name": "<span class='hs_kw45_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_277.html",
            "id": 277
          },
          {
            "name": "<span class='hs_kw53_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_4_132.html",
            "id": 132
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>轮距(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_278.html",
            "id": 278
          },
          {
            "name": "<span class='hs_kw105_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_638.html",
            "id": 638
          },
          {
            "name": "最小<span class='hs_kw3_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_279.html",
            "id": 279
          },
          {
            "name": "<span class='hs_kw6_baikeeJ'></span><span class='hs_kw95_baikeeJ'></span>(kg)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_280.html",
            "id": 280
          },
          {
            "name": "<span class='hs_kw11_baikeeJ'></span>(个)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_282.html",
            "id": 282
          },
          {
            "name": "座位数(个)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_283.html",
            "id": 283
          },
          {
            "name": "<span class='hs_kw4_baikeeJ'></span><span class='hs_kw76_baikeeJ'></span>(L)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_284.html",
            "id": 284
          },
          {
            "name": "行李厢<span class='hs_kw76_baikeeJ'></span>(L)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_20_285.html",
            "id": 285
          },
          {
            "name": "发动机型<span class='hs_kw106_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_570.html",
            "id": 570
          },
          {
            "name": "<span class='hs_kw18_baikeeJ'></span>(mL)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_287.html",
            "id": 287
          },
          {
            "name": "<span class='hs_kw87_baikeeJ'></span>形式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_640.html",
            "id": 640
          },
          {
            "name": "<span class='hs_kw92_baikeeJ'></span><span class='hs_kw39_baikeeJ'></span>形式",
            "link": "http://car.autohome.com.cn/shuyu/detail_8_9_289.html",
            "id": 289
          },
          {
            "name": "<span class='hs_kw92_baikeeJ'></span>数(个)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_290.html",
            "id": 290
          },
          {
            "name": "每缸<span class='hs_kw10_baikeeJ'></span>(个)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_291.html",
            "id": 291
          },
          {
            "name": "<span class='hs_kw101_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_182.html",
            "id": 182
          },
          {
            "name": "<span class='hs_kw21_baikeeJ'></span><span class='hs_kw86_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_641.html",
            "id": 641
          },
          {
            "name": "<span class='hs_kw66_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_181.html",
            "id": 181
          },
          {
            "name": "<span class='hs_kw62_baikeeJ'></span>(mm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_293.html",
            "id": 293
          },
          {
            "name": "<span class='hs_kw9_baikeeJ'></span>马力(Ps)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_294.html",
            "id": 294
          },
          {
            "name": "<span class='hs_kw9_baikeeJ'></span><span class='hs_kw37_baikeeJ'></span>(kW)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_295.html",
            "id": 295
          },
          {
            "name": "<span class='hs_kw9_baikeeJ'></span><span class='hs_kw37_baikeeJ'></span><span class='hs_kw7_baikeeJ'></span>(rpm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_296.html",
            "id": 296
          },
          {
            "name": "<span class='hs_kw9_baikeeJ'></span><span class='hs_kw57_baikeeJ'></span>(N·m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_571.html",
            "id": 571
          },
          {
            "name": "<span class='hs_kw9_baikeeJ'></span><span class='hs_kw57_baikeeJ'></span><span class='hs_kw7_baikeeJ'></span>(rpm)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_642.html",
            "id": 642
          },
          {
            "name": "发动机特有技术",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_643.html",
            "id": 643
          },
          {
            "name": "燃料形式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_572.html",
            "id": 572
          },
          {
            "name": "<span class='hs_kw75_baikeeJ'></span>标<span class='hs_kw106_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_573.html",
            "id": 573
          },
          {
            "name": "<span class='hs_kw20_baikeeJ'></span>方式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_574.html",
            "id": 574
          },
          {
            "name": "<span class='hs_kw29_baikeeJ'></span>材料",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_575.html",
            "id": 575
          },
          {
            "name": "<span class='hs_kw58_baikeeJ'></span>材料",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_576.html",
            "id": 576
          },
          {
            "name": "<span class='hs_kw0_baikeeJ'></span><span class='hs_kw30_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_577.html",
            "id": 577
          },
          {
            "name": "简称",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_22_1072.html",
            "id": 1072
          },
          {
            "name": "挡位个数",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_22_559.html",
            "id": 559
          },
          {
            "name": "变速箱类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_22_221.html",
            "id": 221
          },
          {
            "name": "驱动方式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_23_395.html",
            "id": 395
          },
          {
            "name": "四驱形式",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_7_412.html",
            "id": 412
          },
          {
            "name": "<span class='hs_kw34_baikeeJ'></span><span class='hs_kw103_baikeeJ'></span>结构",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_7_415.html",
            "id": 415
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span><span class='hs_kw27_baikeeJ'></span>类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_23_578.html",
            "id": 578
          },
          {
            "name": "<span class='hs_kw17_baikeeJ'></span>类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_23_579.html",
            "id": 579
          },
          {
            "name": "<span class='hs_kw61_baikeeJ'></span>类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_23_510.html",
            "id": 510
          },
          {
            "name": "车体结构",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_4_223.html",
            "id": 223
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>制动器类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_511.html",
            "id": 511
          },
          {
            "name": "<span class='hs_kw100_baikeeJ'></span>类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_512.html",
            "id": 512
          },
          {
            "name": "<span class='hs_kw16_baikeeJ'></span>制动类型",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_513.html",
            "id": 513
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>轮胎<span class='hs_kw49_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_580.html",
            "id": 580
          },
          {
            "name": "<span class='hs_kw47_baikeeJ'></span><span class='hs_kw49_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_581.html",
            "id": 581
          },
          {
            "name": "<span class='hs_kw35_baikeeJ'></span><span class='hs_kw49_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_24_515.html",
            "id": 515
          },
          {
            "name": "主/副<span class='hs_kw93_baikeeJ'></span>座安全<span class='hs_kw63_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_1082.html",
            "id": 1082
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/<span class='hs_kw71_baikeeJ'></span>侧<span class='hs_kw63_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=421",
            "id": 421
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>排侧<span class='hs_kw63_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=421",
            "id": 421
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>侧<span class='hs_kw63_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=421",
            "id": 421
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/<span class='hs_kw71_baikeeJ'></span>头部<span class='hs_kw63_baikeeJ'></span>(气帘)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=422",
            "id": 422
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>排头部<span class='hs_kw63_baikeeJ'></span>(气帘)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=422",
            "id": 422
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>头部<span class='hs_kw63_baikeeJ'></span>(气帘)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_420.html?lang=422",
            "id": 422
          },
          {
            "name": "膝部<span class='hs_kw63_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_17_420.html?lang=423",
            "id": 423
          },
          {
            "name": "胎压监测装置",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_551.html",
            "id": 551
          },
          {
            "name": "零胎压继续行驶",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_17_424.html",
            "id": 424
          },
          {
            "name": "安全带未系提示",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_552.html",
            "id": 552
          },
          {
            "name": "ISOFIX<span class='hs_kw85_baikeeJ'></span><span class='hs_kw42_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_1084.html",
            "id": 1084
          },
          {
            "name": "发动机<span class='hs_kw36_baikeeJ'></span>防盗",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_481.html",
            "id": 481
          },
          {
            "name": "车内中控锁",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_558.html",
            "id": 558
          },
          {
            "name": "遥控钥匙",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_582.html",
            "id": 582
          },
          {
            "name": "<span class='hs_kw78_baikeeJ'></span>启动系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_431.html",
            "id": 431
          },
          {
            "name": "<span class='hs_kw78_baikeeJ'></span>进入系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_1066.html",
            "id": 1066
          },
          {
            "name": "ABS防抱死",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_110.html",
            "id": 110
          },
          {
            "name": "<span class='hs_kw8_baikeeJ'></span>(EBD/CBC等)",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_125.html",
            "id": 125
          },
          {
            "name": "刹车辅助(EBA/BAS/BA等)",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_437.html",
            "id": 437
          },
          {
            "name": "<span class='hs_kw80_baikeeJ'></span>(ASR/TCS/TRC等)",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_438.html",
            "id": 438
          },
          {
            "name": "车身<span class='hs_kw98_baikeeJ'></span>控制(ESC/ESP/DSC等)",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_109.html",
            "id": 109
          },
          {
            "name": "上坡辅助",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_425.html",
            "id": 425
          },
          {
            "name": "自动<span class='hs_kw16_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_46_363.html",
            "id": 363
          },
          {
            "name": "陡坡缓降",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_138.html",
            "id": 138
          },
          {
            "name": "可变<span class='hs_kw27_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_6_399.html",
            "id": 399
          },
          {
            "name": "<span class='hs_kw43_baikeeJ'></span><span class='hs_kw27_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_6_399.html?lang=167",
            "id": 167
          },
          {
            "name": "可变转向比",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_6_409.html",
            "id": 409
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>桥<span class='hs_kw31_baikeeJ'></span><span class='hs_kw103_baikeeJ'></span>/<span class='hs_kw12_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_46_975.html",
            "id": 975
          },
          {
            "name": "<span class='hs_kw34_baikeeJ'></span><span class='hs_kw103_baikeeJ'></span>锁止功能",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_46_976.html",
            "id": 976
          },
          {
            "name": "<span class='hs_kw5_baikeeJ'></span><span class='hs_kw31_baikeeJ'></span><span class='hs_kw103_baikeeJ'></span>/<span class='hs_kw12_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_46_977.html",
            "id": 977
          },
          {
            "name": "电动<span class='hs_kw26_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_583.html",
            "id": 583
          },
          {
            "name": "全景<span class='hs_kw26_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_583.html?lang=584",
            "id": 584
          },
          {
            "name": "运动外观套件",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_585.html",
            "id": 585
          },
          {
            "name": "<span class='hs_kw46_baikeeJ'></span><span class='hs_kw38_baikeeJ'></span>轮圈",
            "link": "http://car.autohome.com.cn/shuyu/detail_13_15_525.html",
            "id": 525
          },
          {
            "name": "电动吸合门",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_443.html",
            "id": 443
          },
          {
            "name": "侧滑门",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_1122.html",
            "id": 1122
          },
          {
            "name": "电动后备厢",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_452.html",
            "id": 452
          },
          {
            "name": "感应后备厢",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_1369.html",
            "id": 1369
          },
          {
            "name": "车顶行李架",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_47_1368.html",
            "id": 1368
          },
          {
            "name": "<span class='hs_kw77_baikeeJ'></span>方向盘",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_586.html",
            "id": 586
          },
          {
            "name": "方向盘<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1085.html",
            "id": 1085
          },
          {
            "name": "方向盘电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_589.html",
            "id": 589
          },
          {
            "name": "多功能方向盘",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_444.html",
            "id": 444
          },
          {
            "name": "方向盘换挡",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_468.html",
            "id": 468
          },
          {
            "name": "方向盘<span class='hs_kw13_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1064.html",
            "id": 1064
          },
          {
            "name": "方向盘记忆",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1370.html",
            "id": 1370
          },
          {
            "name": "定速巡航",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_445.html",
            "id": 445
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/后<span class='hs_kw16_baikeeJ'></span>雷达",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1086.html",
            "id": 1086
          },
          {
            "name": "倒车<span class='hs_kw90_baikeeJ'></span><span class='hs_kw84_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_448.html",
            "id": 448
          },
          {
            "name": "<span class='hs_kw28_baikeeJ'></span>显示屏",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_590.html",
            "id": 590
          },
          {
            "name": "<span class='hs_kw74_baikeeJ'></span><span class='hs_kw48_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1371.html",
            "id": 1371
          },
          {
            "name": "HUD抬头数字显示",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_471.html",
            "id": 471
          },
          {
            "name": "座椅<span class='hs_kw99_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_591.html",
            "id": 591
          },
          {
            "name": "运动<span class='hs_kw41_baikeeJ'></span>格座椅",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_592.html",
            "id": 592
          },
          {
            "name": "座椅高低<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_639.html",
            "id": 639
          },
          {
            "name": "腰部<span class='hs_kw72_baikeeJ'></span><span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_449.html",
            "id": 449
          },
          {
            "name": "肩部<span class='hs_kw72_baikeeJ'></span><span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_593.html",
            "id": 593
          },
          {
            "name": "主/副<span class='hs_kw93_baikeeJ'></span>座电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1087.html",
            "id": 1087
          },
          {
            "name": "第二排靠背角度<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_595.html",
            "id": 595
          },
          {
            "name": "第二排<span class='hs_kw82_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_596.html",
            "id": 596
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>座椅电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_597.html",
            "id": 597
          },
          {
            "name": "电动座椅记忆",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_598.html",
            "id": 598
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/<span class='hs_kw71_baikeeJ'></span>座椅<span class='hs_kw13_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1088.html",
            "id": 1088
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/<span class='hs_kw71_baikeeJ'></span>座椅通<span class='hs_kw41_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1089.html",
            "id": 1089
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/<span class='hs_kw71_baikeeJ'></span>座椅按摩",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1090.html",
            "id": 1090
          },
          {
            "name": "第三排座椅",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_603.html",
            "id": 603
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>座椅<span class='hs_kw32_baikeeJ'></span>方式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1091.html",
            "id": 1091
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/后<span class='hs_kw34_baikeeJ'></span>扶手",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1092.html",
            "id": 1092
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>杯架",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_606.html",
            "id": 606
          },
          {
            "name": "GPS<span class='hs_kw107_baikeeJ'></span>航系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_607.html",
            "id": 607
          },
          {
            "name": "定位互动服务",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_455.html",
            "id": 455
          },
          {
            "name": "中控台彩色大屏",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_608.html",
            "id": 608
          },
          {
            "name": "<span class='hs_kw56_baikeeJ'></span>/车载<span class='hs_kw69_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_609.html",
            "id": 609
          },
          {
            "name": "车载电视",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_610.html",
            "id": 610
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>液晶屏",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_611.html",
            "id": 611
          },
          {
            "name": "<span class='hs_kw67_baikeeJ'></span><span class='hs_kw51_baikeeJ'></span><span class='hs_kw42_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_469.html",
            "id": 469
          },
          {
            "name": "CD支持MP3/WMA",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_612.html",
            "id": 612
          },
          {
            "name": "多媒体系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html",
            "id": 1096
          },
          {
            "name": "<span class='hs_kw89_baikeeJ'></span>品牌",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1212.html",
            "id": 1212
          },
          {
            "name": "<span class='hs_kw89_baikeeJ'></span>数量",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_618.html",
            "id": 618
          },
          {
            "name": "<span class='hs_kw60_baikeeJ'></span>大灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_458.html",
            "id": 458
          },
          {
            "name": "日间行车灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_442.html",
            "id": 442
          },
          {
            "name": "自动头灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_441.html",
            "id": 441
          },
          {
            "name": "转向辅助灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_51_1161.html",
            "id": 1161
          },
          {
            "name": "转向头灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_465.html",
            "id": 465
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>雾灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_51_619.html",
            "id": 619
          },
          {
            "name": "大灯<span class='hs_kw45_baikeeJ'></span>可调",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_51_620.html",
            "id": 620
          },
          {
            "name": "大灯清洗装置",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_51_621.html",
            "id": 621
          },
          {
            "name": "车内氛围灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_453.html",
            "id": 453
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>/后电动车窗",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_622.html",
            "id": 622
          },
          {
            "name": "车窗防夹手功能",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_623.html",
            "id": 623
          },
          {
            "name": "防紫外线/隔热玻璃",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_624.html",
            "id": 624
          },
          {
            "name": "后视镜电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_625.html",
            "id": 625
          },
          {
            "name": "后视镜<span class='hs_kw13_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_626.html",
            "id": 626
          },
          {
            "name": "内/外后视镜自动防眩目",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_1095.html",
            "id": 1095
          },
          {
            "name": "后视镜电动折叠",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_628.html",
            "id": 628
          },
          {
            "name": "后视镜记忆",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_629.html",
            "id": 629
          },
          {
            "name": "后<span class='hs_kw41_baikeeJ'></span>挡遮阳帘",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_630.html",
            "id": 630
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>侧遮阳帘",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_631.html",
            "id": 631
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span>侧隐私玻璃",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_1063.html",
            "id": 1063
          },
          {
            "name": "遮阳板化妆镜",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_632.html",
            "id": 632
          },
          {
            "name": "后雨刷",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_633.html",
            "id": 633
          },
          {
            "name": "感应雨刷",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_454.html",
            "id": 454
          },
          {
            "name": "空调控制方式",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_1097.html",
            "id": 1097
          },
          {
            "name": "<span class='hs_kw71_baikeeJ'></span><span class='hs_kw73_baikeeJ'></span>空调",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_462.html?lang=459",
            "id": 459
          },
          {
            "name": "后座出<span class='hs_kw41_baikeeJ'></span>口",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_634.html",
            "id": 634
          },
          {
            "name": "温度分区控制",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_462.html?lang=463",
            "id": 463
          },
          {
            "name": "车内<span class='hs_kw43_baikeeJ'></span><span class='hs_kw40_baikeeJ'></span>/花粉过滤",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_635.html",
            "id": 635
          },
          {
            "name": "车载冰箱",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_636.html",
            "id": 636
          },
          {
            "name": "自动泊车入位",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_472.html",
            "id": 472
          },
          {
            "name": "发动机启停技术",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_54_334.html",
            "id": 334
          },
          {
            "name": "<span class='hs_kw54_baikeeJ'></span>辅助",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_17_426.html",
            "id": 426
          },
          {
            "name": "车道偏离<span class='hs_kw83_baikeeJ'></span>系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_54_788.html",
            "id": 788
          },
          {
            "name": "<span class='hs_kw96_baikeeJ'></span>刹车/<span class='hs_kw96_baikeeJ'></span>安全系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_16_44_436.html",
            "id": 436
          },
          {
            "name": "<span class='hs_kw15_baikeeJ'></span><span class='hs_kw96_baikeeJ'></span>转向系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_3_6_404.html",
            "id": 404
          },
          {
            "name": "夜视系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_637.html",
            "id": 637
          },
          {
            "name": "中控液晶屏分屏显示",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_464.html",
            "id": 464
          },
          {
            "name": "自<span class='hs_kw1_baikeeJ'></span>应巡航",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_54_446.html",
            "id": 446
          },
          {
            "name": "全景<span class='hs_kw2_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_11_12_473.html",
            "id": 473
          },
          {
            "name": "电动机",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html",
            "id": 1331
          },
          {
            "name": "电动机总<span class='hs_kw37_baikeeJ'></span>(kW)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1325",
            "id": 1325
          },
          {
            "name": "电动机总<span class='hs_kw57_baikeeJ'></span>(N·m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1326",
            "id": 1326
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw37_baikeeJ'></span>(kW)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1327",
            "id": 1327
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw57_baikeeJ'></span>(N·m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1328",
            "id": 1328
          },
          {
            "name": "后电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw37_baikeeJ'></span>(kW)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1329",
            "id": 1329
          },
          {
            "name": "后电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw57_baikeeJ'></span>(N·m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1331.html?lang=1330",
            "id": 1330
          },
          {
            "name": "工信部续航里程(km)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_1013.html",
            "id": 1013
          },
          {
            "name": "<span class='hs_kw97_baikeeJ'></span><span class='hs_kw64_baikeeJ'></span>(kWh)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_1124.html",
            "id": 1124
          },
          {
            "name": "<span class='hs_kw97_baikeeJ'></span>组<span class='hs_kw91_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_106_1367.html",
            "id": 1367
          },
          {
            "name": "电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw37_baikeeJ'></span>(kW)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_1011.html",
            "id": 1011
          },
          {
            "name": "电动机<span class='hs_kw9_baikeeJ'></span><span class='hs_kw57_baikeeJ'></span>(N·m)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_21_1012.html",
            "id": 1012
          },
          {
            "name": "LED大灯",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_51_659.html",
            "id": 659
          },
          {
            "name": "LATCH座椅<span class='hs_kw42_baikeeJ'></span>(兼容ISOFIX)",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_1084.html",
            "id": 1084
          },
          {
            "name": "<span class='hs_kw85_baikeeJ'></span><span class='hs_kw42_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_45_1084.html",
            "id": 1084
          },
          {
            "name": "<span class='hs_kw14_baikeeJ'></span>雷达",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1086.html",
            "id": 1086
          },
          {
            "name": "后倒车雷达",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_48_1086.html",
            "id": 1086
          },
          {
            "name": "<span class='hs_kw93_baikeeJ'></span>位电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1087.html",
            "id": 1087
          },
          {
            "name": "副<span class='hs_kw93_baikeeJ'></span>位电动<span class='hs_kw40_baikeeJ'></span>",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_49_1087.html",
            "id": 1087
          },
          {
            "name": "2-3<span class='hs_kw70_baikeeJ'></span><span class='hs_kw89_baikeeJ'></span>系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_618.html",
            "id": 618
          },
          {
            "name": "4-5<span class='hs_kw70_baikeeJ'></span><span class='hs_kw89_baikeeJ'></span>系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_618.html",
            "id": 618
          },
          {
            "name": "6-7<span class='hs_kw70_baikeeJ'></span><span class='hs_kw89_baikeeJ'></span>系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_618.html",
            "id": 618
          },
          {
            "name": "≥8<span class='hs_kw70_baikeeJ'></span><span class='hs_kw89_baikeeJ'></span>系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_618.html",
            "id": 618
          },
          {
            "name": "内后视镜自动防眩目",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_1095.html",
            "id": 1095
          },
          {
            "name": "外后视镜自动防眩目",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_52_1095.html",
            "id": 1095
          },
          {
            "name": "<span class='hs_kw102_baikeeJ'></span>CD",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=613",
            "id": 613
          },
          {
            "name": "虚拟多碟CD",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=614",
            "id": 614
          },
          {
            "name": "多碟CD系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=615",
            "id": 615
          },
          {
            "name": "CD系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=613",
            "id": 613
          },
          {
            "name": "<span class='hs_kw102_baikeeJ'></span>DVD",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=616",
            "id": 616
          },
          {
            "name": "多碟DVD系统",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_55_1096.html?lang=617",
            "id": 617
          },
          {
            "name": "手动空调",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_1097.html?lang=460",
            "id": 460
          },
          {
            "name": "自动空调",
            "link": "http://car.autohome.com.cn/shuyu/detail_18_53_1097.html?lang=461",
            "id": 461
          }]
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var config = {
        "message": "<span class='hs_kw38_configLN'></span>",
        "result": {
          "paramtypeitems": [{
            "name": "基本参数",
            "paramitems": [{
              "id": 567,
              "name": "车型<span class='hs_kw43_configLN'></span>",
              "pnid": "6_18",
              "valueitems": [{
                "specid": 32890,
                "value": "V8 Vantage 2018款 4.0T V8"
              }]
            },
            {
              "id": 219,
              "name": "厂<span class='hs_kw22_configLN'></span><span class='hs_kw2_configLN'></span><span class='hs_kw73_configLN'></span><span class='hs_kw70_configLN'></span>(<span class='hs_kw20_configLN'></span>)",
              "pnid": "6_160",
              "valueitems": [{
                "specid": 32890,
                "value": "186.80<span class='hs_kw3_configLN'></span>"
              }]
            },
            {
              "id": 218,
              "name": "厂<span class='hs_kw22_configLN'></span>",
              "pnid": "6_109",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw30_configLN'></span>·<span class='hs_kw1_configLN'></span>"
              }]
            },
            {
              "id": 220,
              "name": "级别",
              "pnid": "6_107",
              "valueitems": [{
                "specid": 32890,
                "value": "跑车"
              }]
            },
            {
              "id": 0,
              "name": "能源类型",
              "pnid": "6_-1",
              "valueitems": [{
                "specid": 32890,
                "value": "汽油"
              }]
            },
            {
              "id": 0,
              "name": "上市<span class='hs_kw52_configLN'></span>",
              "pnid": "6_33",
              "valueitems": [{
                "specid": 32890,
                "value": "2017.11"
              }]
            },
            {
              "id": 0,
              "name": "工信部纯电续驶里程(km)",
              "pnid": "6_-1",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 295,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw55_configLN'></span>(kW)",
              "pnid": "6_204",
              "valueitems": [{
                "specid": 32890,
                "value": "375"
              }]
            },
            {
              "id": 571,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw4_configLN'></span>(N·m)",
              "pnid": "6_123",
              "valueitems": [{
                "specid": 32890,
                "value": "685"
              }]
            },
            {
              "id": 555,
              "name": "发动机",
              "pnid": "6_127",
              "valueitems": [{
                "specid": 32890,
                "value": "4.0T 510马力 V8"
              }]
            },
            {
              "id": 0,
              "name": "变速箱",
              "pnid": "6_155",
              "valueitems": [{
                "specid": 32890,
                "value": "8挡手自一体"
              }]
            },
            {
              "id": 222,
              "name": "长*宽*高(mm)",
              "pnid": "6_199",
              "valueitems": [{
                "specid": 32890,
                "value": "4465*1942*1273"
              }]
            },
            {
              "id": 281,
              "name": "车身结构",
              "pnid": "6_195",
              "valueitems": [{
                "specid": 32890,
                "value": "2门2座硬顶跑车"
              }]
            },
            {
              "id": 267,
              "name": "最高车速(km/h)",
              "pnid": "6_168",
              "valueitems": [{
                "specid": 32890,
                "value": "314"
              }]
            },
            {
              "id": 225,
              "name": "官方0-100km/h加速(s)",
              "pnid": "6_165",
              "valueitems": [{
                "specid": 32890,
                "value": "3.6"
              }]
            },
            {
              "id": 272,
              "name": "<span class='hs_kw28_configLN'></span>0-100km/h加速(s)",
              "pnid": "6_116",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 273,
              "name": "<span class='hs_kw28_configLN'></span>100-0km/h制动(m)",
              "pnid": "6_50",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 271,
              "name": "工信部<span class='hs_kw39_configLN'></span><span class='hs_kw33_configLN'></span>(L/100km)",
              "pnid": "6_43",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 243,
              "name": "<span class='hs_kw28_configLN'></span><span class='hs_kw33_configLN'></span>(L/100km)",
              "pnid": "6_75",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 274,
              "name": "整车<span class='hs_kw48_configLN'></span>",
              "pnid": "6_187",
              "valueitems": [{
                "specid": 32890,
                "value": "三<span class='hs_kw58_configLN'></span>"
              }]
            }]
          },
          {
            "name": "车身",
            "paramitems": [{
              "id": 275,
              "name": "<span class='hs_kw6_configLN'></span>(mm)",
              "pnid": "6_169",
              "valueitems": [{
                "specid": 32890,
                "value": "4465"
              }]
            },
            {
              "id": 276,
              "name": "<span class='hs_kw37_configLN'></span>(mm)",
              "pnid": "6_11",
              "valueitems": [{
                "specid": 32890,
                "value": "1942"
              }]
            },
            {
              "id": 277,
              "name": "<span class='hs_kw62_configLN'></span>(mm)",
              "pnid": "6_39",
              "valueitems": [{
                "specid": 32890,
                "value": "1273"
              }]
            },
            {
              "id": 132,
              "name": "<span class='hs_kw72_configLN'></span>(mm)",
              "pnid": "6_76",
              "valueitems": [{
                "specid": 32890,
                "value": "2704"
              }]
            },
            {
              "id": 278,
              "name": "<span class='hs_kw36_configLN'></span>(mm)",
              "pnid": "6_140",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 638,
              "name": "<span class='hs_kw69_configLN'></span>(mm)",
              "pnid": "6_191",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 279,
              "name": "最小<span class='hs_kw7_configLN'></span>(mm)",
              "pnid": "6_216",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 281,
              "name": "车身结构",
              "pnid": "6_195",
              "valueitems": [{
                "specid": 32890,
                "value": "硬顶跑车"
              }]
            },
            {
              "id": 282,
              "name": "<span class='hs_kw19_configLN'></span>(个)",
              "pnid": "6_185",
              "valueitems": [{
                "specid": 32890,
                "value": "2"
              }]
            },
            {
              "id": 283,
              "name": "座位数(个)",
              "pnid": "6_68",
              "valueitems": [{
                "specid": 32890,
                "value": "2"
              }]
            },
            {
              "id": 284,
              "name": "<span class='hs_kw8_configLN'></span><span class='hs_kw26_configLN'></span>(L)",
              "pnid": "6_112",
              "valueitems": [{
                "specid": 32890,
                "value": "73"
              }]
            },
            {
              "id": 285,
              "name": "行李厢<span class='hs_kw26_configLN'></span>(L)",
              "pnid": "6_111",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 280,
              "name": "<span class='hs_kw10_configLN'></span><span class='hs_kw54_configLN'></span>(kg)",
              "pnid": "6_41",
              "valueitems": [{
                "specid": 32890,
                "value": "1530"
              }]
            }]
          },
          {
            "name": "发动机",
            "paramitems": [{
              "id": 570,
              "name": "发动机型<span class='hs_kw71_configLN'></span>",
              "pnid": "6_8",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 287,
              "name": "<span class='hs_kw31_configLN'></span>(mL)",
              "pnid": "6_102",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 0,
              "name": "<span class='hs_kw31_configLN'></span>(L)",
              "pnid": "6_163",
              "valueitems": [{
                "specid": 32890,
                "value": "4.0"
              }]
            },
            {
              "id": 640,
              "name": "<span class='hs_kw42_configLN'></span>形式",
              "pnid": "6_129",
              "valueitems": [{
                "specid": 32890,
                "value": "双<span class='hs_kw65_configLN'></span><span class='hs_kw49_configLN'></span>"
              }]
            },
            {
              "id": 289,
              "name": "<span class='hs_kw50_configLN'></span><span class='hs_kw57_configLN'></span>形式",
              "pnid": "6_198",
              "valueitems": [{
                "specid": 32890,
                "value": "V"
              }]
            },
            {
              "id": 290,
              "name": "<span class='hs_kw50_configLN'></span>数(个)",
              "pnid": "6_143",
              "valueitems": [{
                "specid": 32890,
                "value": "8"
              }]
            },
            {
              "id": 291,
              "name": "每缸<span class='hs_kw17_configLN'></span>(个)",
              "pnid": "6_220",
              "valueitems": [{
                "specid": 32890,
                "value": "4"
              }]
            },
            {
              "id": 182,
              "name": "<span class='hs_kw64_configLN'></span>",
              "pnid": "6_110",
              "valueitems": [{
                "specid": 32890,
                "value": "10.5"
              }]
            },
            {
              "id": 641,
              "name": "<span class='hs_kw35_configLN'></span><span class='hs_kw40_configLN'></span>",
              "pnid": "6_211",
              "valueitems": [{
                "specid": 32890,
                "value": "DOHC"
              }]
            },
            {
              "id": 181,
              "name": "<span class='hs_kw21_configLN'></span>(mm)",
              "pnid": "6_17",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 293,
              "name": "<span class='hs_kw16_configLN'></span>(mm)",
              "pnid": "6_65",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 294,
              "name": "<span class='hs_kw15_configLN'></span>马力(Ps)",
              "pnid": "6_67",
              "valueitems": [{
                "specid": 32890,
                "value": "510"
              }]
            },
            {
              "id": 295,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw55_configLN'></span>(kW)",
              "pnid": "6_204",
              "valueitems": [{
                "specid": 32890,
                "value": "375"
              }]
            },
            {
              "id": 296,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw55_configLN'></span><span class='hs_kw11_configLN'></span>(rpm)",
              "pnid": "6_98",
              "valueitems": [{
                "specid": 32890,
                "value": "6000"
              }]
            },
            {
              "id": 571,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw4_configLN'></span>(N·m)",
              "pnid": "6_123",
              "valueitems": [{
                "specid": 32890,
                "value": "685"
              }]
            },
            {
              "id": 642,
              "name": "<span class='hs_kw15_configLN'></span><span class='hs_kw4_configLN'></span><span class='hs_kw11_configLN'></span>(rpm)",
              "pnid": "6_35",
              "valueitems": [{
                "specid": 32890,
                "value": "2000-5000"
              }]
            },
            {
              "id": 643,
              "name": "发动机特有技术",
              "pnid": "6_80",
              "valueitems": [{
                "specid": 32890,
                "value": "-"
              }]
            },
            {
              "id": 572,
              "name": "燃料形式",
              "pnid": "6_121",
              "valueitems": [{
                "specid": 32890,
                "value": "汽油"
              }]
            },
            {
              "id": 573,
              "name": "<span class='hs_kw24_configLN'></span>标<span class='hs_kw71_configLN'></span>",
              "pnid": "6_90",
              "valueitems": [{
                "specid": 32890,
                "value": "95<span class='hs_kw71_configLN'></span>"
              }]
            },
            {
              "id": 574,
              "name": "<span class='hs_kw34_configLN'></span>方式",
              "pnid": "6_38",
              "valueitems": [{
                "specid": 32890,
                "value": "未知"
              }]
            },
            {
              "id": 575,
              "name": "<span class='hs_kw44_configLN'></span>材料",
              "pnid": "6_101",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw63_configLN'></span><span class='hs_kw56_configLN'></span>"
              }]
            },
            {
              "id": 576,
              "name": "<span class='hs_kw5_configLN'></span>材料",
              "pnid": "6_32",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw63_configLN'></span><span class='hs_kw56_configLN'></span>"
              }]
            },
            {
              "id": 577,
              "name": "<span class='hs_kw0_configLN'></span><span class='hs_kw45_configLN'></span>",
              "pnid": "6_77",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw13_configLN'></span>V"
              }]
            }]
          },
          {
            "name": "变速箱",
            "paramitems": [{
              "id": 559,
              "name": "挡位个数",
              "pnid": "6_15",
              "valueitems": [{
                "specid": 32890,
                "value": "8"
              }]
            },
            {
              "id": 221,
              "name": "变速箱类型",
              "pnid": "6_201",
              "valueitems": [{
                "specid": 32890,
                "value": "手自一体变速箱(AT)"
              }]
            },
            {
              "id": 1072,
              "name": "简称",
              "pnid": "6_118",
              "valueitems": [{
                "specid": 32890,
                "value": "8挡手自一体"
              }]
            }]
          },
          {
            "name": "底盘转向",
            "paramitems": [{
              "id": 395,
              "name": "驱动方式",
              "pnid": "6_114",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw59_configLN'></span><span class='hs_kw14_configLN'></span>"
              }]
            },
            {
              "id": 578,
              "name": "前<span class='hs_kw41_configLN'></span>类型",
              "pnid": "6_31",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw12_configLN'></span>双叉臂<span class='hs_kw23_configLN'></span><span class='hs_kw41_configLN'></span>"
              }]
            },
            {
              "id": 579,
              "name": "<span class='hs_kw27_configLN'></span>类型",
              "pnid": "6_30",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw47_configLN'></span><span class='hs_kw12_configLN'></span><span class='hs_kw23_configLN'></span>式"
              }]
            },
            {
              "id": 510,
              "name": "<span class='hs_kw9_configLN'></span>类型",
              "pnid": "6_200",
              "valueitems": [{
                "specid": 32890,
                "value": "电动<span class='hs_kw9_configLN'></span>"
              }]
            },
            {
              "id": 223,
              "name": "车体结构",
              "pnid": "6_138",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw32_configLN'></span>"
              }]
            }]
          },
          {
            "name": "车轮制动",
            "paramitems": [{
              "id": 511,
              "name": "<span class='hs_kw46_configLN'></span>类型",
              "pnid": "6_26",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw67_configLN'></span><span class='hs_kw18_configLN'></span>"
              }]
            },
            {
              "id": 512,
              "name": "<span class='hs_kw61_configLN'></span>类型",
              "pnid": "6_141",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw67_configLN'></span><span class='hs_kw18_configLN'></span>"
              }]
            },
            {
              "id": 513,
              "name": "<span class='hs_kw25_configLN'></span>制动类型",
              "pnid": "6_106",
              "valueitems": [{
                "specid": 32890,
                "value": "<span class='hs_kw53_configLN'></span><span class='hs_kw25_configLN'></span>"
              }]
            },
            {
              "id": 580,
              "name": "<span class='hs_kw29_configLN'></span><span class='hs_kw68_configLN'></span>",
              "pnid": "6_203",
              "valueitems": [{
                "specid": 32890,
                "value": "255/40 R20"
              }]
            },
            {
              "id": 581,
              "name": "<span class='hs_kw66_configLN'></span><span class='hs_kw68_configLN'></span>",
              "pnid": "6_84",
              "valueitems": [{
                "specid": 32890,
                "value": "295/35 R20"
              }]
            },
            {
              "id": 515,
              "name": "<span class='hs_kw51_configLN'></span><span class='hs_kw68_configLN'></span>",
              "pnid": "6_95",
              "valueitems": [{
                "specid": 32890,
                "value": "无"
              }]
            }]
          }],
          "speclist": [{
            "showstate": -1,
            "specid": 32890,
            "specstate": 20
          }],
          "yearid": 0
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var option = {
        "message": "<span class='hs_kw0_optionlb'></span>",
        "result": {
          "configtypeitems": [],
          "specid": 32890,
          "speclist": [{
            "specid": 32890,
            "showstate": -1,
            "specstate": 20
          }]
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var color = {
        "message": "成功",
        "result": {
          "specitems": [],
          "total": 0
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var innerColor = {
        "message": "成功",
        "result": {
          "specitems": [],
          "total": 0
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var bag = {
        "message": "成功",
        "result": {
          "specid": 32890,
          "speclist": [{
            "specid": 32890,
            "showstate": -1,
            "specstate": 20
          }],
          "bagtypeitems": []
        },
        "returncode": "0",
        "taskid": "d663523b-f180-4270-8cc8-b12b49a0f2d5",
        "time": "2018-08-30 14:46:15"
      };
      var dealerPrices = null;
      var allowancePrices = null;
      var allowanceIsShow = false;
      var saleSpecs = null;
      var wasLaodSaleSpecs = false;
      var seriesid = 385;
      var specid = 32890;
      var specIDs = [32890];
      var pageName = 'SpecParameter';
      var IsPuCar = false ? 1 : 0;
      var bookSpecitems = [];</script>
"""
startIndex=s.find("var keyLink = {")+14
tempJs=s[startIndex:]
labelJsonStr=tempJs[0:tempJs.find(";")]
labelJson=json.loads(labelJsonStr)
print(type(labelJson))
print(labelJson["result"]["items"][0]["name"])
for item in labelJson["result"]["items"]:
    keys=re.findall(r'\'.{10,20}\'',item['name'])
    id=item['id']
    name=item['name']
    for index,item in enumerate(keys):
        name=re.sub(r'<span class=.{8,20}></span>', keys[index], name)
    print(name)
    # print(re.findall(r'\'.{10,20}\'',item['name']))
    #print(item["id"],item["name"])


#
# 1、解析页面伪元素的值存入到map中
# 2、提取页面js中keyLink对象
# 3、解析keyLink对象，将name中伪元素用class去map中查找替换成实际的值
# 4、将属性id和属性名存入到数据库

# 1、提取config对象
# 2、解析config对象，将伪元素替换成实际值保存到数据库