import logging
import time
from datetime import datetime

import requests

import config
from models import Event, db

log = logging.getLogger(__name__)


def send_tg_message(text: str) -> bool:
    """Отправляет сообщение в Telegram. Возвращает True, если всё прошло успешно."""
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        log.error("Ошибка сети при отправке в Telegram: %s", e)
        return False

    if response.status_code != 200:
        log.error("Telegram вернул %s: %s", response.status_code, response.text)
        return False
    return True


def format_reminder(event: Event) -> str:
    return (
        "🔔 Напоминание!\n"
        f"Событие: {event.title}\n"
        f"Время: {event.event_time.strftime('%d.%m.%Y %H:%M')}"
    )


def check_due_events():
    """Один проход: находит наступившие события и отправляет напоминания."""
    now = datetime.now()
    due_events = Event.query.filter(
        Event.is_notified.is_(False),
        Event.event_time <= now,
    ).all()

    for event in due_events:
        # Помечаем отправленным, только если сообщение действительно дошло,
        # иначе попробуем снова на следующей проверке.
        if send_tg_message(format_reminder(event)):
            event.is_notified = True
            db.session.commit()
            log.info("Отправлено напоминание: %s", event.title)


def run_notifier(app):
    """Бесконечный цикл для фонового потока."""
    log.info("Фоновая проверка напоминаний запущена (каждые %s с)", config.CHECK_INTERVAL)
    while True:
        with app.app_context():
            try:
                check_due_events()
            except Exception:
                # Одна ошибка не должна навсегда остановить поток
                log.exception("Ошибка при проверке событий")
        time.sleep(config.CHECK_INTERVAL)
