import requests
import sqlite3 as db
import time
import config as CONFIG

while True:
    conn = db.connect(CONFIG.DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM usage WHERE s=0")
    rows = cur.fetchall()

    entries = []

    for row in rows:
        entry = {
            'quantityInKilowatt': row[1],
            'timestampOfReading': row[0]
        }
        entries.append(entry)

    data = {
        'items': entries
    }

    # send request
    try:
        result = requests.post(CONFIG.API_ENDPOINT, json=data)
    except requests.exceptions.ConnectionError:
        time.sleep(2)
        continue

    # request succesful
    if(result.status_code == 201):
        timestampIds = []
        for entry in entries:
            timestampIds.append(entry['timestampOfReading'])
        query = "UPDATE usage SET s=1 WHERE t in %s" % str(tuple(timestampIds))
        cur.execute(query)
        conn.commit()

    conn.close()
    time.sleep(5)
