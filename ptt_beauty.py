import requests
from urllib.request import urlretrieve
from shutil import copyfileobj
from bs4 import BeautifulSoup
import os


url = "https://www.ptt.cc/bbs/Beauty/M.1618635139.A.7AA.html"
# 避免被分級擋住，請加入cookies
response = requests.get(url, cookies={"over18": "1"})
html = BeautifulSoup(response.text)

# 將留言區都刪除
for dis in html.find_all("div", class_="push"):
    dis.extract()

# 正式抓取
main_article = html.find("div", id="main-content")
hrefs = main_article.find_all("a")
Filter = ["jpeg", "jpg", "png", "gif", "tif", "bmp"]

for href in hrefs:
    # 假設網址副檔名含有圖片的格式名稱
    if href.text.split(".")[-1] in Filter:

        # 打開圖片(bin，這樣才能使用shutil複製, 影音及圖片=>stream參數須設定)
        img_bin = requests.get(href.text, stream=True)

        # 將上面打開的圖片直接複製過去
            # 先創用來存放圖片的資料夾
        dir_name = html.find("title").text.split("-")[0].replace(" ", "")
        if not os.path.exists("./" + dir_name):
            os.makedirs("./" + dir_name)
            # 開新檔案準備複製寫入圖片(記得設立檔案名稱)
        file_name = dir_name + "/" + href.text.split("/")[-1]
        with open(file_name, "wb") as f:
            print("正在下載:", href.text)
            copyfileobj(img_bin.raw, f)

        # 或是直接用以下也可以
        # urlretrieve(href.text, "./" + dir_name + "/" + file_name)

    else:
        continue
