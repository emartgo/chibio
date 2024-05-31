# main/mockgpio.py
class MockGPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    HIGH = True
    LOW = False

    def setmode(self, mode):
        print(f"GPIO setmode({mode})")

    def setup(self, pin, mode):
        print(f"GPIO setup(pin={pin}, mode={mode})")

    def output(self, pin, state):
        print(f"GPIO output(pin={pin}, state={state})")

    def cleanup(self):
        print("GPIO cleanup()")

