import serial, sys

class SmartmeterReader:
    def __init__(self, port, OutputHandler, baudrate=115200, timeout=5):
        self.port = serial.Serial(port=port, baudrate=baudrate,
                                  timeout=timeout, writeTimeout=timeout)
        self.OutputHandler = OutputHandler

    def open(self):
        # open connection to the serial port
        try:
            self.port.open()
        except:
            sys.exit("Error opening port %s" % self.port.name)

    def close(self):
        # close connection to the serial port
        self.port.close()

    def read(self, raw=False):
        # read serial port output
        if(raw == False):
            return self.port.readline().rstrip()
        else:
            return self.port.readline()

    def listen(self):
        # start listening to serial port
        self.open()
        while True:
            output = self.read()
            # send output to outputhandler instance
            self.OutputHandler.handle(output)