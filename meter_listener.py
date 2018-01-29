import config.config
from lib.SmartmeterReader import SmartmeterReader

reader = SmartmeterReader(config.SERIAL_PORT)
reader.listen()
