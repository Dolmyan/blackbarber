import json
import logging
import sqlite3
from datetime import datetime


class BotDB:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS availability (
                day_of_week INT     NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
                start_time  TIME    NOT NULL,
                end_time    TIME    NOT NULL,
                is_free     BOOLEAN NOT NULL DEFAULT TRUE,
                PRIMARY KEY (day_of_week, start_time)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id           INTEGER   PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER   NOT NULL,
                username     TEXT,
                first_name   TEXT,
                last_name    TEXT,
                service      TEXT      NOT NULL,
                day_of_week  INTEGER   NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
                time         TEXT      NOT NULL,
                phone_number TEXT,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT    NOT NULL
            )
        ''')


        self.connection.commit()

    def get_services(self):
        self.cursor.execute('SELECT name FROM services')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows] if rows else []

    def get_available_times(self, day_of_week: int):
        self.cursor.execute('''
            SELECT start_time FROM availability
            WHERE day_of_week = ? AND is_free = 1
            ORDER BY start_time
        ''', (day_of_week,))
        rows = self.cursor.fetchall()
        return [f"{row[0]}" for row in rows]

    def add_appointment(
            self,
            user_id: int,
            username: str,
            first_name: str,
            last_name: str,
            service: str,
            day_of_week: int,
            time: str,
            phone_number: str = None
    ) -> int:
        self.cursor.execute('''
            INSERT INTO appointments (
                user_id, username, first_name, last_name,
                service, day_of_week, time, phone_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            username,
            first_name,
            last_name,
            service,
            day_of_week,
            time,
            phone_number
        ))
        self.connection.commit()
        return self.cursor.lastrowid

    # database.py
    def get_all_appointments(self):
        self.cursor.execute('''
            SELECT service, day_of_week, time, phone_number, first_name, last_name, username, id
            FROM appointments
            ORDER BY day_of_week, time
        ''')
        return self.cursor.fetchall()

    def confirm_appointment(self, appointment_id: int):
        # Получаем данные о записи
        self.cursor.execute('''
            SELECT day_of_week, time
            FROM appointments
            WHERE id = ?
        ''', (appointment_id,))
        result = self.cursor.fetchone()

        if not result:
            return False

        day_of_week, time = result


        # Помечаем время как занятое в таблице availability
        self.cursor.execute('''
            UPDATE availability
            SET is_free = 0
            WHERE day_of_week = ? AND start_time = ?
        ''', (day_of_week, time))

        self.connection.commit()
        return True


    def cancel_appointment(self, appointment_id: int):
        # Получаем данные о записи
        self.cursor.execute('''
            SELECT day_of_week, time
            FROM appointments
            WHERE id = ?
        ''', (appointment_id,))
        result = self.cursor.fetchone()

        if not result:
            return False

        day_of_week, time = result

        # Освобождаем время в таблице availability
        self.cursor.execute('''
            UPDATE availability
            SET is_free = 1
            WHERE day_of_week = ? AND start_time = ?
        ''', (day_of_week, time))

        # Удаляем запись из таблицы appointments
        self.cursor.execute('''
            DELETE FROM appointments
            WHERE id = ?
        ''', (appointment_id,))

        self.connection.commit()
        return True

    def add_service(self, service: str):
        self.cursor.execute('INSERT INTO services (name) VALUES (?)', (service,))
        self.connection.commit()

    def remove_service(self, service: str):
        self.cursor.execute('DELETE FROM services WHERE name = ?', (service,))
        self.connection.commit()