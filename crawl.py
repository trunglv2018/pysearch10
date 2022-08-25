from json import load
from urllib import request as urlrequest

import threading

def set_interval(func, sec):
	def func_wrapper():
		set_interval(func, sec) 
		func()  
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t
proxy_host = ''    # host and port of your proxy

def get_proxy(apiKey):
	print('lay ip moi')
	req = urlrequest.Request('http://proxy.tinsoftsv.com/api/changeProxy.php?key='+apiKey+'&location=2')
	response = urlrequest.urlopen(req)
	res = load(response)
	print(res)
	if (res['proxy'] != ''):
		proxy_host = res['proxy']
		print('da doi proxy ', proxy_host)
		proxy_host = ''
    	

# set_interval(func=get_proxy('TLgL2Md9RG56xlKpkSBQSktZAFzBsYtswUEBaa'), sec=110)
url = 'http://www.httpbin.org/ip'

req = urlrequest.Request(url)
print('su dung proxy', proxy_host)
req.set_proxy('117.0.75.42:36607', 'http')

response = urlrequest.urlopen(req)
print(response.read().decode('utf8'))
