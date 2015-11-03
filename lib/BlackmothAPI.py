"""

Blackmoth API class library will allow for code base in other applications to be cut down by a large amount.

Still not complete.

"""

import requests
import json

"""

GPSStream is still under development

"""


class GPSStream:
    def __init__(self, ip):
        self.ip_entry_data = ip
        self.gps_stream_url = 'http://' + str(ip) + ':8080/gps/stream'
        self.stream_data = ''
        self.gps_stream()

    def gps_stream(self):
        try:
            stream = requests.get(self.gps_stream_url, stream=True)
            for i in stream.iter_lines():
                if i:
                    self.stream_data = json.loads(i.decode("utf-8"))
        except:
            print('Error: BlackMothAPI: GPSStream: Unable to start stream')
            return 1


class PoEState:
    def __init__(self, ip, state):
        self.ip_entry_data = ip
        self.state_change = state
        self.poe_down_url = 'http://' + self.ip_entry_data + ':8080/shutdown/powerdown/poe/'
        self.poe_up_url = 'http://' + self.ip_entry_data + ':8080/shutdown/powerup/poe/'
        self.poe_set()

    def poe_set(self):
        if self.state_change == 'off':
            try:
                powerdown = requests.get(self.poe_down_url)
                print(powerdown)
            except:
                print('Error: BlackMothAPI: poe_set: powerdown')
        elif self.state_change == 'on':
            try:
                powerup = requests.get(self.poe_up_url)
                print(powerup)
            except:
                print('Error: BlackMothAPI: poe_set: powerup')
        else:
            print('Error: BlackMothAPI: poe_set: please check IP = str and state = str')


class ScreenState:
    def __init__(self, ip, state):
        self.ip_entry_data = ip
        self.state_change = state
        self.screen_down_url = 'http://' + self.ip_entry_data + ':8080/shutdown/powerdown/screen/'
        self.screen_up_url = 'http://' + self.ip_entry_data + ':8080/shutdown/powerup/screen/'
        self.screen_set()

    def screen_set(self):
        if self.state_change == 'off':
            try:
                powerdown = requests.get(self.screen_down_url)
                print(powerdown)
            except:
                print('Error: BlackMothAPI: screen_set: powerdown')
        elif self.state_change == 'on':
            try:
                powerup = requests.get(self.screen_up_url)
                print(powerup)
            except:
                print('Error: BlackMothAPI: screen_set: powerup')
        else:
            print('Error: BlackMothAPI: screen_set: please check IP = str and state = str')


class GSMState:
    def __init__(self, ip):
        self.ip_entry_data = ip
        self.interface_url = 'http://' + self.ip_entry_data + ':8080/gsm/interface/'
        self.interface_data = ''
        self.gsm_get()

    def gsm_get(self):
        try:
            get = requests.get(self.interface_url)
            gsm_data = json.loads(get.text)
            self.interface_data = gsm_data
        except:
            print('Error: BlackMothAPI: GSMState: GSM Please check IP = str')
            return 1


class FirmwareVersion:
    def __init__(self, ip):
        self.ip_entry_data = ip
        self.version_url = 'http://' + self.ip_entry_data + ':8080/config/version/'
        self.version_data = ''
        self.version_get()

    def version_get(self):
        try:
            get = requests.get(self.version_url)
            self.version_data = json.loads(get.text)
        except:
            print('Error: BlackMothAPI: FirmwareVersion: Please check IP = str')
            return 1


class CameraConf:
    def __init__(self, ip):
        self.ip_entry_data = ip
        self.config_camera_url = 'http://' + str(ip) + ':8080/config/camera/'
        self.config_camera_data = ''

    def config_camera(self):
        try:
            get = requests.get(self.config_camera_url)
            self.config_camera_data = json.loads(get.text)
        except:
            print('Error: BlackMothAPI: CameraConf: Please check IP = str')
            return 1


class SystemIds:
    def __init__(self, ip):
        self.ip_entry_data = ip
        self.system_ids_url = 'http://' + str(ip) + ':8080/system/ids/'
        self.system_ids = ''
        self.get_system_ids()

    def get_system_ids(self):
        try:
            get = requests.get(self.system_ids_url)
            data = json.loads(get.text)
            self.system_ids = data
        except:
            print('Error: BlackmothAPI: SystemIds: Please check IP = str or Cannot reach: ' + str(self.ip_entry_data))
