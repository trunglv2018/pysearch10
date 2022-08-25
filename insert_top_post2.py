from datetime import datetime
import secrets
import string
import pymongo
from slugify import slugify

kwFilePath = 'key_2'
mgoclient = pymongo.MongoClient("mongodb://phongthuyvanan:Thanhtruc05062017@phongthuyvanan.vn:27017")
mgodb = mgoclient["phongthuyvanan"]
top5Col = mgodb["top42"]
kwFile = open(kwFilePath, 'r',encoding="utf8")
kwLines = kwFile.readlines()
count = 0
# print(getLastKwNum())
# Strips the newline character
for kw in kwLines:
    print("crawl Kw {}".format(kw))
    topPost = {}
    ts = datetime.timestamp(datetime.now())
    topPost['created_at'] = int(ts)
    topPost['updated_at'] = int(ts)
    topPost['keyword'] = kw
	
    topPost['slug'] = slugify(kw)
    topPost['code'] = ''.join(secrets.choice(string.digits) for x in range(10))  
    serpResults = []
    topPost['serp_result'] = serpResults
    result = top5Col.insert_one(topPost)
    print('insert result', result)