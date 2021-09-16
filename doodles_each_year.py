from urllib.request import urlopen, urlretrieve
import json
import os
import datetime as dt

start_year = int(input("起始抓取年份(最低:1998): "))

# 抓取年份
while 1998 <= start_year <= dt.datetime.today().year:
	for month in range(12):
		url = "https://www.google.com/doodles/json/" + str(start_year) + "/" + str(month + 1) + "?hl=zh-TW"
		res = urlopen(url)
		imgs = json.load(res)

		print("嘗試抓取", url)

		# 確認抓取的月份是否真的存在，
		if len(imgs) != 0:
			print(month + 1, "月存在抓取中")
			for img in imgs:
				try:
					img = img["high_res_url"]
					img_url = "https:" + img
				except:
					img = img["url"]
					img_url = "https:" + img

				if not os.path.exists("Doodles/" + str(start_year) + "Month" + str(month + 1)):
					os.makedirs("Doodles/" + str(start_year) + "Month" + str(month + 1))

				img_name = "Doodles/" + str(start_year) + "Month" + str(month + 1) + "/" + img_url.split("/")[-1]
				urlretrieve(img_url, img_name)

		# 不存在
		else:
			continue

	start_year += 1