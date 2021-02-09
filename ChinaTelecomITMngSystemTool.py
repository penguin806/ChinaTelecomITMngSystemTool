# v1.0	Feb 2nd, 2021
# Repo: https://github.com/penguin806/ChinaTelecomITMngSystemTool.git
import requests
import datetime
import time
import json
from requests_html import HTMLSession

#用户名
userName = '0746zhoud'
# cookie
jSessionId = "B63CD5079B5F685B3384A6EC958BFCF0"
# 时间间隔
timeInterval = 1
posId = 'w20789'

def requestEventPage():
	session = HTMLSession()
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
	cookies = {"JSESSIONID": jSessionId}
	url = 'http://134.176.30.19:9081/ITMS/newView/event/eventHandle.jsp'

	result = session.get(url, cookies = cookies, headers = headers)
	lockKey = result.html.find('#lockKey')
	toolUrl = result.html.find('#toolUrl')

	lockKey=lockKey[0].attrs['value']
	toolUrl=toolUrl[0].attrs['value']


	form = {
		'posID': posId,
		'reqDealL':'requestService',
		'areaId': '746',
		'filterCon':'', 
		'sendGroupValue':'',
		'employeeId': userName,
		'toolUrl': toolUrl,
		'selectedReq':'',
		'isSerDesk': 'true',
		'lockKey': lockKey,
		'console': posId + ':requestService',
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
		timeDiff = (datetime.datetime.now() - datetime.datetime.strptime(row['createdate'], '%Y-%m-%d %H:%M:%S')).total_seconds()
		# print(timeDiff)
		if row["statusinfo"] == '新生成' and row["remindername"] == '' and row['sourse'] == '10000号系统' and timeDiff <= 20:
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
					'posID' : posId,
					'lockKey' : lockKey
					# 'lockKey' : 'A16F651F5E00C3816FA03E15D65851CA1E6C6F636B3C3C3037343674616E67721346221V20CA4'
				},
				cookies = cookies
			)
			if result.text == "0":
				print(row["statusinfo"] + " " + row["requestid"])
				print(row["title"])
				print("Response: "  + str(result.status_code) + " / " + result.text + "\n\n")


if __name__ == '__main__':
    while True:
        print(time.strftime('%Y-%m-%d %X',time.localtime()))
        requestEventPage()
        time.sleep(timeInterval)