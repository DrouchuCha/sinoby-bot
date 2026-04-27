"""
Отправка уведомлений и файлов медиаплана в VK Teams.

API: облачный VK Teams (myteam.mail.ru).

Требует переменных окружения:
    VKTEAMS_TOKEN          — токен бота из @metabot в VK Teams
    VKTEAMS_MANAGER_ID     — ID/email получателя (например, m.egorov@sinoby.ru)
    VKTEAMS_API_BASE       — необязательно (по умолчанию https://myteam.mail.ru/bot/v1)
"""

import logging
import os
from datetime import datetime
from typing import Optional

import aiohttp

log = logging.getLogger(__name__)

VKTEAMS_API_BASE = os.getenv("VKTEAMS_API_BASE", "https://myteam.mail.ru/bot/v1")
VKTEAMS_TOKEN = os.getenv("VKTEAMS_TOKEN", "")
VKTEAMS_MANAGER_ID = os.getenv("VKTEAMS_MANAGER_ID", "")


def _format_quiz_message(d: dict, user_name: str = "", user_handle: str = "") -> str:
    """Формирует читаемое сообщение для менеджера из данных квиза."""
    category = d.get("category", "—")
    region = d.get("region", "—")
    district = d.get("district", "—")
    city = d.get("city", "—")
    spec = d.get("spec", "—")
    goal = d.get("goal", "—")
    channels = d.get("channels", []) or []
    budget = d.get("budget", "—")
    calls = d.get("forecast_calls")
    price = d.get("forecast_price")
    ts = d.get("ts", "")
    contact = d.get("contact") or {}

    spec_label = {
        "Авто": "Бренд",
        "Недвижимость": "Категория",
        "Медицина": "Направление",
    }.get(category, "Выбор")

    channels_str = ", ".join(channels) if channels else "—"

    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        time_str = dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        time_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    forecast_block = ""
    if calls and price:
        forecast_block = (
            "\n📊 ПРОГНОЗ\n"
            f"• Звонков в месяц: ~{calls}\n"
            f"• Цена звонка: ~{price}\n"
        )

    contact_lines = []
    if contact:
        full_name = " ".join(filter(None, [contact.get("first_name"), contact.get("last_name")]))
        if full_name:
            contact_lines.append(f"👤 {full_name}")
        if contact.get("phone"):
            contact_lines.append(f"📞 +{contact['phone']}")
        if contact.get("user_id"):
            contact_lines.append(f"🆔 Telegram ID: {contact['user_id']}")
    elif user_name or user_handle:
        if user_name:
            contact_lines.append(f"👤 {user_name}")
        if user_handle:
            contact_lines.append(f"🆔 {user_handle}")
    else:
        contact_lines.append("👤 Контакт не предоставлен")

    contact_block = "\n".join(contact_lines)

    return (
        "🆕 НОВАЯ ЗАЯВКА — SINOBY MediaPlanBot\n"
        f"{'─' * 28}\n"
        "📋 ПАРАМЕТРЫ КАМПАНИИ\n"
        f"• Сфера: {category}\n"
        f"• Регион: {region} ({district})\n"
        f"• Город: {city}\n"
        f"• {spec_label}: {spec}\n"
        f"• Цель: {goal}\n"
        f"• Каналы: {channels_str}\n"
        f"• Бюджет: {budget}"
        f"{forecast_block}"
        f"\n{'─' * 28}\n"
        "📞 КОНТАКТ КЛИЕНТА\n"
        f"{contact_block}\n"
        f"\n🕐 {time_str}"
    )


def _is_configured() -> bool:
    if not VKTEAMS_TOKEN:
        log.warning("VK Teams: VKTEAMS_TOKEN не задан, пропускаем отправку")
        return False
    if not VKTEAMS_MANAGER_ID:
        log.warning("VK Teams: VKTEAMS_MANAGER_ID не задан, пропускаем отправку")
        return False
    return True


async def send_text_to_vkteams(chat_id: str, text: str) -> bool:
    """Отправка простого текста."""
    if not VKTEAMS_TOKEN:
        return False

    url = f"{VKTEAMS_API_BASE}/messages/sendText"
    params = {"token": VKTEAMS_TOKEN, "chatId": chat_id, "text": text}

    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as resp:
                payload = await resp.json(content_type=None)
                if payload.get("ok"):
                    log.info("VK Teams: текст отправлен в %s (msgId=%s)", chat_id, payload.get("msgId"))
                    return True
                log.error("VK Teams: ошибка отправки текста в %s: %s", chat_id, payload)
                return False
    except Exception as e:
        log.exception("VK Teams: исключение при отправке текста в %s: %s", chat_id, e)
        return False


async def send_file_to_vkteams(
    chat_id: str,
    file_bytes: bytes,
    filename: str,
    caption: Optional[str] = None,
) -> bool:
    """Отправка файла на /messages/sendFile (multipart/form-data)."""
    if not VKTEAMS_TOKEN:
        return False

    url = f"{VKTEAMS_API_BASE}/messages/sendFile"
    params = {"token": VKTEAMS_TOKEN, "chatId": chat_id}
    if caption:
        params["caption"] = caption

    try:
        timeout = aiohttp.ClientTimeout(total=60)
        form = aiohttp.FormData()
        form.add_field("file", file_bytes, filename=filename, content_type="application/octet-stream")

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, params=params, data=form) as resp:
                payload = await resp.json(content_type=None)
                if payload.get("ok"):
                    log.info(
                        "VK Teams: файл %s отправлен в %s (fileId=%s)",
                        filename, chat_id, payload.get("fileId"),
                    )
                    return True
                log.error("VK Teams: ошибка отправки файла в %s: %s", chat_id, payload)
                return False
    except Exception as e:
        log.exception("VK Teams: исключение при отправке файла в %s: %s", chat_id, e)
        return False


async def send_quiz_to_vkteams(
    quiz_data: dict,
    user_name: str = "",
    user_handle: str = "",
    chat_id: Optional[str] = None,
) -> bool:
    """Отправка результата квиза менеджеру в VK Teams (текстом)."""
    if not _is_configured():
        return False
    target = chat_id or VKTEAMS_MANAGER_ID
    text = _format_quiz_message(quiz_data, user_name=user_name, user_handle=user_handle)
    return await send_text_to_vkteams(target, text)


async def send_mediaplan_to_vkteams(
    file_bytes: bytes,
    filename: str,
    brand: str = "",
    city: str = "",
    chat_id: Optional[str] = None,
) -> bool:
    """Отправка XLSX-медиаплана менеджеру в VK Teams."""
    if not _is_configured():
        return False
    target = chat_id or VKTEAMS_MANAGER_ID
    caption_parts = [p for p in ("📄 Медиаплан", brand, city) if p]
    caption = " · ".join(caption_parts)
    return await send_file_to_vkteams(target, file_bytes, filename, caption)
