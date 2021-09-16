from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 等待用
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 抓取圖片用功能
import os
import wget


# 先建立一個等待用的功能
def wait(your_driver, wait_by, until_element, wait_time=30):
    """

    :param your_driver: webdriver.Chrome() or webdriver.Firefox(), ...etc
    :param wait_by: By.YOUR ATTRIBUTE
    :param until_element: IF FIND THIS ELEMENT, THE EXECUTE WILL GO TO NEXT LINE
    :param wait_time: HOW LONG YOUR DRIVER WILL WAIT
    :return: None

    """
    WebDriverWait(your_driver, wait_time).until(
        EC.presence_of_element_located((wait_by, until_element))
    )


key_words = input("我想在IG上搜索 (e.g. #起司蛋餅)： ")

chrome_driver = "C:\\Users\\JamesWu\\Desktop\\Selenium\\chromedriver.exe"
chrome = webdriver.Chrome(chrome_driver)

# 去IG頁面
chrome.get("https://www.instagram.com/")

wait(chrome, By.NAME, "username")
wait(chrome, By.NAME, "password")

# 找到需要的欄位，準備輸入登入資料，然後登入 (不要記住登入資訊、不要通知)
account = chrome.find_element_by_name("username")
account.clear()
account.send_keys("")
password = chrome.find_element_by_name("password")
password.clear()
password.send_keys("")

wait(chrome, By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")

logging = chrome.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
logging.click()

wait(chrome, By.CLASS_NAME, "cmbtv")


no_remember = chrome.find_element_by_class_name("cmbtv")
no_remember.click()

wait(chrome, By.CLASS_NAME, "HoLwm")

no_notify = chrome.find_element_by_class_name("HoLwm")
no_notify.click()

wait(chrome, By.CLASS_NAME, "x3qfX")

# 搜尋你自己要的資訊 (到關鍵字欄位輸入你自己要的內容)
search = chrome.find_element_by_class_name("x3qfX")
search.clear()

search.send_keys(key_words)
wait(chrome, By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[1]/div")
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)

wait(chrome, By.XPATH, "/html/body/div[1]/section/main/article/div[1]/h2/div")
time.sleep(3)   # 給予讀取圖片的時間



###########################################
###### 若想要下載多張，則需要將滾輪往下滾，並查看規律 (目前為 1批/大約載入兩次圖片) #######
###########################################
""" 可參閱 https://selenium-python.readthedocs.io/faq.html#how-to-scroll-down-to-the-bottom-of-a-page """
""" 使用方式為 driver.execute_script("window.scrollBy(0, document.body.scrollHeight) """
""" 或也可使用 driver.execute_script("window.scrollTo(0, document.body.scrollHeight) """

# 建立存放圖片資料夾

if not os.path.exists("./{}".format(key_words[1:])):
    os.makedirs("./{}".format(key_words[1:]))


# 先抓最新
img_count = 0
imgs_new = chrome.find_elements_by_class_name("FFVAD")
for img in imgs_new[0:9]:
    save_path = os.path.join("./{}/{}{}.jpg".format(key_words[1:], key_words[1:], img_count))
    img_url = img.get_attribute("src")
    wget.download(url=img_url, out=save_path)
    img_count += 1

# 再抓新載入
img_count = img_count
for n in range(20):
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2.5)
    # 滾動4次抓一批圖
    if n % 4 == 0:
        imgs_old = chrome.find_elements_by_class_name("FFVAD")
        for img in imgs_old[9:]:
            save_path = os.path.join("./{}/{}{}.jpg".format(key_words[1:], key_words[1:], img_count))
            img_url = img.get_attribute("src")
            wget.download(url=img_url, out=save_path)
            img_count += 1


# 關閉瀏覽器
time.sleep(15)
chrome.close()