from selenium import webdriver
import time

url="https://car.autohome.com.cn/config/spec/1000001.html"
driver=webdriver.PhantomJS()

driver.get(url)

print(driver.page_source)