from enum import Enum

class PrinterStates(Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"

class SingleTonPrinter():
    singlePrinter = None
    def __new__(cls):
        if(SingleTonPrinter.singlePrinter is None):
            newObject = super().__new__(cls)
            newObject.state = PrinterStates.IDLE
            SingleTonPrinter.singlePrinter = newObject
            return newObject
        else:
            return SingleTonPrinter.singlePrinter

        
    def setRunning(self):
        self.state = PrinterStates.RUNNING

    def setIdle(self):
        self.state = PrinterStates.IDLE

p1 = SingleTonPrinter()
print(p1.state)
p1.setRunning()


p2 = SingleTonPrinter()
print(p2.state)
