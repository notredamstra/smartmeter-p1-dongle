from lib.SmartmeterReader import SmartmeterReader
import config

reader = SmartmeterReader(config.SERIAL_PORT)
reader.listen()
