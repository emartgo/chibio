# main/mocki2c.py
class MockI2CDevice:
    def __init__(self, address, busnum):
        self.address = address
        self.busnum = busnum

    def readU8(self, register):
        print(f"Mock readU8 from register {register} of device at address {self.address} on bus {self.busnum}")
        return 0

    def write8(self, register, value):
        print(f"Mock write8 value {value} to register {register} of device at address {self.address} on bus {self.busnum}")

class MockI2C:
    @staticmethod
    def get_i2c_device(address, busnum):
        return MockI2CDevice(address, busnum)

I2C = MockI2C()