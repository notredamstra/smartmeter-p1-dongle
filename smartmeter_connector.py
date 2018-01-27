import sys
import sqlite3 as db
import time
import config as CONFIG

# open serial port
try:
    CONFIG.ser.open()
except:
    sys.exit("Error opening port %s." % CONFIG.ser.name)

# listen to serial port and write output to db
while True:
    p1_line = CONFIG.ser.readline().rstrip()
    curr_usage = None
    if p1_line[0:9] == "1-0:1.7.0":
        curr_usage = float(p1_line[p1_line.find("(")+1:p1_line.find(")")].split('*')[0])
        conn = db.connect(CONFIG.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO usage VALUES((?), (?), 0)", (time.time(), curr_usage))
        conn.commit()
    else:
        pass