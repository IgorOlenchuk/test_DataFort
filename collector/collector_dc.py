import os
import aiohttp
import asyncio
import json
import time
import datetime
import logging
from dataclasses import dataclass, field
from db.core import engine
from utils import config
from cities import CITY_ID
from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, registry


mapper_registry = registry()


async def main():
    while True:
        try:
            await upload_from_api()
        except Exception as e:
            logging.exception(e)
        await asyncio.sleep(3600)


@mapper_registry.mapped
@dataclass
class CityWeather:
    __table__ = Table(
        config.NAME_TABLE,
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("date", String(16), nullable=False),
        Column("city", String(30), nullable=False),
        Column("weather", String(30), nullable=False), 
        Column("main_temp", Float(6), nullable=False),
        Column("main_feels_like", Float(6), nullable=False),
        Column("main_temp_min", Float(6), nullable=False),
        Column("main_temp_max", Float(6), nullable=False),
        Column("main_pressure", Integer, nullable=False),
        Column("main_humidity", Integer, nullable=False),
        Column("wind_speed", Float(6), nullable=False),
    )
    id: int = field(init=False, default_factory=int, metadata={"sa": Column(Integer, primary_key=True)})
    date: str = field(default=None, metadata={"sa": Column(String(16))})
    city: str = field(default=None, metadata={"sa": Column(String(30))})
    weather: str = field(default=None, metadata={"sa": Column(String(30))})
    main_temp: float = field(default=None, metadata={"sa": Column(Float(6))})
    main_feels_like: float = field(default=None, metadata={"sa": Column(Float(6))})
    main_temp_min: float = field(default=None, metadata={"sa": Column(Float(6))})
    main_temp_max: float = field(default=None, metadata={"sa": Column(Float(6))})
    main_pressure: int = field(default=None, metadata={"sa": Column(Integer)})
    main_humidity: int = field(default=None, metadata={"sa": Column(Integer)})
    wind_speed: float = field(default=None, metadata={"sa": Column(Float(6))})
    '''
        При нагревании уменьшается атмосферное давление.
        При охлаждении -увеличивается.
        Следовательно, с изменением температуры воздуха непрерывно меняется и давление.
        При повышении температуры относительная влажность уменьшается,
        При понижении температуры относительная влажность увеличивается.
    '''


async def upload_from_api():
    current_date = datetime.datetime.now().isoformat(timespec='minutes') 
    for city in CITY_ID.keys():
        async with aiohttp.ClientSession() as session:
            async with session.get(config.URL, params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': config.API_KEY}) as res:
                data = await res.json()
                data['dt'] = current_date
                data['weather'] = data['weather'][0]['description']
            await upload_to_db(CityWeather(
                            data['dt'],
                            data['name'],
                            data['weather'],
                            data['main']['temp'],
                            data['main']['feels_like'],
                            data['main']['temp_min'],
                            data['main']['temp_max'],
                            data['main']['pressure'],
                            data['main']['humidity'],
                            data['wind']['speed']
                            ))


async def upload_to_db(CityWeather):
    Session = sessionmaker(engine)
    cityweather_obj = MetaData(CityWeather)
    city_weater = Table(
        config.NAME_TABLE,
        cityweather_obj,
        Column("date", String(16), nullable=False),
        Column("city", String(30), nullable=False),
        Column("weather", String(30), nullable=False), 
        Column("main_temp", Float(6), nullable=False),
        Column("main_feels_like", Float(6), nullable=False),
        Column("main_temp_min", Float(6), nullable=False),
        Column("main_temp_max", Float(6), nullable=False),
        Column("main_pressure", Integer, nullable=False),
        Column("main_humidity", Integer, nullable=False),
        Column("wind_speed", Float(6), nullable=False),
        )
    city_weater.create(engine, checkfirst=True)
    with Session() as session:
        session.add(CityWeather)
        # session.add(CityWeather.city)
        # session.add(CityWeather.weather)
        # session.add(CityWeather.main_temp)
        # session.add(CityWeather.main_feels_like)
        # session.add(CityWeather.main_temp_min)
        # session.add(CityWeather.main_temp_max)
        # session.add(CityWeather.main_pressure)
        # session.add(CityWeather.main_humidity)
        # session.add(CityWeather.wind_speed)
        session.commit()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
