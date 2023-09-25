import sqlite3
from datetime import datetime
conn = sqlite3.connect("maxi.db")


def create_table():
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS run_data(
        id INTEGER PRIMARY KEY,
        time TIMESTAMP,
        stw REAL,
        sog REAL,
        tws REAL,
        aws REAL,
        twa REAL,
        awa REAL,
        lon REAL,
        lat REAL)
    ''')
    c.close()


def insert_data(data):
    data["time"] = datetime.now()
    conn.execute(
        '''INSERT INTO run_data (time, stw, sog, tws, aws, twa, awa, lon, lat)
        VALUES (:time, :stw, :sog, :tws, :aws, :twa, :awa, :lon, :lat)''',
        data)
    conn.commit()


def read_data():
    c = conn.execute("SELECT * FROM run_data")
    for row in c:
        print(row)
    c.close()


if __name__ == "__main__":
    create_table()
    data = dict(stw=None, sog=None, tws=None, aws=None, twa=None, awa=None, lon=None, lat=None)
    insert_data(data)
    read_data()
