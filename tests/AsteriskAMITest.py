import unittest
import unittest.mock as mock
from asterisk_ami import AsteriskAMI
from config import SERVER_IP, SERVER_PORT


class AsteriskAMITest(unittest.TestCase):
    def setUp(self):
        self.ami = AsteriskAMI()

    @mock.patch('asterisk_ami.socket.socket.connect')
    def test_connect(self, mock_connect):
        self.ami.connect(SERVER_IP, SERVER_PORT)
        mock_connect.assert_called_with((SERVER_IP, SERVER_PORT))

    def test_connect_fail(self):
        with self.assertRaises(Exception):
            self.ami.connect(SERVER_IP, SERVER_PORT)

    @mock.patch('asterisk_ami.socket.socket.send')
    def test_login(self, mock_send):
        mock_send.return_value =\
            "Response: Success\r\n"\
            "Message: Authentication accepted\r\n"
        params = ["Action: Login\r\n", "Username: user\r\n", "Secret: password\r\n", "Events: OFF\r\n", "\r\n\r\n"]
        self.ami.login("user", "password")
        args, kwargs = mock_send.call_args
        for param in params:
            self.assertIn(param, args[0])

    @mock.patch('asterisk_ami.socket.socket.send')
    def test_login_failed(self, mock_send):
        mock_send.return_value = \
            "Response: Error\r\n" \
            "Message: Authentication failed\r\n"
        with self.assertRaises(Exception):
            self.ami.login("user", "password")

    @mock.patch('asterisk_ami.socket.socket.send')
    def test_is_extension_available_call_value(self, mock_send):
        params = ["Action: ExtensionState\r\n", "Exten: 10\r\n", "Context: from-internal\r\n", "\r\n\r\n"]
        self.ami.is_doorphone_available("10", "from-internal")
        args, kwargs = mock_send.call_args
        for param in params:
            self.assertIn(param, args[0])

    @mock.patch('asterisk_ami.socket.socket.send')
    def test_is_extension_available_return_value(self, mock_send):
        mock_send.return_value = \
            "Response: Success\r\n" \
            "ActionID: 1\r\n" \
            "Message: Extension Status\r\n" \
            "Exten: 10\r\n" \
            "Context: from-internal\r\n" \
            "Hint: \r\n" \
            "Status: 0\r\n\r\n"
        response = self.ami.is_doorphone_available("10", "from-internal")
        self.assertTrue(response)

    def tearDown(self):
        self.ami.disconnect()


if __name__ == "__main__":
    unittest.main()
