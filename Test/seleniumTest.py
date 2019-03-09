
#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
#browser.get("file:///Users/guohan/Desktop/wei.html")
#browser.get("file:///Users/guohan/Desktop/sub.html")
browser.get("https://car.autohome.com.cn/config/spec/20211.html#pvareaid=3454569")
time.sleep(2)
configData=browser.find_element_by_id("auto-header1")
print(configData)


# Record the search window
# search_windows = driver.current_window_handle

# Deal with Baidu search
# elem = driver.find_element_by_id("kw")
# elem.clear()
#
# elem.send_keys("pycon")
# elem.send_keys("python selenium programmer")
# search = driver.find_element_by_id("su")
# search.click()
#
# # Open a registration page
# login = driver.find_element_by_name('tj_login')
# login.click()
# driver.find_element_by_link_text(u'立即注册').click()

try:
    # ele=browser.find_element_by_id("name")
    # print(ele.value_of_css_property("content"))
    # print(ele.get_attribute("name"))
    # print(ele.text)
    # print(ele.get_property("id"))
    # guohan=browser.find_element_by_css_selector(css_selector=".hw-01")
    # print(guohan.text)
    # print(guohan.get_property("class"))
    # print(guohan.value_of_css_property("content"))

    #找到输入框元素
    # input=browser.find_element_by_id("kw")
    # #输入文字
    # input.send_keys("Python")
    # # 输入enter，触发enter事件
    # input.send_keys(Keys.ENTER)
    # #等待请求
    # wait=WebDriverWait(browser,10)
    # wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    # #print(browser.current_url)
    # #print(browser.get_cookies())
    # #print(browser.page_source)
    # print(input.get_property("class"))
    # #根据属性名获取属性值
    # print(input.get_attribute("class"))
    # print(input.get_attribute("name"))
    #print(input.tag_name)
    #print(input.value_of_css_property('font'))
    #browser.execute_script()
    # elements=browser.find_element(By.TAG_NAME,"p")
    # print(elements.text)
    # elements2 = browser.find_elements(By.CSS_SELECTOR,".tbcs")
    # print(len(elements2))
    # for ele in elements2:
    #     spanList=ele.find_elements(By.TAG_NAME,"span")
    #     for span in spanList:
    #         print(span.get_property("class"))
    #
    # browser.find_elements(By.CSS_SELECTOR, ".tbcs")
    # #browser.get("http://www.baidu.com")
    # print(browser.page_source)
    pass







finally:
    browser.close()


