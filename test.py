import pymongo
url = "mongodb://phongthuyvanan:Thanhtruc05062017@phongthuyvanan.vn:27017"
db = "phongthuyvanan.vn"
mgoclient = pymongo.MongoClient(url)
mgodb = mgoclient[db]
topCol = mgodb[table]
keywords = topCol.count_documents({'serp_result':[]})