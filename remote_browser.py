from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 給瀏覽器載入資料等待用
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# 將等待的程式碼製作成功能
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

"""
上一頁 driver.back()
下一頁 driver.forward()
點擊按鈕 html_element.click()
"""


#　事先找好　chrome 的 driver 並設置一個變數來儲存驅動檔案路徑
chrome_driver = "C:\\Users\\JamesWu\\Desktop\\Selenium\\chromedriver.exe"

# 開啟瀏覽器
chrome = webdriver.Chrome(chrome_driver)

# 示範用 Dcard
chrome.get("https://www.dcard.tw/f")
wait(chrome, By.CLASS_NAME, "dz5d85-0")

query = chrome.find_element_by_name("query")

# 搜尋最好先清空
query.clear()

query.send_keys("比特幣")
query.send_keys(Keys.RETURN)
wait(chrome, By.CLASS_NAME, "sc-3yr054-1")

titles = chrome.find_elements_by_class_name("tgn9uw-3")

title_ls = []

for title in titles:
    title_ls.append(title.text)

print(title_ls)

link = chrome.find_element_by_link_text(title_ls[0])
link.click()
time.sleep(1.5)
chrome.back()
chrome.back()
chrome.forward()


# 若要關閉你的瀏覽器
time.sleep(15)
chrome.quit()