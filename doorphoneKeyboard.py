from evdev import InputDevice, ecodes
from asterisk_ami import AsteriskAMI
from config import numbers, originate_template, DOORPHONEEXTEN, SERVER_PORT, SERVER_IP, USERNAME, PASSWORD


class DoorphoneKeyboard:
    def __init__(self):
        self.device = None
        self.numbers = numbers
        self.doorphone_extension = DOORPHONEEXTEN
        self.originate = originate_template
        self.ami = AsteriskAMI()
        self.ami.connect(SERVER_IP, SERVER_PORT)
        self.ami.login(USERNAME, PASSWORD)

    def set_input_device(self, path: str):
        """assign the device in <path> to use as keyboard"""
        device = InputDevice(path)
        self.device = device

    def get_keycode(self):
        """returns the code for a push down event in the keyboard"""
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:
                return event.code

    def get_apartment_number(self, code: str):
        """Returns a string with the apartment extension number"""
        return str(self.numbers[code])

    def call_apartment(self, extension: str):
        """Places a call to the extension number provided and connect it to the doorphone"""
        if self.ami.is_doorphone_available(self.doorphone_extension, "from-internal"):
            self.originate["Exten"] = extension
            try:
                self.ami.send_command(self.originate)
            except Exception as error:
                print(error)
        else:
            print("Doorphone unavailable")
