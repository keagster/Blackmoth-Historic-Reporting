"""
Application was generated out of a need to fill some of the empty vars fields on some of the units
"""

import requests
import json
import lib.trucks as trucks
from threading import Thread


class FillVars:
    def __init__(self):
        self.io = ''
        for truck in trucks.trucks:
            self.fill_data_thread(truck, trucks.trucks[truck])

    def fill_data_thread(self, truck_ip, truck_name):
        fill_data_thread_run = Thread(target=self.fill_data, args=[truck_ip, truck_name])
        fill_data_thread_run.start()

    def fill_data(self, truck_ip, truck_name):
        url = 'http://' + truck_ip + ':8080/config/params/set/'
        update = {"key": "name", "val": truck_name}
        try:
            post = requests.post(url, data=json.dumps(update))
            print(post)
        except:
            print('Error: fill_data(): Failed to post data to: ' + str(truck_name))


if __name__ == '__main__':
    FillVars()
