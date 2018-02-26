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
         offpeak_consumption real ,
         peak_consumption real ,
         offpeak_redelivery real ,
         peak_redelivery real ,
         live_usage real ,
         live_redelivery real ,
         gas_consumption real ,
         tst_reading_electricity integer ,
         tst_reading_gas integer ,
         s integer
        );
        """
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)
    finally:
        conn.close()