# 💈 BlackBarber Telegram Bot

Telegram-бот для онлайн-записи. Позволяет пользователям выбирать услуги, бронировать время, а администраторам —
управлять расписанием.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?logo=telegram)
![SQLite](https://img.shields.io/badge/SQLite-Used-green?logo=sqlite)

---

## 🚀 Возможности

- 📅 Запись клиентов по дням недели и времени
- 🧔 Выбор услуг из списка
- 📲 Сохранение контактных данных
- 📋 Админ-панель: управление расписанием и записями
- 🔔 Уведомления о новых записях

---

## 🛠️ Технологии

- `Python 3.12+`
- `Aiogram 3.x` — Telegram Bot API
- `SQLite` — локальная база данных

---

## 📦 Установка

1. **Клонируй репозиторий**:
   ```bash
   git clone https://github.com/dolmyan/blackbarber.git
   cd blackbarber
   ```

2. **Создай виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   ```

3. **Установи зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Открой файл `config.py`**, добавь свой токен, данные мастера:
   ```python
   TG_TOKEN="your_telegram_bot_token_here"
   admin_id="master_user_id"
   master_first_name = "master_first_name"
   master_last_name = "master_last_name"
   master_location = "master_adress"
   master_phone_number = "master_phone_number"
   ```

---

## ▶️ Запуск

```bash
python main.py
```

---

## 🗂️ Структура проекта

```
blackbarber/
│
├── main.py                 # Точка входа
├── config.py              # Настройки
├── database.py            # Работа с БД
├── states.py              # FSM-состояния
├── blackbarber.db         # Файл SQLite (временно)
│
├── app/                   # Основная логика бота
│   ├── start.py
│   ├── appointments.py
│   ├── admin_add_appointment.py
│   └── ... и другие модули
```

---

## 🤝 Авторы

- Разработчик: [@bigboyandroid](https://t.me/bigboyandroid)
