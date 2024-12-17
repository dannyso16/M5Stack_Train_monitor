#参考　https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/0a38c1
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI

def is_hankyu_on_schedule() -> bool:
    """Yahoo乗り換え案内のサイトから路線の遅延状況を取得し、
    遅延がなければTrue、遅延があればFalseを返す。
    TODO: URLは阪急京都線versionです。
    """
    URL = 'https://transit.yahoo.co.jp/traininfo/detail/306/0/' 
    r = requests.get(URL)
    s = BeautifulSoup(r.text, 'html.parser')
    # API_title = s.find('title').text
    API_status_detail = s.find('div', class_='elmServiceStatus').find('p').text
    print('is_hankyu_on_schedule()  get status: OK')
    return API_status_detail.startswith("現在、事故・遅延に関する情報はありません")


def get_next_departure_time(departure_station:str, arrival_station:str) -> str:
    """阪急のサイトから、出発駅と到着駅の間の、次の電車の出発/到着時刻を取得し、
    出発時刻を　HH:MM　形式で返す。
    """
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    url = 'https://www.hankyu.co.jp/station/search/index.php' \
        + '?from=' + urllib.parse.quote(departure_station) \
        + '&to=' + urllib.parse.quote(arrival_station) \
        + '&mode=result&ymd=' + now.strftime("%Y-%m-%d") \
        + '&hm=' + now.strftime("%H") + urllib.parse.quote(':') + str(int(now.strftime("%M"))+1) \
        + '&type=0&tp=0&via='
    
    # スクレイピング
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    time_text = s.find('li', class_='time').get_text()

    departure_time, arrival_time = time_text.split(' → ')
    
    print(f'{departure_station} 発:{departure_time}')
    print(f'{arrival_station} 着:{arrival_time}')
    
    return departure_time

app = FastAPI()
@app.get("/trainapi/status")
async def status():
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    departure_station = '茨木市'
    arrival_station = '河原町'

    next_time = get_next_departure_time(departure_station, arrival_station)
    current_time = now.strftime("%H:%M")
    condition = "ONTIME" if is_hankyu_on_schedule() else "DELAY"
 
    return {
        "statusCode": 200
        ,"body": json.dumps({
            "next_time": next_time,
            "current_time": current_time,
            "condition": condition
        })
    }
