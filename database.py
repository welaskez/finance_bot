import sqlite3

from datetime import datetime


class Database:
    def __init__(self, db_name: str = 'db.sqlite3'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_categories_table()
        self._create_wastes_table()

    def _create_categories_table(self):
        query = (f"CREATE TABLE IF NOT EXISTS categories("
                 "id INTEGER PRIMARY KEY,"
                 f"category TEXT NOT NULL UNIQUE);")
        self.cursor.execute(query)
        self.connection.commit()

    def _create_wastes_table(self):
        query = (f"CREATE TABLE IF NOT EXISTS currencies_{datetime.now().strftime('%B_%Y')}("
                 "id INTEGER PRIMARY KEY,"
                 "category TEXT NOT NULL,"
                 "date TEXT NOT NULL,"
                 "amount INTEGER NOT NULL);")
        self.cursor.execute(query)
        self.connection.commit()

    def add_waste(self, category: str, amount: int | float, date: str):
        self.cursor.execute(f"INSERT INTO currencies_{datetime.now().strftime('%B_%Y')} (category, amount, date) "
                            f"VALUES (?,?,?)",
                            (category, amount, date))
        self.connection.commit()

    def delete_waste(self, category: str, amount: int | float, date: str):
        self.cursor.execute(f"DELETE FROM wastes WHERE category='{category}' AND amount={amount} AND date='{date}';")
        self.connection.commit()

    def get_today_wastes(self):
        today_date = str(datetime.now().strftime('%Y-%m-%d'))

        query = f"SELECT * FROM currencies_{datetime.now().strftime('%B_%Y')} WHERE date='{today_date}';"
        self.cursor.execute(query)
        wastes = self.cursor.fetchall()

        current_categories = self.get_categories()

        wastes_dict = {}
        for category in current_categories:
            wastes_dict[category[1]] = 0

        for waste in wastes:
            wastes_dict[waste[1]] += waste[3]

        total_today_wastes = sum(wastes_dict.values())

        return wastes_dict, total_today_wastes

    def add_category(self, category: str):
        self.cursor.execute("INSERT INTO categories (category) VALUES (?)", (category,))
        self.connection.commit()

    def delete_category(self, category: str):
        self.cursor.execute(f'DELETE FROM categories WHERE category="{category}";')
        self.connection.commit()

    def get_categories(self):
        self.cursor.execute('SELECT * FROM categories;')
        categories = self.cursor.fetchall()
        return categories

    def __del__(self):
        self.cursor.close()
        self.connection.close()
