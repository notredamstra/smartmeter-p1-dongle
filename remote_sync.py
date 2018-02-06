import requests
import sqlite3 as db
import time, config

while True:
    conn = db.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + config.DB_TABLE_NAME + " WHERE s=0")
    rows = cur.fetchall()

    entries = []

    for row in rows:
        entry = {
            'meter_model': row[0],
            'meter_id': row[1],
            'offpeak_consumption': row[2],
            'peak_consumption': row[3],
            'offpeak_redelivery': row[4],
            'peak_redelivery': row[5],
            'live_usage': row[6],
            'live_redelivery': row[7],
            'gas_consumption': row[8],
            'tst_reading_electricity': int(row[9]),
            'tst_reading_gas': int(row[10])
        }
        entries.append(entry)

    data = {
        'items': entries
    }

    # send request
    try:
        result = requests.post(config.API_ENDPOINT, json=data)
        print result
    except Exception, e:
        print e
        time.sleep(2)
        continue

    # request succesful
    if(result.status_code == 201):
        timestampIds = []
        for entry in entries:
            timestampIds.append(str(entry['tst_reading_electricity']).strip("L"))
        query = "UPDATE " + config.DB_TABLE_NAME + " SET s=1 WHERE tst_reading_electricity in %s" % str(tuple(timestampIds))
        print query
        try:
            cur.execute(query)
            print "Rows updated %s", cur.rowcount
        except Exception, e:
            print e
        conn.commit()

    conn.close()
    time.sleep(30)
