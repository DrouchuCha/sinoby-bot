"""
SINOBY MediaPlanBot — Telegram Bot
"""

import asyncio
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
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

load_dotenv()

BOT_TOKEN  = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://drouchucha.github.io/sinoby-mediaplan/")
SHEETS_URL = "https://script.google.com/macros/s/AKfycbwORRGftN-ehlSFpJlvNk74IxoDLlGQ8BW_weDDztzK7bQSE3z29QeBg5beTTP_tNrF8A/exec"

MANAGER_IDS = [267728315]

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
    days  = monthrange(year, month)[1]
    start = date(year, month, 1)
    end   = date(year, month, days)
    return f"{start.strftime('%d.%m.%Y')}-{end.strftime('%d.%m.%Y')}", days

def days_word(n):
    if n == 31: return '31 день'
    if n == 30: return '30 дней'
    return '28 дней'

def parse_budget(budget_str):
    import re
    nums = re.findall(r'\d+', budget_str.replace(' ', '').replace('\u202f', ''))
    if not nums: return 500000
    return max(int(n) for n in nums)

def create_excel_bytes(data):
    city     = data.get('city', '')
    brand    = data.get('brand', '')
    budget   = parse_budget(data.get('budget', '500000'))
    calls    = int(data.get('calls') or 50)
    channels = data.get('channels', ['Яндекс Директ'])

    region     = CITY_REGION.get(city.lower(), city)
    date_range, n_days = next_month_range()
    period     = days_word(n_days)

    wb = Workbook()
    ws = wb.active
    ws.title = 'Контекст'

    GREEN = PatternFill('solid', fgColor='92D050')
    LIGHT = PatternFill('solid', fgColor='E2EFDA')
    BLACK = PatternFill('solid', fgColor='0A0A0A')
    thin  = Side(style='thin')
    def brd(): return Border(top=thin, bottom=thin, left=thin, right=thin)
    center = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Шапка
    ws.merge_cells('A1:M1')
    ws['A1'].value     = f'SINOBY | Медиаплан — {brand} | {city}'
    ws['A1'].font      = Font(name='Arial', size=12, bold=True, color='FFFFFF')
    ws['A1'].fill      = BLACK
    ws['A1'].alignment = center
    ws.row_dimensions[1].height = 28

    meta = [(2,'Посадочная страница','ваш ленд'),
            (3,'Срок кампании', date_range),
            (4,'Регион показа',  region)]
    for row, label, value in meta:
        ws[f'A{row}'].value = label
        ws[f'A{row}'].font  = Font(name='Arial', size=8, bold=True)
        ws[f'B{row}'].value = value
        ws[f'B{row}'].font  = Font(name='Arial', size=8)
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
        if sc != ec:
            ws.merge_cells(f'{sc}5:{ec}5')
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
        ws[f'A{dr}'].value = sys_name;    ws[f'A{dr}'].font = Font(name='Arial', size=10, bold=True)
        ws[f'C{dr}'].value = placement;   ws[f'C{dr}'].font = Font(name='Arial', size=10)
        ws[f'D{dr}'].value = period;      ws[f'D{dr}'].font = Font(name='Arial', size=10)
        ws[f'E{dr}'].value = impressions; ws[f'E{dr}'].font = Font(name='Arial', size=10)
        ws[f'F{dr}'].value = impressions; ws[f'F{dr}'].font = Font(name='Arial', size=10)
        ws[f'G{dr}'] = f'=H{dr}/F{dr}';  ws[f'G{dr}'].font = Font(name='Arial', size=10)
        ws[f'G{dr}'].number_format = '0.00%'
        ws[f'H{dr}'].value = clicks;      ws[f'H{dr}'].font = Font(name='Arial', size=10)
        ws.merge_cells(f'I{dr}:J{dr}')
        ws[f'I{dr}'] = f'=M{dr}/H{dr}';  ws[f'I{dr}'].font = Font(name='Arial', size=10)
        ws[f'I{dr}'].number_format = '#,##0 ₽'
        ws[f'K{dr}'].value = calls;       ws[f'K{dr}'].font = Font(name='Arial', size=10)
        ws[f'L{dr}'] = f'=M{dr}/K{dr}';  ws[f'L{dr}'].font = Font(name='Arial', size=10)
        ws[f'L{dr}'].number_format = '#,##0 ₽'
        ws[f'M{dr}'].value = ch_budget;   ws[f'M{dr}'].font = Font(name='Arial', size=10)
        ws[f'M{dr}'].number_format = '#,##0 ₽'
        dr += 1

    # Итог
    first, last = 6, dr - 1
    ws.merge_cells(f'A{dr}:D{dr}')
    ws[f'A{dr}'].value = 'Итог:'
    ws[f'A{dr}'].font  = Font(name='Arial', size=10, bold=True)
    ws[f'A{dr}'].fill  = LIGHT

    for col in ['E','F','H','K','M']:
        ws[f'{col}{dr}'] = f'=SUM({col}{first}:{col}{last})'
        ws[f'{col}{dr}'].font = Font(name='Arial', size=10, bold=True)
        ws[f'{col}{dr}'].fill = LIGHT
        if col == 'M': ws[f'{col}{dr}'].number_format = '#,##0 ₽'

    ws[f'G{dr}'] = f'=H{dr}/F{dr}'
    ws[f'G{dr}'].font = Font(name='Arial', size=10, bold=True)
    ws[f'G{dr}'].fill = LIGHT
    ws[f'G{dr}'].number_format = '0.00%'

    ws.merge_cells(f'I{dr}:J{dr}')
    ws[f'I{dr}'] = f'=M{dr}/H{dr}'
    ws[f'I{dr}'].font = Font(name='Arial', size=10, bold=True)
    ws[f'I{dr}'].fill = LIGHT
    ws[f'I{dr}'].number_format = '#,##0 ₽'

    ws[f'L{dr}'] = f'=M{dr}/K{dr}'
    ws[f'L{dr}'].font = Font(name='Arial', size=10, bold=True)
    ws[f'L{dr}'].fill = LIGHT
    ws[f'L{dr}'].number_format = '#,##0 ₽'

    # Ширина колонок
    for col, w in [('A',18),('B',18),('C',14),('D',12),('E',13),('F',13),
                   ('G',10),('H',10),('I',11),('J',11),('K',8),('L',14),('M',18)]:
        ws.column_dimensions[col].width = w

    # Сохраняем в байты
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        tmp_path = f.name
    wb.save(tmp_path)
    with open(tmp_path, 'rb') as f:
        result = f.read()
    os.unlink(tmp_path)
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
        "city":     city,
        "brand":    spec,
        "budget":   budget,
        "calls":    calls or "—",
        "price":    price or "—",
        "channels": channels,
        "goal":     goal,
        "category": category,
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
        city   = data.get('city', '')
        brand  = data.get('brand', '')
        today  = date.today()
        year   = today.year + (1 if today.month == 12 else 0)
        month  = 1 if today.month == 12 else today.month + 1
        fname  = f"МП_{brand}_{city}_{month}.{year}.xlsx"

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
