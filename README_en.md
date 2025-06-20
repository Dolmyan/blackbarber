
# 💈 BlackBarber Telegram Bot

A Telegram bot for online bookings. It allows users to choose services, book appointments, and enables admins to manage schedules.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?logo=telegram)
![SQLite](https://img.shields.io/badge/SQLite-Used-green?logo=sqlite)

---

## 🚀 Features

- 📅 Client booking by day and time
- 🧔 Service selection from a list
- 📲 Saving contact information
- 📋 Admin panel: manage schedule and appointments
- 🔔 Notifications about new bookings

---

## 🛠️ Technologies

- `Python 3.12+`
- `Aiogram 3.x` — Telegram Bot API framework
- `SQLite` — lightweight local database

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dolmyan/blackbarber.git
   cd blackbarber
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Open `config.py`** and add your bot token and master info:
   ```python
   TG_TOKEN="your_telegram_bot_token_here"
   admin_id="master_user_id"
   master_first_name = "master_first_name"
   master_last_name = "master_last_name"
   master_location = "master_adress"
   master_phone_number = "master_phone_number"   ```

---

## ▶️ Running the Bot

```bash
python main.py
```

---

## 🗂️ Project Structure

```
blackbarber/
│
├── main.py                 # Entry point
├── config.py              # Configuration
├── database.py            # Database logic
├── states.py              # FSM states
├── blackbarber.db         # SQLite database (temporary)
│
├── app/                   # Bot logic
│   ├── start.py
│   ├── appointments.py
│   ├── admin_add_appointment.py
│   └── ... other modules
```

---

## 🤝 Author

- Developer: [@bigboyandroid](https://t.me/bigboyandroid)
