import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

# Record the search window
search_windows = driver.current_window_handle

# Deal with Baidu search
elem = driver.find_element_by_id("kw")
elem.clear()

elem.send_keys("pycon")
elem.send_keys("python selenium programmer")
search = driver.find_element_by_id("su")
search.click()
search.get_property()

# Open a registration page
login = driver.find_element_by_name('tj_login')
login.click()
driver.find_element_by_link_text(u'立即注册').click()


driver.quit()
print("quit")
driver.close()