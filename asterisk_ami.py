import socket


class AsteriskAMI:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_ip: str, server_port: int):
        """Connects with the asterisk AMI"""
        try:
            self.socket.connect((server_ip, server_port))
        except Exception as error:
            raise("error: couldn't connect to asterisk", error)

    def login(self, username: str, password: str):
        """Login with asterisk AMI """
        response = self.send_command({
            "Action": "Login",
            "Username": username,
            "Secret": password,
            "Events": "OFF"})
        if 'Response: Success' not in response:
            raise Exception(response)

    def send_command(self, args: dict):
        """Sends the command to asterisk AMI"""
        command = ""
        for key, value in args.items():
            command += key + ": " + value + "\r\n"
        command += "\r\n"
        return self.socket.send(command)

    def is_doorphone_available(self, extension: str, context: str):
        """Check if the doorphone extension it's available"""
        response = (self.send_command(dict(Action="ExtensionState", Exten=extension, Context=context)))
        return True if "Status: 0" in response else False

    def disconnect(self):
        """Closes the connection to Asterisk AMI"""
        self.socket.close()
