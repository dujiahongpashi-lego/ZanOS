from uart2 import UART2
from wifi_network import WifiNetwork
from ble_keyboard import BLEKeyboard

u2 = UART2()  # p5 连G16, p6连G17
net = WifiNetwork()


def on_keyboard_connect():
    u2.response('KEYBOARD_STATUS', 'READY')


def on_keyboard_miss_connection():
    u2.response('KEYBOARD_STATUS', 'MISS')


def on_key_press(key):
    u2.response('KEY_PRESSED', key)


ble = BLEKeyboard(on_success=on_keyboard_connect,
                  on_fail=on_keyboard_miss_connection, on_key_press=on_key_press)


def network_connect(data):
    ssid = data['ssid']
    password = data['password']
    net.connect(ssid, password)
    while not net.is_connected():
        pass
    res = {'ssid': net.ssid, 'status': 'online'}
    u2.response('WIFI_STATUS', res)


def is_connect(data):
    res = {'ssid': '', 'status': 'off-line'}
    if net.is_connected():
        res = {'ssid': net.ssid, 'status': 'online'}
    u2.response('WIFI_STATUS', res)


def network_request(data):
    if not net.is_connected():
        print('Not Online.')
        return
    url = data['url']
    label = data['label']

    def cb(resp, label=label):
        data = {'label': label, 'response': resp}
        u2.response('HTTP_RESPONSE', data)
    net.get_request(url, cb)


def init_keyboard(data):
    # try:
        found_keyboard = ble.scan_connect()
        # if not found_keyboard:
        #     print("Scanning timed out")
        #     del(ble)
        #     return False
        # time.sleep(600)

        # ble.disconnect()
        # print("LEGO Disconnected")
        # time.sleep_ms(2000)

    # except Exception as e:
    #     print("ERROR!!!!", e)
    #     return False

    # print("Restar keyboard scan")
    # return True

def start():
    master_cmds = [
        {'scope': 'CONNECT_WIFI', 'cb': network_connect},
        {'scope': 'CONNECT_KEYBOARD', 'cb': init_keyboard},
        {'scope': 'ASK_WIFI_STATUS', 'cb': is_connect},
        {'scope': 'REQ_HTTP', 'cb': network_request},
    ]

    u2.reg_listener(master_cmds)

start()
