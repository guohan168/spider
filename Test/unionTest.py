import scrapy,pymysql,re
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# 1、利用selenium获取加载后的网页
from selenium.webdriver.support.wait import WebDriverWait

url="https://car.autohome.com.cn/config/spec/32253.html"
dr=webdriver.Chrome()
dr.get(url)
#time.sleep(3)
wait=WebDriverWait(dr,3)
wait.until(EC.presence_of_element_located((By.ID,'tab_0')))
page=dr.page_source


#2、将page转换为Scrapy的Selector，以便于通过selector语法选择操作元素
res=Selector(text=page)

# 3、获取所有的table的父元素
configDiv=res.css("#config_data")

# 4、获取configDiv下的所有table
tableList=configDiv.xpath("table")
print(len(tableList))

#取出一个伪元素测试
cloData=tableList[1].xpath(".//tr")[1].xpath(".//a")
className=cloData[0].xpath("span/@class").extract_first()
print(className)# 打印出厂字了，商字使用了伪元素
#根据span的class名通过selenium执行js获取其值
js="return window.getComputedStyle(document.getElementsByClassName('" + className + "')[0], 'before').getPropertyValue('content')"
word=dr.execute_script(js)
print(word)
# 获取到span的值后，将span的class样式删除，显示赋值
removeScripts="var arr = document.getElementsByClassName('"+className+"');arr[0].classList.remove('"+className+"');arr[0].innerHTML="+word+";arr[0].classList.remove('"+className+"');"
dr.execute_script(removeScripts)

# print(dr.find_element_by_xpath("/html/body/div[3]/div[3]/table[2]/tbody/tr[2]/th/div/a").text)

tableList = dr.find_elements(By.CSS_SELECTOR, ".tbcs")
classNameList = list()
for table in tableList:
    spanList = table.find_elements(By.TAG_NAME, "span")
    for span in spanList:
        className = span.get_attribute("class")
        if className and className != '':
            classNameList.append(className)
            # js = "return window.getComputedStyle(document.getElementsByClassName('" + className + "')[0], 'before').getPropertyValue('content')"
            # word = dr.execute_script(js)
            # print(word)
            # # 获取到span的值后，将span的class样式删除，显示赋值
            # removeScripts = "var arr = document.getElementsByClassName('" + className + "');arr[0].classList.remove('" + className + "');arr[0].innerHTML=" + word + ";arr[0].classList.remove('" + className + "');"
            # dr.execute_script(removeScripts)


js="return window.getComputedStyle(document.getElementsByClassName('" + classNameList[0] + "')[0], 'before').getPropertyValue('content')"
word=dr.execute_script(js)
print(word)
# 获取到span的值后，将span的class样式删除，显示赋值
removeScripts="var arr = document.getElementsByClassName('"+classNameList[0]+"');arr[0].classList.remove('"+classNameList[0]+"');arr[0].innerHTML="+word+";arr[0].classList.remove('"+classNameList[0]+"');"
dr.execute_script(removeScripts)


className='hs_kw41_configiU'
js="return window.getComputedStyle(document.getElementsByClassName('" + className + "')[0], 'before').getPropertyValue('content')"
word=dr.execute_script(js)
print(word)
# 获取到span的值后，将span的class样式删除，显示赋值
removeScripts="""
           var arr = document.getElementsByClassName('%s');
           alert(arr.length);
           for(i=0;i<arr.length;i++){
                alert(i);
                arr[i].innerHTML=%s;
           }
         """
removeScripts=removeScripts % (className,word)
dr.execute_script(removeScripts)


#removeScripts="var arr = document.getElementsByClassName('"+className+"');arr[0].classList.remove('"+className+"');arr[0].innerHTML="+word+";arr[0].classList.remove('"+className+"');"
#removeScripts=removeScripts % (className,className,word)
# dr.execute_script(removeScripts)
# dr.execute_script(removeScripts)

# 5、取出table中的值
#for table in tableList:Python/spider_vcar_vcyber_com/Test/unionTest.py:81


# 1、取出tables所在的div



#dr.close()
