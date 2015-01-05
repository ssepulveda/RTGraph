#!/usr/bin/env python
from os import name
if name == 'posix':
    from serial.tools import list_ports

def getSerialPorts():
    portList = []
    if name == 'posix':
        try:
            for ports in list_ports.comports():
                if ports[2] != "n/a":
                    portList.append(ports[0])
        except:
            portList = ['/dev/ttyUSB0', '/dev/ttyUSB1',
                        '/dev/ttyACM0', '/dev/ttyACM1']
    else:
        portList = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5']
    return portList
