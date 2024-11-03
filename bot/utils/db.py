# bot/utils/db.py

import sqlite3
from datetime import datetime


def initialize_db():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    # Створення таблиці для адрес
    cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                        id INTEGER PRIMARY KEY,
                        city TEXT,
                        street TEXT,
                        house_number TEXT,
                        entrance TEXT,
                        floor TEXT,
                        apartment_number TEXT
                    )''')
    # Створення таблиці для показників
    cursor.execute('''CREATE TABLE IF NOT EXISTS measurements (
                        id INTEGER PRIMARY KEY,
                        address_id INTEGER,
                        service TEXT,
                        previous_reading REAL,
                        current_reading REAL,
                        amount REAL,
                        date TEXT,
                        FOREIGN KEY (address_id) REFERENCES addresses(id)
                    )''')
    conn.commit()
    conn.close()


def save_address(data):
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO addresses (city, street, house_number, entrance, floor, apartment_number)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (data.get('city'), data.get('street'), data.get('house_number'),
                    data.get('entrance'), data.get('floor'), data.get('apartment_number')))
    conn.commit()
    conn.close()


def get_addresses():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, city, street, house_number FROM addresses")
    rows = cursor.fetchall()
    conn.close()

    addresses = [f"{row[1]}, {row[2]}, буд. {row[3]}" for row in rows]
    return addresses


def save_measurement(address_id, service, previous, current, amount):
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO measurements (address_id, service, previous_reading, current_reading, amount, date)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (address_id, service, previous, current, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()


def get_measurements_by_address(address_id):
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT service, previous_reading, current_reading, amount, date 
                      FROM measurements WHERE address_id = ? ORDER BY date DESC''', (address_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
