import os
import asyncio
import requests
import psycopg2
import json
import pandas as pd
import time
import datetime
from pandas import json_normalize
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.types import Integer

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
API_KEY = "51f9d590eeeb790b4e8e2d218307f523"


async def main():

    while True:
        df = pd.DataFrame()
        eng = create_engine("postgresql://postgre:postgre@127.0.0.1/weather_db")
        connection = psycopg2.connect(database='weather_db', user='postgre', password='postgre', host='127.0.0.1', port=5432)

        try:
            cursor = connection.cursor()

            for city in CITY_ID:
                try:
                    current_date = datetime.datetime.now().isoformat(timespec='minutes') 
                    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': API_KEY})
                    data = res.json()
                    data['dt'] = current_date
                    data['weather'] = data['weather'][0]['description']
                    df_request = json_normalize(data)
                    df = pd.concat([df, df_request])
                except Exception as e:
                    print("Exception (weather):", e)
                    pass
            try:
                pd.read_sql_table('city_weather', "postgresql://postgre:postgre@127.0.0.1/weather_db")
                df.to_sql('city_weather', con=eng, if_exists='append', index=False)
            except:
                df.to_sql('city_weather', con=eng, if_exists='replace', index=False)

            cursor.execute(("SELECT * FROM city_weather"))
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
        
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


        await asyncio.sleep(3600)


asyncio.run(main())
