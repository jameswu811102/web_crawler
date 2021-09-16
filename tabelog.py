'''
事前工具、知識

1. HTML 網頁標籤閱讀

2. bs4 (BeautifulSoup)工具的應用

3. 學習異常處理try & except使用

'''

# 以爬取日文美食排行榜「食べログ」為例子

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError          # try & except 異常處理使用


Page = 1

while True:
    print("第" + str(Page) + "頁")

    try:
        url = "https://tabelog.com/tw/hiroshima/rstLst/" + str(Page) + "?SrtT=rt"
        response = urlopen(url)  # 打開網頁
        html = BeautifulSoup(response)  # 解析網頁

    except HTTPError:
        print("無此頁，第" + str(Page-1) + "頁為最終頁")
        break

    Page = Page + 1

    # ↓解析後尋找要的資料，先找每間餐廳
    rsts = html.find_all("li", class_ = "list-rst js-list-item")

    # ↓再用for in 迴圈來得到每間餐廳的詳細需要資料
    for rst in rsts:
        EngName = rst.find("a", class_ = "list-rst__name-main")
        JapName = rst.find("small", class_ = "list-rst__name-ja")
        Area = rst.find("li", class_ = "list-rst__area")
        Catalog = rst.find("li", class_ = "list-rst__catg")
        RankValue = rst.find("b", class_ = "c-rating__val")
        Prices = rst.find_all("span", class_="c-rating__val")       # 注意！含午餐及晚餐價

    #   打印最終每間餐廳擷錄出來的資訊
        print("餐廳名(拼音):", EngName.text)
        print("餐廳名(日文):", JapName.text)
        print("餐廳所在縣市:", Area.text.strip())
        print("餐廳分類:", Catalog.text)
        print("餐廳評價:", RankValue.text)
        print("餐廳價格(午餐):", Prices[1].text)
        print("餐廳價格(晚餐):", Prices[0].text)
        print("詳細餐廳內容網址:", EngName["href"])
        print("-" * 20 + "分隔" + "-" * 20)






