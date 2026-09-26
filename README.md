# Календарь с напоминаниями в Telegram

Веб-приложение на Flask: добавляете событие с датой и временем, и когда оно наступает, в Telegram приходит напоминание.

## Возможности

- добавление и удаление событий через веб-интерфейс;
- хранение событий в SQLite через SQLAlchemy;
- фоновая проверка наступивших событий и отправка сообщений через Telegram Bot API;
- повторная попытка отправки, если Telegram временно недоступен.

## Технологии

Python 3.10+, Flask, Flask-SQLAlchemy, SQLite, Telegram Bot API.

## Запуск

```bash
git clone https://github.com/<ваш-логин>/tg-calendar.git
cd tg-calendar
python -m venv venv
# Windows: venv\Scripts\activate    Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

Создайте файл `.env` по образцу `.env.example`:

- `BOT_TOKEN` выдаёт [@BotFather](https://t.me/BotFather);
- `CHAT_ID` можно узнать, написав боту [@userinfobot](https://t.me/userinfobot).

Не забудьте один раз написать своему боту `/start`, иначе он не сможет отправлять вам сообщения.

```bash
python app.py
```

Откройте http://127.0.0.1:5000 в браузере.

## Структура

```
app.py        маршруты Flask
models.py     модель Event
notifier.py   фоновая отправка напоминаний
config.py     настройки из .env
templates/    HTML-шаблоны
```

## Планы

- управление событиями прямо из Telegram (aiogram);
- несколько пользователей;
- планировщик APScheduler вместо цикла в потоке.
