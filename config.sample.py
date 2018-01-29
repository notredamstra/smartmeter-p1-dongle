import os.path
import serial

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "example.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DB_TABLE_NAME = "snapshots"

# set serial port config
SERIAL_BAUDRATE = 115200
SERIAL_XONXOFF = 0
SERIAL_RTSCTS = 0
SERIAL_TIMEOUT = 20
SERIAL_PORT = "/dev/ttyUSB0"

# API endpoint
API_ENDPOINT = "https://example-api/v1/endpoint"