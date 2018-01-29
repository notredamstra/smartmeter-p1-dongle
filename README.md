# Smart meter P1 Dongle
Read real-time energy data from ESMR 5.0 smart meter and write it to an external API for processing. Based on earlier work from [@gejanssen](https://github.com/gejanssen/slimmemeter-rpi).

## Hardware used to read smart meter
* Raspberry Pi 3B 
* USB - RJ11 cable (bought at [Dutch webshop](https://www.sossolutions.nl/slimme-meter-kabel?gclid=CjwKCAiAqbvTBRAPEiwANEkyCEnNKpPhHju9uXXN2DHgt3lLaOfotyFa6OEJdMGqX0M63YfPuXcQERoChlAQAvD_BwE "SOS Solutions"))

## Getting started
1. Clone this repository
```
git clone https://github.com/notredamstra/smartmeter-p1-dongle
```
2. Run `db_setup.py` to create SQLite3 database
```
python config/db_setup.py
```
3. Create new `config.py` file from `config.sample.py` with your specific information
```
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "example.db" <-- Setup assumes a sqlite file located in root of project
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DB_TABLE_NAME = "snapshots" <-- Rename DB table if you think of a cooler name

# set serial port config
SERIAL_BAUDRATE = 115200 <-- This might be different for older smart meters, check the supplier documentation
SERIAL_XONXOFF = 0
SERIAL_RTSCTS = 0
SERIAL_TIMEOUT = 20
SERIAL_PORT = "/dev/ttyUSB0" <-- This depends on the USB port connected to the smart meter, check your Raspberry

# API endpoint
API_ENDPOINT = "https://example-api/v1/endpoint" <-- This setup sends energy data to an external API
```
4. Run `meter_listener.py` as a background service. The script will continously read the P1-port on the smart meter and process the energy data.

5. Run `remote_sync.py` as a background service. This script will search the SQLite database for new entries and send them to the remote API.
