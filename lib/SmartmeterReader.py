import sqlite3 as db
import serial, sys, config.config

class SmartmeterReader:
    def __init__(self, port, baudrate=115200, timeout=5):
        self.port = serial.Serial(port=port, baudrate=baudrate,
                                  timeout=timeout, writeTimeout=timeout)
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
            'tst_reading': None
        }

    def open(self):
        # open connection to the serial port
        try:
            self.port.open()
        except:
            sys.exit("Error opening port %s" % self.port.name)

    def close(self):
        # close connection to the serial port
        self.port.close()

    def read(self):
        # read serial port output
        return self.port.readline().rstrip()

    def listen(self):
        # start listening to serial port
        self.open()
        while True:
            output = self.read()
            self.compose_snapshot(output)

    def compose_snapshot(self, output):
        if output[0] == '/':
            self.snapshot['meter_model'] = output[1:]
        elif output[0:10] == '0-0:96.1.1':
            self.snapshot['meter_id'] = float(output[output.find("(")+1:output.find(")")].split('*')[0])
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
        elif output[0:9] == '1-0:24.2.1':
            self.snapshot['gas_consumption'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '0-0:1.0.0':
            self.snapshot['tst_reading'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0] == '!':
            if None not in self.snapshot.viewvalues():
                self.save_snapshot(self.snapshot)
            self.snapshot = dict.fromkeys(self.snapshot, None)

    def save_snapshot(self, snapshot):
        conn = db.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + config.DB_TABLE_NAME + " VALUES((?), (?), (?), (?), (?), (?), (?), (?), (?), (?) 0)",
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
                        snapshot['tst_reading'],
                        0
                    ))
        conn.commit()
        conn.close()
