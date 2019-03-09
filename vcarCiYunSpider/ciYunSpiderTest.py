import time,json
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = '525591772@qq.com'
PASSWORD = 'gh200426'

CHAOJIYING_USERNAME = '18856009935'
CHAOJIYING_PASSWORD = 'gh200426'
CHAOJIYING_SOFT_ID = '    897500'
CHAOJIYING_KIND = '9004'

import requests
from hashlib import md5


class Chaojiying(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


class CrackTouClick():
    def __init__(self):
        self.url = 'http://safety.autohome.com.cn/userverify/index?locnum=104092&backurl=//k.autohome.com.cn%2Fspec%2F1000004%2Fge5'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        self.open()

    def __del__(self):
        self.browser.close()

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """

        print("request--------------->")
        self.browser.get(self.url)

        print("request==============>")
        time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
        find = True
        ele = None
        #网路不给力class，点击重试：geetest_reset_tip_content
        try:
            ele=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
            # ele = self.browser.find_element_by_css_selector(".geetest_radar_tip")
        except Exception as e:
            find = False

        if find:
            # 如果存在网络不给力则先解决网络不给力
            noNet=None
            try:
                noNet=self.browser.find_element_by_class_name("geetest_reset_tip_content")
            except Exception as e:
                pass
            # 需要判断文字内容：
            # if noNet != None:
            #     noNet.click()
            #     time.sleep(0.5)
            ele.click()

        # email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        # password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        # email.send_keys(self.email)
        # password.send_keys(self.password)

    # 此方法不需要，验证码已加载
    def get_touchclick_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit')))
        return button

    def get_touch_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        print("befor presence img")
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        print("already presence img")
        return element

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        if ('string' == typeof(obj)) {
            obj = document.getElementById(obj);
        }
        var ro = obj.getBoundingClientRect();
        //document.documentElement.clientTop 在IE67中始终为2，其他高级点的浏览器为0
        ro.top = ro.top - document.documentElement.clientTop;
        //document.documentElement.clientLeft 在IE67中始终为2，其他高级点的浏览器为0
        ro.left = ro.left - document.documentElement.clientLeft;
        ro.Width = ro.width || ro.Right - ro.Left;
        ro.Height = ro.height || ro.Bottom - ro.Top;
        return ro
        """
        # element = self.get_touch_element()

        # js="""
        # obj=document.getElementsByClassName('geetest_item_img')[0]
        # var ro = obj.getBoundingClientRect();
        # //document.documentElement.clientTop 在IE67中始终为2，其他高级点的浏览器为0
        # ro.top = ro.top - document.documentElement.clientTop;
        # //document.documentElement.clientLeft 在IE67中始终为2，其他高级点的浏览器为0
        # ro.left = ro.left - document.documentElement.clientLeft;
        # ro.Width = ro.width || ro.Right - ro.Left;
        # ro.Height = ro.height || ro.Bottom - ro.Top;
        # return ro
        # """
        #
        # ro=self.browser.execute_script(js)
        # print(ro)
        # print(type(ro))
        #
        # top=ro['top']
        # bottom=int(ro['top'])+int(ro['height'])
        # left=ro['left']
        # right=int(ro['left'])+int(ro['width'])

        element = self.get_touch_element()
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print("location:top  bottom  left right")
        print((top,bottom,left,right))
        # print((top+110, bottom+403, left+505, right+843))
        # 火狐left+545
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        # 由于Mac分辨率高，截图好尺寸偏大，需要进行缩小,原本尺寸为：2400 ＊ 1430
        # print("sssccccrrrrrsssshhhott")
        # print(screenshot.width,screenshot.height)
        screenshot=screenshot.resize((int(screenshot.width * 0.48) ,int(screenshot.height * 0.48)))
        return screenshot

    def get_touch_click_image(self, name='/Users/guohan/Desktop/tt.png'):
        """
        获取验证码图片
        :param name:图片对象
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        # 获取整个屏幕截图
        screenshot = self.get_screenshot()
        screenshot.save('/Users/guohan/Desktop/sc.png')
        # 裁剪验证码图片
        captcha = screenshot.crop((left-25, top-50, right-25, bottom-50))
        captcha.save(name)


        # self.browser.save_screenshot(name)
        element=self.get_touch_element()
        #
        # left = element.location['x']
        # top = element.location['y']
        # right = element.location['x'] + element.size['width']
        # bottom = element.location['y'] + element.size['height']
        #
        # im = Image.open('/Users/guohan/Desktop/1.jpg')
        # im = im.crop((left, top, right, bottom))
        # im.save('/Users/guohan/Desktop/1.jpg')
        # print(top,bottom,left,right)

        # screenshot = self.browser.get_screenshot_as_png()
        # with open(name, "wb")as f:
        #     f.write(screenshot)

        return captcha

    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result:识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations=[]
        for group in groups:
            x,y=group.split(",")
            y =int(y) - 26
            x = int(x)
            locations.append([x,y])
        # locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations:点击位置
        :return: None
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touch_element(), location[0], location[1]).click().perform()

    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit')))
        button.click()

    def login(self):
        """
        登陆
        :return:None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, '_submit')))
        submit.click()
        print("登陆成功")

    def crack(self):
        """
        破解入口
        :return:None
        """
        # 点击验证按钮
        # button = self.get_touchclick_button()
        # button.click()
        # 获取验证码图片
        image = self.get_touch_click_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='png')
        # 识别验证码
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        print(">>>>>>>>>>>>>>>>>>>>>>locations")
        print(locations)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 判定是否成功
        success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "touchlick_hod_note"), '验证成功'))
        print(success)

        # # 失败后重试
        # if not success:
        #     self.crack()
        # else:
        #     self.login()



crack = CrackTouClick()
crack.crack()