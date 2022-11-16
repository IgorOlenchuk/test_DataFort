import os
import asyncio
import requests
import json
import pandas as pd
import time
import datetime
import logging
from dotenv import load_dotenv
from pandas import json_normalize
from db.core import engine
from utils import config
from cities import CITY_ID


async def main():
    while True:
        try:
            await upload_from_api()
        except Exception as e:
            logging.exception(e)
        await asyncio.sleep(3600)


async def upload_from_api():
    df = pd.DataFrame()
    for city in CITY_ID.keys():
        try:
            current_date = datetime.datetime.now().isoformat(timespec='minutes') 
            res = requests.get(config.URL,
                        params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': config.API_KEY})
            data = res.json()
            data['dt'] = current_date
            data['weather'] = data['weather'][0]['description']
            df_request = json_normalize(data)
            df = pd.concat([df, df_request])
        except Exception as e:
            print("Exception:", e)
            pass
    await upload_to_db(df)


async def upload_to_db(df):
    try:
        pd.read_sql_table(config.NAME_TABLE, con=engine)
        df.to_sql(config.NAME_TABLE, con=engine, if_exists='append', index=False)
    except:
        df.to_sql(config.NAME_TABLE, con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
