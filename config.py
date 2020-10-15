# device_path = "/dev/input/by-path/pci-0000:00:1a.0-usb-0:1.2:1.0-event-kbd"
device_path = "/dev/input/event16"
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5038
DOORPHONEEXTEN = "10"
USERNAME = "username"
PASSWORD = "password"

originate_template = {
    "Action": "Originate",
    "Channel": "LOCAL/01@from-internal",
    "Context": "from-internal",
    "Exten": "",
    "Priority": "1",
    "Timeout": "2000",
    "CallerID": "Portero Calle",
    "Variable": "CHANNEL(language)=es"
}

numbers = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "q": 10,
    "w": 11,
    "r": 12,
    "t": 13,
    "y": 14,
    "u": 15
}
