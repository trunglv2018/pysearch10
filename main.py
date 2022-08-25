

import pymongo
from slugify import slugify
from search import search
import telegram

def crawl(app_url:str, url:str, db:str, table:str, tld:str, lang:str):
    mgoclient = pymongo.MongoClient(url)
    mgodb = mgoclient[db]
    topCol = mgodb[table]
    keywords = topCol.find({'serp_result':[]})
    # Strips the newline character
    for kw in keywords:
        keyword = kw['keyword']
        print("crawl Kw ")
        serpResults = []
        try:
            for d in search(keyword, tld=tld, lang=lang, num=15):
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
    telegram_notify = telegram.Bot("5550854606:AAEsD8oDz3YRsndF_hZ7KxHiu8NXooWGV7o")
    telegram_notify.send_message(chat_id="-696126162", text=str(app_url)+'/crawl?appurl='+str(app_url)+'&dburl='+url+'&db='+db+'&table='+table+'&appurl='+app_url+'&tld='+tld+'&lang='+lang,
                                parse_mode='Markdown')

def crawl_bulk(topCol, tld:str, lang:str, kw):
    serpResults = []
    for d in search(kw['keyword'], tld=tld, lang=lang, num=15):
        if(d['title']==''):
            continue
        if('phohen' in d['link']):
            continue
        d['slug']= slugify(d['title']) 
        serpResults.append(d)
    if(len(serpResults)==0):
        return
    result = topCol.update_one({'_id':kw['_id']},{'$set':{'serp_result':serpResults}})
    print('insert result', result)

# crawl('top5','')

from typing import Union

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
class MgDBModel(BaseModel):
    url: str
    table_name: str
    db_name: str
    app_url: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/crawl")
@app.get("/crawl")
def read_item(appurl, dburl, db, table, tld, lang, background_tasks: BackgroundTasks):
    background_tasks.add_task(
            crawl,appurl, dburl, db, table, tld, lang)
    return {
        "url":appurl,
    }


@app.get("/crawl_bulk")
def read_item(appurl, dburl, db, table, tld, lang, background_tasks: BackgroundTasks):
    mgoclient = pymongo.MongoClient(dburl)
    mgodb = mgoclient[db]
    topCol = mgodb[table]
    keywords = topCol.find({'serp_result':[]}).skip(0).limit(500)
    # Strips the newline character
    for kw in keywords:
        background_tasks.add_task(
                crawl_bulk, topCol, tld, lang, kw)
    return {
        "url":appurl,
    }