import time

from doorphoneKeyboard import DoorphoneKeyboard
from config import device_path


def main():
    while True:
        try:
            doorphone = DoorphoneKeyboard()
            doorphone.set_input_device(device_path)
            doorphone.device.grab()
        except (FileNotFoundError, IOError):
            print("Keyboard not found")
            time.sleep(3)
        except Exception as error:
            print(error)
            time.sleep(3)
        else:
            while True:
                key = doorphone.get_keycode()
                number = doorphone.get_apartment_number(str(key))
                doorphone.call_apartment(number)


if __name__ == "__main__":
    import sys
    sys.exit(main())
