import unittest
import unittest.mock as mock
from evdev import ecodes
from config import DOORPHONEEXTEN, originate_template
from doorphoneKeyboard import DoorphoneKeyboard


class MockEvent:
    def __init__(self):
        self.type = ecodes.EV_KEY
        self.value = 1
        self.code = 1


class DoorphoneKeyboardTest(unittest.TestCase):

    @mock.patch('doorphoneKeyboard.AsteriskAMI')
    def setUp(self, mock_ami):
        self.doorphone = DoorphoneKeyboard()

    def tearDown(self):
        pass

    def test_usb_keyboard_is_not_connected(self):
        with self.assertRaises(FileNotFoundError):
            self.doorphone.set_input_device("devicePathWithoutKeyboardPresent")

    @mock.patch('doorphoneKeyboard.InputDevice')
    def test_usb_keyboard_is_connected(self, mock_InputDevice):
        self.doorphone.set_input_device("device_path")
        mock_InputDevice.assert_called_with("device_path")

    def test_get_key_from_user(self):
        mock_event = MockEvent()
        self.doorphone.device = mock.Mock()
        self.doorphone.device.read_loop = mock.Mock(return_value=[mock_event])
        key = self.doorphone.get_keycode()
        self.assertEqual(key, mock_event.code)

    def test_get_apartment_number(self):
        code = "1"
        number = self.doorphone.get_apartment_number(code)
        self.assertEqual(number, "1")

    def test_call_apartment_checks_doorphone_is_available(self):
        self.doorphone.call_apartment("1")
        self.doorphone.ami.is_doorphone_available.assert_called_with(DOORPHONEEXTEN, "from-internal")

    @mock.patch('doorphoneKeyboard.AsteriskAMI')
    def test_call_apartment_with_doorphone_available(self, mock_ami):
        originate = originate_template
        originate["Exten"] = "1"
        self.doorphone.ami.is_doorphone_available.return_value = True
        self.doorphone.call_apartment("1")
        self.doorphone.ami.send_command.assert_called_with(originate)


if __name__ == "__main__":
    unittest.main()
