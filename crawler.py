# 爬取京东手机数据，并存储到excel或txt文件中
# 测试时间为2017年7月10日
# !C:\Python\Python35
#_*_ encoding: utf-8 _*_

import requests
from bs4 import BeautifulSoup
import json
import xlwt

# 获取商品名称
urlfirst = "https://list.jd.com/list.html?cat=9987,653,655&page="
urllast = "&sort=sort_dredisprice_asc&trans=1&JL=6_0_0#J_main"
# 打开文件存放京东手机数据
# with open("京东手机信息.txt", 'w') as jdshouji:
xls = xlwt.Workbook()
# 创建第一个表单
sheet = xls.add_sheet("Sheet1")
# 创建表头
sheet.write(0, 0, '商品名称')
sheet.write(0, 1, '价格')
# 从第一行开始记录产品信息
row = 1

# 一页一页获取数据，存入excel文件
for page in range(1, 147):
	# 取得每一个网页URL
	product_html = requests.get(urlfirst + str(page) + urllast)
	soup = BeautifulSoup(product_html.text, 'lxml')
	productname = soup.select("ul.gl-warp li.gl-item div.p-name a em")
	productsku = soup.select("ul.gl-warp li.gl-item div.gl-i-wrap.j-sku-item")
	# for sku in productsku:
	#    print(sku["data-sku"])
	# 构造json地址，每个json请求30个商品信息
	counter = 0
	plist = []
	jsonaddr = ""
	skulist = ""
	jsonfirst = "https://p.3.cn/prices/mgets?callback=jQuery268148&ext=10000000&type=1&area=10_727_728_0&skuIds="
	jsonlast = "&pdbp=0&pdtk=&pdpin=&pduid=1335704484&source=list_pc_front&_=1499430797963"
	for sku in productsku:
		skulist = skulist + "J_" + sku["data-sku"] + "%2C"
		counter += 1
		if counter < 30:
			continue
			# 最后一个skuid要去掉"%2C"
		skulist = skulist[0:-3]
		# 得到json地址
		jsonaddr = jsonfirst + skulist + jsonlast

		jsonstr = requests.get(jsonaddr)
		# 取得json字符串
		jsonstr = jsonstr.text[13:-3]
		# 取得json内对象
		price_json = json.loads(jsonstr)
		for price in price_json:
			plist.append(price['p'])
			# print(price_json['p'])
		jsonaddr = ""
		skulist = ""
		counter = 0
	if skulist:
		# 最后一个skuid要去掉"%2C"
		skulist = skulist[0:-3]
		# 得到json地址
		jsonaddr = jsonfirst + skulist + jsonlast

		jsonstr = requests.get(jsonaddr)
		# 取得json字符串
		jsonstr = jsonstr.text[13:-3]
		# 取得json内对象
		price_json = json.loads(jsonstr)
		for price in price_json:
			plist.append(price['p'])
	for (pname, price) in zip(productname, plist):
# ---------- 商品名称中包含像“™”这样的字符，需要过滤----------
		try:
			# jdshouji.write(pname.text + '\t' + price + '\n')
			sheet.write(row, 0, pname.text)
			sheet.write(row, 1, price)
			row = row + 1
		except:
			# jdshouji.write("本商品包含特殊字符，请自行查询！商品地址：" + urlfirst + str(page) + urllast + "\n")
			error = "本商品包含特殊字符，请自行查询！商品地址：" + urlfirst + str(page) + urllast
			sheet.write(row, 0, error)
			row = row + 1
	plist = []

xls.save('京东手机信息.xls')


