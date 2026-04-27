"""
SINOBY MediaPlanBot
"""

import asyncio
import base64
import io
import json
import logging
import os
import random
import tempfile
from datetime import date
from calendar import monthrange
from urllib.parse import urlencode

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    CallbackQuery, BufferedInputFile,
)
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from PIL import Image as PILImage

load_dotenv()

BOT_TOKEN  = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://drouchucha.github.io/sinoby-mediaplan/")
SHEETS_URL = "https://script.google.com/macros/s/AKfycbwORRGftN-ehlSFpJlvNk74IxoDLlGQ8BW_weDDztzK7bQSE3z29QeBg5beTTP_tNrF8A/exec"
MANAGER_IDS = [267728315]

# Логотип встроен как base64
LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAIsAAABaCAIAAAAHGTIiAAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxopAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUGA2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJRIliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZAKbWPz9HbOBQAAATWElEQVR4nO1beVSU1fu/950FkJ2RRVBALE1MIahYRFxyCUMxXEiPVpZFHsujmcXJOu2cY3LUY4sJmnCyWCIxRHGplBIUkVVxCURUBgQGhwGGGWbe972/Px55G2djNPP3fs95P394hrs893nu597nPs+9r5gQggTwGNT/twIChoDAEN8hMMR3CAzxHQJDfIfAEN8hMMR3CAzxHQJDfIfAEN8hMMR3CAzxHQJDfIfAEN8hMMR3CAzxHQJDfIfAEN8hMMR3CAzxHQJDfIfAEN8hMMR3CAzxHQJDfIfAEN8hNltKBgF/UhSFMX6IWv0n+B81Cht9t82yLCFEJBIZtYNyy1YRgpg7EpEIoaEtB4HwmxuOEMKyLLqX6bOli3WjTMs5MAxjiw5GMBLIWWqjUYQQhmGgJUVRdzHEMAxI12q1V69ebW1t1ev17u7ugYGBI0aM4MajqH/rGx+IEFsA/IFRfX19jY2N7e3tDMMMHz48KCho+PDhaHBvPRx97gN3GIJ/McYXLlzYtWvX0aNHm5qauBXk4eERHh6+YsWKZcuWiUQijkiEEEIEIcQS/XVdejdz3kU0PlCaLMIOCBFLOwm6nzx5cteuXQghPz+/tLQ04KykpOS7775DCH3yySdjx461TiTUVlRUbN26FSGUkpISEhJi2IX7febMmfT09D/++OP69etcdy8vr6ioqJUrVyYkJCCD1QmzgTHu6elZt26dRqMRiUQURUGh9dkkhNjZ2aWlpbm5uXGL49ChQ/v27aMoavPmzSNHjrQiBxRWqVQbNmzo7+8nhHz88cd3VhnsrE2bNjk4OHAdxGKxnZ2doYiIiIhz584RQmiahqXHEoYQUqlenqtE+7tRrhKd7VvAEgbKTcEwDCGksbFRJpOBTF9fX04gcIYQKikpMRzFLKA2NzcXuhQWFhp2gYH6+vqSk5MN3Y5YLJZKpYZGxcXFNTU13WUUyxJC2tvbrfNhCTdv3gQher2eEPLFF19AeV1dHaeYKbj28fHxnKiTJ0+KoXpgYGDx4sVFRUUIIU9Pz6SkpGeffXbMmDFSqbSzs7OioiI3N/fUqVPl5eVTp07NycmJj49nGEYkwhhR/cw1Of3TMEqMEJZg0sYcUDNXnETjCWLx3bEi7FS1Wp2YmNjV1SUWixFC7u7uXAM7OzsolEgkNk6HVCqFLobzDouxs7Nz3rx55eXlCKFRo0YtXbr0mWeeCQgIEIlEbW1tZWVl2dnZtbW1xcXFMTExhYWF4eHhhlsQYyyTyVQqVURExOzZsxmGscUTSiQSNzc36A4lDg4OYrFYJBKBnpbAMIxYLN64cSOw8M88wMJZuHAhtFuyZMmNGzfMkpyZmQmzOWzYsMrKSkIITesJIRqm5aBK+qsKF6mkhSrqVxXqYxq57WW6RmCs8PDw6OhohFBwcDC3fvfu3QtqlJaW2riH9u/fD12Ki4uhkGVZmqa1Wm1UVBRUrV69WqFQmErQ6XRbtmwBP+Hl5dXc3MyyLMMwsIc6Ojo8PDwQQikpKVbUsAKwNy0tDSEkEonq6+uJhT0ELcF8Z2fnxMRE0PzUqVOIEAKuHyH05ptvch1ommYGodfrQe7Zs2eBJG9vb4VCwbIsw+oJIZc0m/K70S/dKL8bXehfR0zo4ZT48MMPEUIuLi6NjY1JSUkIoQkTJpAHyhCUv/vuu1CemppqahRN03q9HpgoLCwEkmbMmAEMgbEcQ2vXrtXr9RqNRm8b7pUhULi0tBSOmKysrIKCAtiFp06dQl1dXX5+fhjj6dOnQ2tLjhLGq6mp+fHHHzMzM+VyOSGEZRlCWEJIh+54o3Z7u66YEAIlpn1/+uknGPiXX34hhMyePfuBM6TT6QghjY2N9vb2CKHly5dDoVmjWJYdGBgghGzfvh2EHDhwgBPCMbRu3TrOhHuCLQzBny0tLSNHjkQIvfzyy2RwzwBD4uzsbLlcLpFItm3bBlpa8rZisZhl2ZCQkJCQEK4QY2hMPCUzPdFM+G0UxYGHPXfu3GuvvQaLOjExkWVZ6375/gC50ffff6/Vat3d3bds2QIBlVmjMMYSiYSm6bVr12ZlZdXU1OzcuTMhIcGoMXAJsDQuxvg+8l8gCYKAlpaW2NjYXbt2GUWw1IEDBzDGMTExEKpaSd8QQhRFgZeH9WuoIUtohuhZQhvRAzLb29uXLFmiVqtXrFiRkpKi0+msn7r3tFQNO4pEIkLI8ePHMcbz58/38fEhVnMdmFaM8auvvkoIOXPmTHt7u9EkSCQSiqKkUillGRhjcI9WjDIFhPjJycmnT58ODAzMzc0Vi8VGia34woULhBBwcbYkkqCQmXJsZkPADNI0nZSUdO3atcjIyIyMDFuCIjs7O4yx9U1mGsJBoUKhuHr1KmcUGeo/u4MyMTExkItcuXLF29ub0x8hpFAoGhoa7s4C7+pub28vk8nAr6LBdMr6oAghmqbFYvHmzZuzsrIcHR3z8vJ8fHwGBgaMMhzx7du3EUL+/v73fUkFvK5evbq6unrChAl79uzhVAT/lpycXFJS4ufnl5eXZ2dnZ8VXAEQi0apVq1xcXKybCrVdXV2ws7ny27dv9/T0cEYNaRc08Pb2dnZ2VqlUHR0dXBXsiaysrMzMTCvdHRwcfHx8Jk2a9MILLyQlJWGMhyQJ6CksLHz//fcRQunp6U899RRN06aLQPygbg8rKysrKio0Go2REtu3b09PT7e3t8/NzR01ahSsROveAGNcW1tr+9CWPPOQu8dse9MJEYvFYrHY0qSzLNvf39/U1NTU1HTgwIGsrKzs7GxnZ2crA8HCra+vf+mll1iW3bRp07Jly2C6aJo2Hl0mk7W2tjY3N9+rPUZwdHQUiUSOjo7wJ4x39OjRjRs3IoS++eabyZMnQ+GQouB249FHH7XuD+GEq6ys/Prrrw3LZTKZq6trV1cXl9hZHw6m/tatW729vQghLy8vrgq0Xbly5UcffWRJeYZhurq6SktLd+zY8ffffxcXFycnJ+fk5FhahaC2UqlctGhRd3f3woULP//8c7O75w7mzJmDMZ46dappIGgWkB5xyQTXKzY2FiEUERFBBqPMK1euwNXkO++8Q+6OViHQmDt3LrIQbcMFiS04duwYdIFoG0aJiIjAGK9YsYIMFbJzXXbs2IEQcnNz6+jogHIu2gb9h4RCoQgJCYGJhsAaQnmjaFun07EsGxcXhxAKDQ3t7e3lcmROmYyMDDQYbVOJiYmEkNLS0qqqKoqirPsfOHJg11txjxRF9fT0LFq0SKFQxMfHb9myxdoaMYfu7m6apgcGBmjLgFqVSmXYEfSfM2cOIaSwsLC1tdXolDICIQTs2rNnD8Y4Ojra09PTyNXAPQXMrCVotVqZTPbBBx+AAhUVFWgw9DeaQIlEsmHDhuLiYi8vr/z8fCcnJ2TOtf4zmUlJSf7+/gzDrF+/3tBIU+j1eoqizp49m5GR8e2337a0tCATX08GA8IXX3zx/PnzwcHBP/zwA7H2sGQecItlC4yIB6+4cuXKYcOGwSUxxthSKgNrViwWb9u2rba2lhCyZs0aU6MwxlbibIBEImFZNjAwENpDqGIEyDHS09O3bdsmkUj27ds3ZswYmqatR7aUq6vrp59+Sgj5888/33jjDZFIJBKJ4GYBDIM7EiC/rKxs5syZr7/+empqqqOjo9k1QlFUSkrKr7/+6uHhkZ+f7+bm9tBegxBC4AYCAwM3bNiAEMrJyfnss88gyTA1CmMslUr3798PAVVcXNzcuXPNptJDujiY6M7OTmhv+EQAYBjG09OzoqLirbfeQght3bp11qxZNh3M4KaXL18Ofz7//PNwFW8ElmUzMjJcXV0RQi4uLpBFwQlkeA7Nnj07OzsbZurgwYPEwmXJkOfQv7851el006ZNg6pVq1bdunXLVIJGo0lNTYWMys/PTy6Xm705ffvtt4kNhzRN09OnT4e1CG80Wq2WDJ5Djo6OR44cGT16NEJo9erVlmbG9BwSg5veu3evTqfLy8srKCgoKSlZvHjxnDlzHnnkEXh9OHv2bF5eHlzju7m55efnT5gwwSiDg/1UW1ubnJyMENq8eXN8fLyNwduDBeeUCgoKFixYUFJSsnv37sOHDyclJc2cOZN7fSgtLc3Jyamvr0cIBQYGHjx40NfXF7Y7udvLccGRWVtYlu3u7q6qqvryyy9LSkoQQrNmzQoLCzO6oMEYv/LKK62trdOnT//qq68s5b9mQAYvnQghqampsEs4GOk0bdo02D2GqxsW15QpUyCIQIPXf1auGqF7fHw8RVETJ07kSjIzM2Fyy8rKiG17qKCgALocOXLEsAtopdVq169fb5ilY4yNpiYxMRFugY1e8Do6Otzd3SmKcnd3DwoKGj16dJA5BAQEGE5aeHg4txe5m1OKokCH0aNHd3R0QK1Zo6DL7t27KYoSiUSlpaWI0wnUamxsfO+99yZNmsTdYSCERowYkZCQkJ+fbzg1RgyFh4dD48mTJ0OUxUWQliZ3xowZCKGgoCCuBHY3Quivv/6ykaGff/4ZuhQVFRl14RSoqalZs2bNuHHjuIdBjLG/v//SpUuPHTtmaIVhx/b2dtsdgLOz89NPP52Wlgav1yABpjs1NRXaODk5VVVVWbcLuuzcuRO6lJSUmP+ShGXZ5ubmtrY2vV7v5uYWEBDAvYSaHvuEEIxxZWVld3c3QigsLMzd3Z3YcGFTW1urUCicnJwgi8IYt7W1Xbx4ESH05JNPurq62iKks7Ozrq4OIRQaGiqTyYy6EIMvSXQ63bVr12AJe3h4BAYGQubPsqzZyyGdTnf69GkIKKynFo6Ojj4+PvB8gAzu5eDHjRs3GhoaCCG+vr7BwcHW4ybo0traeunSJYxxWFiYma+xzAYz7FAfLpkOY0vLhwNLykNecU+JmnVA2mfF9vsIa40ZAnCbDg2+fAw54+w9fhVm2OW//l6Oa3mvRtn+mgDhiXUNrbSx1IXivpf7r1c933bV/4S9IOSf71rMtjD6YVpl+0iW5HDr2kZRZhWwoqoVff7NiNZxr/SYFQ6vGHcYglci0xa3b9/W6XSm48GToukZplKp9Hq9WTlwIJtWWfI2lpRWKpVwehuVq9VqlUply9SAPmbl9/b29vf3GzXu7+/v7u42lWxlbXV1dRmV6PX6vr6+3t5eo4sYvV5vVjgIwRiLb968efjw4ZEjR2KMZ82aBVeisMqqqqpu3bql1+ujoqI8PT1BJ4qi6uvrYaTIyEiwgR38YrSnp4emafiYCOQghE6cONHf39/e3h4REfH4449zHrauru7y5cvz5s3LyMhYu3Ytt7RZli0tLZ0yZUpZWVlYWBjE/VB7+vTp9vZ2QkhsbCwk/ICbN29CRBcUFDR+/Hhk2SsQQn7//feBgYG2trbY2Nhx48Zx+ly8eLG6ujo0NDQ4OJjrIpfLa2pqEEIBAQETJ07kAj+5XN7b2/vYY4+VlZVFR0dzqa5Wq/3tt99YlvX29o6MjOQoVCqVBw8edHJymjdvHncnhDE+dOiQWCx2c3OLiYnhhOh0uuPHj0PIRimVyoCAgOeee04ikbS0tHDTSgg5ceKEp6enXq+Xy+VQDlXXr18vKiqKiooyWv6EkBkzZjg7O4MZMKdKpVKpVMbHx4eEhBitLKlU2tHRkZ2d7eLiwn1LDr3q6+uPHj1aWVmJDB7WtFrt9evXFyxY8MQTT5w/fx6GgLHKysoQQq6uro2NjZwJpvRgjBUKhVqtjo+PDw4ONvIcarU6MjISbqFg2WGMz5w5Q9O0h4dHQ0ODYWOGYU6cOFFUVCSXy9Hg2Y4xbmxs9PT0TEhIgAQRpogQ4uXlFRoaGhkZOWzYMMMFpFarHRwc2trayOAtO8a4qanJyclp/vz5NE1T9vb2DQ0N586dU6lUnp6eoBz8O378eKVS6e7uPmbMGGJwPy2TySIiIsrLyw1Do/7+ftiVnDcDOc7OznAjXl1dbfQCzzBMdHR0XFwcXLdwywpShylTpgQGBhqeYVKp1NnZuays7Pz58/7+/lAFtWPHjtXpdDqdbtKkSZY2EEh2dXVlGKaioqKurs5IH5FIBN9hGbYfO3YswzAajSY0NNRQMiFk4sSJkydPhqSKY8LX17e1tbW8vLy6uhrdfYzp9XqdTmeqmKHfgh8+Pj4KhaK8vFyj0aDLly8fO3asrq5OpVIRgzwcUF9f39zcbPjERAiBtFmhUBjm4f39/fBdZ29vL7kbAwMDtbW1crkc7Oeg0Wjgjaunp8eoS19fHyFErVabfl0GogxVhR/Nzc2XLl0yGsII0FKj0dTW1kI+blYfo/Y3bty4ePGiUZVOp4MStVpt1F6pVNbU1IBRhvOm0WgM1YMqSNING8O/KpWqpqZGrVbfecmw/q7+n4LcV2B6f73uA/c60ANRzFDIHZdtKde1dCNiVhVi4CFtl/OgRMHCtDEltK7PPUk2q7ztmkBjU2X+KefSXVvECXj4MB/2COAPePpfAwVwEBjiOwSG+A6BIb5DYIjvEBjiOwSG+A6BIb5DYIjvEBjiOwSG+A6BIb5DYIjvEBjiOwSG+A6BIb5DYIjvEBjiOwSG+A6BIb5DYIjvEBjiOwSG+A6BIb5DYIjvEBjiO/4PKqCySMPKEZoAAAAASUVORK5CYII="

doc_storage = {}
doc_counter = 0

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()

CITY_REGION = {
    'москва': 'Москва и Московская область',
    'воронеж': 'Воронеж, Воронежская область',
    'ярославль': 'Ярославль, Ярославская область',
    'тула': 'Тула, Тульская область',
    'рязань': 'Рязань, Рязанская область',
    'липецк': 'Липецк, Липецкая область',
    'санкт-петербург': 'Санкт-Петербург и Ленинградская область',
    'калининград': 'Калининград, Калининградская область',
    'мурманск': 'Мурманск, Мурманская область',
    'архангельск': 'Архангельск, Архангельская область',
    'вологда': 'Вологда, Вологодская область',
    'петрозаводск': 'Петрозаводск, Республика Карелия',
    'ростов-на-дону': 'Ростов-на-Дону, Ростовская область',
    'краснодар': 'Краснодар, Краснодарский край',
    'волгоград': 'Волгоград, Волгоградская область',
    'сочи': 'Сочи, Краснодарский край',
    'астрахань': 'Астрахань, Астраханская область',
    'симферополь': 'Симферополь, Республика Крым',
    'ставрополь': 'Ставрополь, Ставропольский край',
    'махачкала': 'Махачкала, Республика Дагестан',
    'владикавказ': 'Владикавказ, Республика Северная Осетия',
    'грозный': 'Грозный, Чеченская Республика',
    'нальчик': 'Нальчик, Кабардино-Балкарская Республика',
    'пятигорск': 'Пятигорск, Ставропольский край',
    'казань': 'Казань, Республика Татарстан',
    'нижний новгород': 'Нижний Новгород, Нижегородская область',
    'уфа': 'Уфа, Республика Башкортостан',
    'самара': 'Самара, Самарская область',
    'пермь': 'Пермь, Пермский край',
    'саратов': 'Саратов, Саратовская область',
    'екатеринбург': 'Екатеринбург, Свердловская область',
    'челябинск': 'Челябинск, Челябинская область',
    'тюмень': 'Тюмень, Тюменская область',
    'сургут': 'Сургут, Ханты-Мансийский АО',
    'магнитогорск': 'Магнитогорск, Челябинская область',
    'нижний тагил': 'Нижний Тагил, Свердловская область',
    'новосибирск': 'Новосибирск, Новосибирская область',
    'красноярск': 'Красноярск, Красноярский край',
    'иркутск': 'Иркутск, Иркутская область',
    'кемерово': 'Кемерово, Кемеровская область',
    'барнаул': 'Барнаул, Алтайский край',
    'томск': 'Томск, Томская область',
    'владивосток': 'Владивосток, Приморский край',
    'хабаровск': 'Хабаровск, Хабаровский край',
    'благовещенск': 'Благовещенск, Амурская область',
    'якутск': 'Якутск, Республика Саха (Якутия)',
    'улан-удэ': 'Улан-Удэ, Республика Бурятия',
    'магадан': 'Магадан, Магаданская область',
}

def next_month_range():
    today = date.today()
    year  = today.year + (1 if today.month == 12 else 0)
    month = 1 if today.month == 12 else today.month + 1
    from calendar import monthrange as mr
    days  = mr(year, month)[1]
    start = date(year, month, 1)
    end   = date(year, month, days)
    return f"{start.strftime('%d.%m.%Y')}-{end.strftime('%d.%m.%Y')}", days

def days_word(n):
    if n == 31: return '31 день'
    if n == 30: return '30 дней'
    return '28 дней'

def parse_budget(s):
    import re
    nums = re.findall(r'\d+', str(s).replace(' ','').replace('\u202f','').replace('\xa0',''))
    return max((int(n) for n in nums), default=500000)

def create_excel_bytes(data):
    city     = data.get('city', '')
    brand    = data.get('brand', '')
    budget   = parse_budget(data.get('budget', '500000'))
    calls    = int(data.get('calls') or 50)
    channels = data.get('channels', ['Яндекс Директ'])
    region   = CITY_REGION.get(city.lower(), city)
    date_range, n_days = next_month_range()
    period   = days_word(n_days)

    GREEN  = PatternFill('solid', fgColor='92D050')
    LIGHT  = PatternFill('solid', fgColor='E2EFDA')
    thin   = Side(style='thin')
    def brd(): return Border(top=thin, bottom=thin, left=thin, right=thin)
    center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    left_a = Alignment(horizontal='left',   vertical='center', wrap_text=True)

    wb = Workbook()
    ws = wb.active
    ws.title = 'Контекст'

    ws.column_dimensions['A'].width = 17.9
    ws.column_dimensions['B'].width = 16.4
    ws.row_dimensions[1].height = 72

    # Логотип
    ws.merge_cells('A1:B1')
    logo_bytes = base64.b64decode(LOGO_B64)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tmp.write(logo_bytes)
    tmp.close()
    xl_img = XLImage(tmp.name)
    xl_img.width  = 240
    xl_img.height = 68
    xl_img.anchor = 'A1'
    ws.add_image(xl_img)

    # Мета
    for row, label, value in [
        (2, 'Посадочная страница', 'ваш ленд'),
        (3, 'Срок кампании',       date_range),
        (4, 'Регион показа',       region),
    ]:
        ws[f'A{row}'].value     = label
        ws[f'A{row}'].font      = Font(name='Arial', size=8, bold=True)
        ws[f'A{row}'].alignment = left_a
        ws[f'B{row}'].value     = value
        ws[f'B{row}'].font      = Font(name='Arial', size=8)
        ws.merge_cells(f'B{row}:M{row}')

    # Заголовки
    headers = [
        ('A','B','Поисковая система / Канал'),
        ('C','C','Рекламный носитель'),
        ('D','D','Время размещения'),
        ('E','E','Охват (прогноз)'),
        ('F','F','Показы (прогноз)'),
        ('G','G','Средний CTR,%'),
        ('H','H','Переходы'),
        ('I','J','Средняя цена за клик'),
        ('K','K','РЛ'),
        ('L','L','Стоимость РЛ'),
        ('M','M','Бюджет с НДС и АК'),
    ]
    for sc, ec, title in headers:
        if sc != ec: ws.merge_cells(f'{sc}5:{ec}5')
        c = ws[f'{sc}5']
        c.value = title
        c.font  = Font(name='Arial', size=8, bold=True)
        c.fill  = GREEN
        c.alignment = center
        c.border = brd()
    ws.row_dimensions[5].height = 32

    # Данные
    dr = 6
    for ch in channels:
        is_ya = 'яндекс' in ch.lower()
        is_vk = 'вконтакте' in ch.lower() or 'vk' in ch.lower()
        ch_budget   = min(budget, 700000) if is_vk else budget
        cpc         = round(random.uniform(65, 80))
        clicks      = round(ch_budget / cpc)
        ctr         = round(random.uniform(0.0075, 0.011), 5)
        impressions = round(clicks / ctr)
        sys_name  = 'Яндекс.Директ' if is_ya else ('ВКонтакте' if is_vk else ch)
        placement = 'сети/поиск'     if is_ya else ('лента/сторис' if is_vk else '')

        ws.merge_cells(f'A{dr}:B{dr}')
        ws[f'A{dr}'].value = sys_name
        ws[f'A{dr}'].font  = Font(name='Arial', size=10, bold=True)

        for col, val in [('C', placement), ('D', period)]:
            ws[f'{col}{dr}'].value     = val
            ws[f'{col}{dr}'].font      = Font(name='Arial', size=10)
            ws[f'{col}{dr}'].alignment = center

        for col, val, fmt in [
            ('E', impressions, '#,##0'),
            ('F', impressions, '#,##0'),
            ('H', clicks,      '#,##0'),
            ('K', calls,       '#,##0'),
            ('M', ch_budget,   '#,##0 ₽'),
        ]:
            ws[f'{col}{dr}'].value         = val
            ws[f'{col}{dr}'].font          = Font(name='Arial', size=10)
            ws[f'{col}{dr}'].alignment     = center
            ws[f'{col}{dr}'].number_format = fmt

        ws[f'G{dr}'] = f'=H{dr}/F{dr}'
        ws[f'G{dr}'].number_format = '0.00%'; ws[f'G{dr}'].alignment = center; ws[f'G{dr}'].font = Font(name='Arial', size=10)
        ws.merge_cells(f'I{dr}:J{dr}')
        ws[f'I{dr}'] = f'=M{dr}/H{dr}'
        ws[f'I{dr}'].number_format = '#,##0 ₽'; ws[f'I{dr}'].alignment = center; ws[f'I{dr}'].font = Font(name='Arial', size=10)
        ws[f'L{dr}'] = f'=M{dr}/K{dr}'
        ws[f'L{dr}'].number_format = '#,##0 ₽'; ws[f'L{dr}'].alignment = center; ws[f'L{dr}'].font = Font(name='Arial', size=10)
        dr += 1

    # Итог
    first, last = 6, dr - 1
    ir = dr
    ws.merge_cells(f'A{ir}:D{ir}')
    ws[f'A{ir}'].value = 'Итог:'; ws[f'A{ir}'].font = Font(name='Arial', size=10, bold=True); ws[f'A{ir}'].fill = LIGHT

    for col, fmt in [('E','#,##0'),('F','#,##0'),('H','#,##0'),('K','#,##0'),('M','#,##0 ₽')]:
        ws[f'{col}{ir}'] = f'=SUM({col}{first}:{col}{last})'
        ws[f'{col}{ir}'].font = Font(name='Arial', size=10, bold=True)
        ws[f'{col}{ir}'].fill = LIGHT; ws[f'{col}{ir}'].alignment = center
        ws[f'{col}{ir}'].number_format = fmt

    ws[f'G{ir}'] = f'=H{ir}/F{ir}'
    ws[f'G{ir}'].font=Font(name='Arial',size=10,bold=True); ws[f'G{ir}'].fill=LIGHT
    ws[f'G{ir}'].number_format='0.00%'; ws[f'G{ir}'].alignment=center

    ws.merge_cells(f'I{ir}:J{ir}')
    ws[f'I{ir}'] = f'=M{ir}/H{ir}'
    ws[f'I{ir}'].font=Font(name='Arial',size=10,bold=True); ws[f'I{ir}'].fill=LIGHT
    ws[f'I{ir}'].number_format='#,##0 ₽'; ws[f'I{ir}'].alignment=center

    ws[f'L{ir}'] = f'=M{ir}/K{ir}'
    ws[f'L{ir}'].font=Font(name='Arial',size=10,bold=True); ws[f'L{ir}'].fill=LIGHT
    ws[f'L{ir}'].number_format='#,##0 ₽'; ws[f'L{ir}'].alignment=center

    for col, w in [('C',14),('D',12),('E',13),('F',13),('G',10),
                   ('H',10),('I',11),('J',11),('K',8),('L',14),('M',18)]:
        ws.column_dimensions[col].width = w

    out = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    wb.save(out.name)
    with open(out.name, 'rb') as f:
        result = f.read()
    os.unlink(out.name)
    os.unlink(tmp.name)
    return result


@dp.message(CommandStart())
async def cmd_start(msg: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📋 Создать медиаплан", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
    )
    await msg.answer(
        "👋 Добро пожаловать в <b>SINOBY MediaPlanBot</b>\n\nНажмите кнопку ниже чтобы создать медиаплан.",
        parse_mode="HTML", reply_markup=kb,
    )


@dp.message(F.web_app_data)
async def on_webapp_data(msg: Message):
    global doc_counter
    raw  = msg.web_app_data.data
    user = msg.from_user
    log.info(f"Получены данные от {user.id} (@{user.username}): {raw}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        await msg.answer("⚠️ Ошибка при получении данных.")
        return

    from datetime import datetime
    category    = data.get("category", "—")
    region      = data.get("region",   "—")
    district    = data.get("district", "—")
    city        = data.get("city",     "—")
    spec        = data.get("spec",     "—")
    goal        = data.get("goal",     "—")
    channels    = data.get("channels", [])
    budget      = data.get("budget",   "—")
    calls       = data.get("forecast_calls")
    price       = data.get("forecast_price")
    ts          = data.get("ts", "")

    spec_label  = "Бренд" if category == "Авто" else "Категория" if category == "Недвижимость" else "Направление"
    channel_str = ", ".join(channels) if channels else "—"

    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        time_str = dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    forecast_block = ""
    if calls and price:
        forecast_block = f"\n📊 <b>Прогноз</b>\n├ Звонков в месяц: <b>~{calls}</b>\n└ Цена звонка: <b>~{price}</b>\n"

    name     = user.full_name or "—"
    username = f"@{user.username}" if user.username else f"ID:{user.id}"

    text = (
        f"📋 <b>Новый запрос на медиаплан</b>\n{'─'*28}\n"
        f"🏷 Сфера: <b>{category}</b>\n"
        f"📍 Регион: <b>{region} ({district})</b>\n"
        f"🏙 Город: <b>{city}</b>\n"
        f"🔖 {spec_label}: <b>{spec}</b>\n"
        f"🎯 Цель: <b>{goal}</b>\n"
        f"📡 Канал: <b>{channel_str}</b>\n"
        f"💰 Бюджет: <b>{budget}</b>\n"
        f"{forecast_block}"
        f"{'─'*28}\n"
        f"👤 {name} · {username}\n🕐 {time_str}"
    )

    await msg.answer(
        f"✅ <b>Запрос принят!</b>\n\nНаш менеджер свяжется с вами в ближайшее время.\n\n"
        f"<b>Ваши параметры:</b>\n• Сфера: {category}\n• Город: {city}\n• {spec_label}: {spec}\n• Бюджет: {budget}",
        parse_mode="HTML", reply_markup=ReplyKeyboardRemove(),
    )

    doc_counter += 1
    doc_key = str(doc_counter)
    doc_storage[doc_key] = {
        "city": city, "brand": spec, "budget": budget,
        "calls": calls or "—", "price": price or "—",
        "channels": channels, "goal": goal, "category": category,
    }

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📄 Сформировать медиаплан", callback_data=f"doc:{doc_key}")
    ]])

    for manager_id in MANAGER_IDS:
        try:
            await bot.send_message(chat_id=manager_id, text=text, parse_mode="HTML", reply_markup=kb)
            log.info(f"Уведомление отправлено менеджеру {manager_id}")
        except Exception as e:
            log.error(f"Не удалось отправить менеджеру {manager_id}: {e}")


@dp.callback_query(F.data.startswith("doc:"))
async def on_create_doc(cb: CallbackQuery):
    await cb.answer("Генерирую файл...")
    await cb.message.edit_reply_markup(reply_markup=None)

    doc_key = cb.data[4:]
    data    = doc_storage.get(doc_key)

    if not data:
        await cb.message.answer("⚠️ Данные устарели. Попросите клиента пройти квиз заново.")
        return

    try:
        xlsx_bytes = create_excel_bytes(data)
        city  = data.get('city', '')
        brand = data.get('brand', '')
        today = date.today()
        year  = today.year + (1 if today.month == 12 else 0)
        month = 1 if today.month == 12 else today.month + 1
        fname = f"МП_{brand}_{city}_{month}.{year}.xlsx"

        await cb.message.answer_document(
            BufferedInputFile(xlsx_bytes, filename=fname),
            caption=f"📄 <b>Медиаплан готов</b>\n{brand} · {city}",
            parse_mode="HTML",
        )
    except Exception as e:
        log.error(f"Ошибка создания Excel: {e}")
        await cb.message.answer(f"⚠️ Ошибка: {e}")


@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("ℹ️ <b>SINOBY MediaPlanBot</b>\n\n/start — квиз медиаплана\n/help — справка", parse_mode="HTML")


async def main():
    log.info("Бот запускается...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
