import config, sqlite3
from sqlite3 import Error

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(config.DB_PATH)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

