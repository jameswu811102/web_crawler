from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import os


def wait(your_driver, wait_by, until_element, wait_time=30):
    """

    Use to make the driver wait for seconds until the specify element shown

    :param your_driver: webdriver.Chrome() or webdriver.Firefox(), ...etc
    :param wait_by: By.YOUR ATTRIBUTE
    :param until_element: IF FIND THIS ELEMENT, THE EXECUTE WILL GO TO NEXT LINE
    :param wait_time: HOW LONG YOUR DRIVER WILL WAIT
    :return: None

    """
    WebDriverWait(your_driver, wait_time).until(
        EC.presence_of_element_located((wait_by, until_element))
    )


# 設定瀏覽器並開啟，並設定 ActionChains
driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
chrome = webdriver.Chrome(driver_path)
chrome.maximize_window()
actionchain = ActionChains(chrome)

# 找到頁面
url = "https://www.manhuaren.com/manhua-huiyedaxiaojiexiangrangwogaobai--tiancaimendelianaitounaozhan/"
chrome.get(url)

wait(chrome, By.XPATH, "/html/body/div[5]/div[1]")

# 找到要的頁面
chrome.find_element_by_partial_link_text("番外").click()
wait(chrome, By.PARTIAL_LINK_TEXT, "展开全部章节")

# 展開所有頁面
more = chrome.find_element_by_xpath("/html/body/div[5]/a")
chrome.execute_script("arguments[0].click();", more)

# 得到所有章節 (共有幾章)
chapters = chrome.find_element_by_id("detail-list-select-3").find_elements_by_tag_name("a")
len = len(chapters)

# 正式抓取
c = 0
while c < len:
    print(c)
    # 點擊要進去的章節
    try:
        chapter = chrome.find_element_by_xpath("/html/body/div[5]/ul[3]/li[{}]/a".format(c+1))
        chapter_name = chapter.text

        if not os.path.exists(f"C:\\Users\\JamesWu\\Desktop\\{chapter_name}"):
            os.makedirs(f"C:\\Users\\JamesWu\\Desktop\\{chapter_name}")

        chrome.execute_script("arguments[0].click();", chapter)
        time.sleep(2)



        try:
            # 點到章節裡面有廣告 → 處理
            ad = chrome.find_element_by_class_name("lb-win-con").find_element_by_tag_name("img")
            print("有廣告")
            actionchain.move_by_offset(915, 85).click().perform()
            print("廣告關閉")
            time.sleep(3)
        except:
            pass


        page = 1
        for i in range(35):
            try:
                # 找到圖片下載網址
                # chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                img = chrome.find_element_by_class_name("lazy")
                img_url = img.get_attribute("src").split("?")[0]

                # 運用 requests 套件訪問，並下載圖片 ( 否則直接下載會被擋, 用 wget.download() 的方法也會被擋 )
                params = {
                    "Referer": "https://www.manhuaren.com/m250172",
                    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    "sec-ch-ua-mobile": "?0",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                }

                response = requests.get(img_url, params=params)
                with open(f"C:\\Users\\JamesWu\\Desktop\\{chapter_name}\\{page}.jpg", mode="wb") as f:
                    f.write(response.content)
                    print(f"抓取Page{page}")

                chrome.find_element_by_partial_link_text("下一页").click()
                page += 1
                time.sleep(1.5)

            except:
                print(f"{chapter_name}完結")
                break


        if c == 0:
            chrome.back()
            chrome.back()
            chrome.find_element_by_partial_link_text("番外").click()
            wait(chrome, By.PARTIAL_LINK_TEXT, "展开全部章节")

            more = chrome.find_element_by_xpath("/html/body/div[5]/a")
            chrome.execute_script("arguments[0].click();", more)
            c += 1

        else:
            chrome.back()
            chrome.find_element_by_partial_link_text("番外").click()
            wait(chrome, By.PARTIAL_LINK_TEXT, "展开全部章节")

            more = chrome.find_element_by_xpath("/html/body/div[5]/a")
            chrome.execute_script("arguments[0].click();", more)
            c += 1

    except:
        print("已跑完所有章節，準備關閉瀏覽器")


time.sleep(10)
chrome.quit()
