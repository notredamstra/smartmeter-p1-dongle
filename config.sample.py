import os.path
import serial

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "example.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# set serial port config
SERIAL_BAUDRATE = 115200
SERIAL_XONXOFF = 0
SERIAL_RTSCTS = 0
SERIAL_TIMEOUT = 20
SERIAL_PORT = "/dev/ttyUSB0"

ser = serial.Serial()
ser.baudrate = SERIAL_BAUDRATE
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = SERIAL_XONXOFF
ser.rtscts = SERIAL_RTSCTS
ser.timeout = SERIAL_TIMEOUT
ser.port = SERIAL_PORT

# API endpoint
API_ENDPOINT = "https://example-api/v1/endpoint"