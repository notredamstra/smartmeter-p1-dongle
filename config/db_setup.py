import config, sqlite3
from sqlite3 import Error

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(config.DB_PATH)
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS snapshots (
         meter_model text NOT NULL,
         meter_id text NOT NULL,
         offpeak_consumption text NOT NULL,
         peak_consumption text NOT NULL,
         offpeak_redelivery text NOT NULL,
         peak_redelivery text NOT NULL,
         live_usage text NOT NULL,
         live_redelivery text NOT NULL,
         gas_consumption text NOT NULL,
         tst_reading text NOT NULL,
         s integer
        );
        """
    except Error as e:
        print(e)
    finally:
        conn.close()