import requests
from requests_html import HTMLSession
import json

session = HTMLSession()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
cookies={"JSESSIONID": "98FDFDF0B0FABCD59BAC36B02E21985D"}
url = 'http://134.176.30.19:9081/ITMS/newView/event/eventHandle.jsp'

result = session.get(url, cookies = cookies, headers = headers)
lockKey = result.html.find('#lockKey')
toolUrl = result.html.find('#toolUrl')

# print(result)
lockKey=lockKey[0].attrs['value']
toolUrl=toolUrl[0].attrs['value']


form = {
	'posID':'w746005', 
	'reqDealL':'requestService',
	'areaId': '746',
	'filterCon':'', 
	'sendGroupValue':'',
	'employeeId': '0746tangr',
	'toolUrl': toolUrl,
	'selectedReq':'',
	'isSerDesk': 'true',
	'lockKey': lockKey,
	'console': 'w746005:requestService',
	'qareaId': '100',
	'orderSource': '',
	'orderNo': '',
	'rows': '20',
	'page': '1',
	'sortName': 'priority',
	'sortOrder': 'desc'
}

result = requests.post('http://134.176.30.19:9081/ITMS/Event/eventHandle.do?method=queryAllEventHandle', data = form, cookies = cookies)
resultJson=json.loads(result.content)

resultJson["rows"].reverse()
for row in resultJson["rows"]:
	print('\n\n\n\n')
	if row["statusinfo"] == '新生成' and row["remindername"] == '':
		# print(row["statusinfo"] + " " + row["requestid"])
		# print(row["title"])
		result = requests.post(
			'http://134.176.30.19:9081/ITMS/RequestManager/initDispatch.do',
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
				'X-Requested-With': 'XMLHttpRequest'
			},
			params = {
				'method' : 'enableLock',
				'reqId' : row["requestid"],
				'childId' : 1,
				'posID' : 'w746005',
				'lockKey' : lockKey
				# 'lockKey' : 'A16F651F5E00C3816FA03E15D65851CA1E6C6F636B3C3C3037343674616E67721346221V20CA4'
			},
			cookies = cookies
		)
		if result.text == "0":
			print(row["statusinfo"] + " " + row["requestid"])
			print(row["title"])
			print(str(result.status_code) + " / " + result.text)