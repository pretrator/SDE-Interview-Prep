class PrivateTest():
    def __init__(self):
        self._privateTest = 24
        self.nonPrivate = 23


p = PrivateTest()
p._privateTest = 45