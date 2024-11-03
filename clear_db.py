import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("services.db")
cursor = conn.cursor()

# Додаємо колонки, якщо вони ще не існують
try:
    cursor.execute("ALTER TABLE addresses ADD COLUMN city TEXT")
    cursor.execute("ALTER TABLE addresses ADD COLUMN street TEXT")
    cursor.execute("ALTER TABLE addresses ADD COLUMN house_number TEXT")
    cursor.execute("ALTER TABLE addresses ADD COLUMN entrance TEXT")
    cursor.execute("ALTER TABLE addresses ADD COLUMN floor TEXT")
    cursor.execute("ALTER TABLE addresses ADD COLUMN apartment_number TEXT")
    conn.commit()
except sqlite3.OperationalError:
    print("Колонки вже існують або не потребують додавання.")

# Закриваємо з'єднання
conn.close()
