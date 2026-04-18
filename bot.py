"""
SINOBY MediaPlanBot — Telegram Bot
====================================
pip install aiogram==3.7.0 aiohttp python-dotenv
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from urllib.parse import urlencode

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppData, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    CallbackQuery,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN  = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://drouchucha.github.io/sinoby-mediaplan/")
SHEETS_URL = "https://script.google.com/macros/s/AKfycbypMC4LDH9ItJDLGCru-obQj2qmWrdqTnFYtZUlQCimSSrUACYxkZuSG87msvxfwPshNw/exec"

MANAGER_IDS = [267728315]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()


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
    raw  = msg.web_app_data.data
    user = msg.from_user
    log.info(f"Получены данные от {user.id} (@{user.username}): {raw}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        await msg.answer("⚠️ Ошибка при получении данных.")
        return

    category  = data.get("category", "—")
    region    = data.get("region",   "—")
    district  = data.get("district", "—")
    city      = data.get("city",     "—")
    spec      = data.get("spec",     "—")
    goal      = data.get("goal",     "—")
    channels  = data.get("channels", [])
    budget    = data.get("budget",   "—")
    calls     = data.get("forecast_calls")
    price     = data.get("forecast_price")
    ts        = data.get("ts", "")

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

    doc_data = json.dumps({
        "city": city, "brand": spec, "budget": budget,
        "calls": calls or "—", "price": price or "—",
        "channels": ",".join(channels), "goal": goal,
    }, ensure_ascii=False)

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📄 Сформировать медиаплан", callback_data=f"doc:{doc_data[:200]}")
    ]])

    for manager_id in MANAGER_IDS:
        try:
            await bot.send_message(chat_id=manager_id, text=text, parse_mode="HTML", reply_markup=kb)
        except Exception as e:
            log.error(f"Не удалось отправить менеджеру {manager_id}: {e}")


@dp.callback_query(F.data.startswith("doc:"))
async def on_create_doc(cb: CallbackQuery):
    await cb.answer("Создаю документ...")
    await cb.message.edit_reply_markup(reply_markup=None)

    try:
        data = json.loads(cb.data[4:])
    except Exception:
        await cb.message.answer("⚠️ Ошибка данных.")
        return

    params = {
        "action": "create_doc",
        "city":     data.get("city",     ""),
        "brand":    data.get("brand",    ""),
        "budget":   data.get("budget",   ""),
        "calls":    data.get("calls",    "—"),
        "price":    data.get("price",    "—"),
        "channels": data.get("channels", "Яндекс Директ"),
        "goal":     data.get("goal",     ""),
    }

    url = SHEETS_URL + "?" + urlencode(params)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                result = await resp.json(content_type=None)

        if result.get("ok"):
            await cb.message.answer(
                f"📄 <b>Медиаплан сформирован!</b>\n\n"
                f"<b>{result.get('title','Медиаплан')}</b>\n\n"
                f"🔗 <a href='{result.get('url','')}'>Открыть документ</a>",
                parse_mode="HTML", disable_web_page_preview=True,
            )
        else:
            await cb.message.answer(f"⚠️ Ошибка: {result.get('error','Неизвестная ошибка')}")

    except Exception as e:
        log.error(f"Ошибка создания документа: {e}")
        await cb.message.answer(f"⚠️ Ошибка: {e}")


@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("ℹ️ <b>SINOBY MediaPlanBot</b>\n\n/start — квиз медиаплана\n/help — справка", parse_mode="HTML")


async def main():
    log.info("Бот запускается...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
