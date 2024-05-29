# main/mocksmbus.py
class MockSMBus:
    def __init__(self, bus):
        self.bus = bus
        print(f"Mock SMBus created for bus {bus}")

    def read_byte_data(self, addr, cmd):
        print(f"Mock read_byte_data from addr {addr}, cmd {cmd}")
        return 0

    def write_byte_data(self, addr, cmd, value):
        print(f"Mock write_byte_data to addr {addr}, cmd {cmd}, value {value}")

    def read_word_data(self, addr, cmd):
        print(f"Mock read_word_data from addr {addr}, cmd {cmd}")
        return 0

    def write_word_data(self, addr, cmd, value):
        print(f"Mock write_word_data to addr {addr}, cmd {cmd}, value {value}")

SMBus = MockSMBus
