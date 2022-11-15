import os
import asyncio
import requests
import psycopg2
import json
import pandas as pd
import time
import datetime
from pandas import json_normalize
from sqlalchemy import create_engine

#1850147 Tokio, Japan
#1273294 Delhi, IN
#1796236 Shanghai, CN
#3448439 São Paulo, BR
#3530597 Mexico City, MX
#360630 Cairo, EG
#1275339 Mumbai, IN
#1816670 Beijing, CN
#1185241 Dhaka, BD
#1853909 Osaka, JP
CITY_ID = [1850147, 1273294, 1796236, 3448439, 3530597, 360630, 1275339, 1816670, 1185241, 1853909]

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
API_KEY = os.getenv('API_KEY')


async def main():

    while True:
        df = pd.DataFrame()
        try:
            connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            cursor = connection.cursor()

            for city in CITY_ID:
                try:
                    current_date = datetime.datetime.now().strftime('%Y%m%d')
                    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': API_KEY})
                    data = res.json()
                    df_request = json_normalize(data)
                    df = pd.concat([df, df_request])
                    cursor.execute("INSERT INTO yami(js1) VALUES ('{}')".format(json.dumps(data)))
                    connection.commit()
                    count = cursor.rowcount
                    print(count, "Record inserted successfully into mobile table")
                except Exception as e:
                    print("Exception (weather):", e)
                    pass
                df['dt'] = current_date
        
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


        await asyncio.sleep(10)


asyncio.run(main())
