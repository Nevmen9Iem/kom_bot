# bot/utils/db.py

import sqlite3


def initialize_db():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS addresses (
                        id INTEGER PRIMARY KEY,
                        city TEXT,
                        street TEXT,
                        house_number TEXT,
                        entrance TEXT,
                        floor TEXT,
                        apartment_number TEXT
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
    cursor.execute("SELECT city, street, house_number FROM addresses")
    rows = cursor.fetchall()
    conn.close()

    # Форматування для відображення в меню
    addresses = [f"{row[0]}, {row[1]}, буд. {row[2]}" for row in rows]
    return addresses
