from sqlite3 import Error

import config
import sqlite3

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(config.DB_PATH)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS snapshots (
         meter_model text ,
         meter_id text ,
         offpeak_consumption text ,
         peak_consumption text ,
         offpeak_redelivery text ,
         peak_redelivery text ,
         live_usage text ,
         live_redelivery text ,
         gas_consumption text ,
         tst_reading_electricity text ,
         tst_reading_gas text ,
         s integer
        );
        """
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)
    finally:
        conn.close()