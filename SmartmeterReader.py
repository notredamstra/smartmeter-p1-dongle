import serial, sys

class SmartmeterReader:
    def __init__(self, port, SM_Processor, baudrate=115200, timeout=5):
        self.port = serial.Serial(port=port, baudrate=baudrate,
                                  timeout=timeout, writeTimeout=timeout)
        self.SM_Processor = SM_Processor
        self.snapshot = {
            'meter_id': None,
            'offpeak_consumption': None,
            'peak_consumption': None,
            'offpeak_redelivery': None,
            'peak_redelivery': None,
            'current_usage': None,
            'current_redelivery': None,
            'gas_consumption': None
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
            self.snapshot['meter_id'] = output[1:]
        elif output[0] == '!':
            if None not in self.snapshot.viewvalues():
                self.SM_Processor.process(self.snapshot)
            self.snapshot = dict.fromkeys(self.snapshot, None)
        elif output[0:9] == '1-0:1.8.1':
            self.snapshot['offpeak_consumption'] = float(output[output.find("(")+1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:1.8.2':
            self.snapshot['peak_consumption'] = float(output[output.find("(")+1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.8.1':
            self.snapshot['offpeak_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.8.2':
            self.snapshot['peak_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:1.7.0':
            self.snapshot['current_usage'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:2.7.0':
            self.snapshot['current_redelivery'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])
        elif output[0:9] == '1-0:24.2.1':
            self.snapshot['gas_consumption'] = float(output[output.find("(") + 1:output.find(")")].split('*')[0])