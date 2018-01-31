import sqlite3 as db
import re
import serial
import sys

import config


class SmartmeterReader:
    def __init__(self, port, baudrate=115200, timeout=5):
        try:
            self.port = serial.Serial(port=port, baudrate=baudrate,
                                  timeout=timeout, writeTimeout=timeout)
        except:
            sys.exit("Error opening port %s" % self.port.name)

        self.snapshot = {
            'meter_model': None,
            'meter_id': None,
            'offpeak_consumption': None,
            'peak_consumption': None,
            'offpeak_redelivery': None,
            'peak_redelivery': None,
            'live_usage': None,
            'live_redelivery': None,
            'gas_consumption': None,
            'tst_reading_electricity': None,
            'tst_reading_gas': None
        }

    def close(self):
        # close connection to the serial port
        self.port.close()

    def read(self):
        # read serial port output
        return self.port.readline().rstrip()

    def listen(self):
        # start listening to serial port
        while True:
            output = self.read()
            self.compose_snapshot(output)

    def compose_snapshot(self, output):
        if not output:
            return

        if output[0] == '/':
            self.snapshot['meter_model'] = output[1:]
        elif output[0:10] == '0-0:96.1.1':
            self.snapshot['meter_id'] = output[output.find("(")+1:output.find(")")].split('*')[0]
        elif output[0:9] == '1-0:1.8.1':
            self.snapshot['offpeak_consumption'] = float(output[output.find("(")+1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:1.8.2':
            self.snapshot['peak_consumption'] = float(output[output.find("(")+1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.8.1':
            self.snapshot['offpeak_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.8.2':
            self.snapshot['peak_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:1.7.0':
            self.snapshot['live_usage'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.7.0':
            self.snapshot['live_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:10] == '0-1:24.2.1':
            parts = re.findall(r"\(([A-Za-z0-9_*.]+)\)", output)
            self.snapshot['tst_reading_gas'] = parts[0][parts[0].find("(") + 1:parts[0].find(")")].split('W')[0]
            self.snapshot['gas_consumption'] = float(parts[1][parts[1].find("(") + 1:parts[1].find(")")].split('*')[0])
        elif output[0:9] == '0-0:1.0.0':
            self.snapshot['tst_reading_electricity'] = output[output.find("(") + 1:output.find(")")].split('W')[0]
        elif output[0] == '!':
            if None not in self.snapshot.viewvalues():
                self.save_snapshot(self.snapshot)
            self.snapshot = dict.fromkeys(self.snapshot, None)

    def save_snapshot(self, snapshot):
        conn = db.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + config.DB_TABLE_NAME + " VALUES((?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), 0)",
                    (
                        snapshot['meter_model'],
                        snapshot['meter_id'],
                        snapshot['offpeak_consumption'],
                        snapshot['peak_consumption'],
                        snapshot['offpeak_redelivery'],
                        snapshot['peak_redelivery'],
                        snapshot['live_usage'],
                        snapshot['live_redelivery'],
                        snapshot['gas_consumption'],
                        snapshot['tst_reading_electricity'],
                        snapshot['tst_reading_gas']
                    ))
        conn.commit()
        conn.close()