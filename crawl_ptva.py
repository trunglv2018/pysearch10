

import time
import pymongo
from slugify import slugify
from search import search
import sys, getopt


def crawl(table, app_url):
    mgoclient = pymongo.MongoClient("mongodb://phongthuyvanan:Thanhtruc05062017@phongthuyvanan.vn:27017")
    mgodb = mgoclient["phongthuyvanan"]
    topCol = mgodb[table]
    keywords = topCol.find({'serp_result':[]})
    # Strips the newline character
    for kw in keywords:
        keyword = kw['keyword']
        print("crawl Kw ")
        serpResults = []
        try:
            for d in search(keyword, tld='com.vn', lang='vi', num=15):
                if(d['title']==''):
                    continue
                if('phohen' in d['link']):
                    continue
                d['slug']= slugify(d['title']) 
                serpResults.append(d)
            if(len(serpResults)==0):
                continue
            result = topCol.update_one({'_id':kw['_id']},{'$set':{'serp_result':serpResults}})
            print('insert result', result)
        except:
            break
    time.sleep(300)
    # telegram_notify = telegram.Bot("5550854606:AAEsD8oDz3YRsndF_hZ7KxHiu8NXooWGV7o")
    # telegram_notify.send_message(chat_id="-696126162", text=str(app_url)+'?table='+str(table)+'&appurl='+app_url,
    #                             parse_mode='Markdown')

def main(argv):
    tableName = 'top1'
    try:
        tableName = sys.argv[1]
    except getopt.GetoptError:
        print('test.py table name')
        sys.exit(2)
    print(tableName)
    crawl(tableName,'')
if __name__ == "__main__":
   main(sys.argv[1:])