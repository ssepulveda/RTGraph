
class Serial:
    def __init__( self, port='COM1', baudrate=115200, timeout=1,
                  bytesize=8, parity='N', stopbits=1, xonxoff=0,
                  rtscts=0):
        self.name = port
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self._is_open = True
        self._receivedData = ""
        self._data = ""

    def is_open(self):
        return self._is_open

    def open( self ):
        self._is_open = True

    def close( self ):
        self._is_open = False

    def write( self, string):
        self._data += string

    def read(self, n=1):
        s = self._data[0:n]
        self._data = self._data[n:]
        return s

    def readline(self):
        returnIndex = self._data.index("\n")
        if returnIndex != -1:
            s = self._data[0:returnIndex + 1]
            self._data = self._data[returnIndex + 1:]
            return s
        else:
            return ""
