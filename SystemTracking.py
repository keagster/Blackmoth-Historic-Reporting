"""

This application can be executed as a cron or from and alternate service bus such as systemd

"""

import time
import sqlite3
import lib.trucks as trucks
import lib.BlackmothAPI as BlackmothAPI
from threading import Thread

# Start/Float database connection for use globally
try:
    sqlite = sqlite3.connect('bin\\system-history.db')
    query = sqlite.cursor()

    # Setup Database on first run
    query.execute('CREATE TABLE IF NOT EXISTS tigers(timedate real, name text, serial text, item text)')
    query.execute('CREATE TABLE IF NOT EXISTS cameras(timedate real, name text, cam_serial text, cam_item text)')
except:
    print('Error: Unable to start or float to SQLite3 database')


class CaptureSystemIds:
    def __init__(self):
        self.unit_ip = ''
        self.data = ''

        for truck in trucks.trucks:
            self.get_data(truck)

    def get_data_thread(self, ip):
        """
        Have decided to bypass threading at this time as sqlite will lock to single thread
        Will resolve this issue once main is working
        """
        get_data_thread = Thread(target=self.get_data, args=[ip])
        get_data_thread.start()

    def get_data(self, ip):
        sys_ids = BlackmothAPI.SystemIds(ip)
        sys_ids_data = sys_ids.system_ids
        RecordSystemIds(sys_ids_data)


class RecordSystemIds:
    def __init__(self, system_ids):
        self.system_ids = system_ids
        self.time_date = ''
        self.calc_live_data()
        self.sqlite_update()

    def calc_live_data(self):
        # Any other information that is required in future can be calculated and converted to class var here
        self.time_date = time.ctime()

    def sqlite_update(self):
        if self.system_ids != '':
            # Save Tiger Data to DB
            try:
                sqlite.execute('INSERT INTO tigers(timedate, name, serial, item) VALUES(?, ?, ?, ?)',
                               (self.time_date, self.system_ids['name'], self.system_ids['serial'], self.system_ids['item']))
                sqlite.commit()
                # Save Camera Data to DB
                for entry in self.system_ids['cameras']:
                    if entry != '':
                        sqlite.execute('INSERT INTO cameras(timedate, name, cam_serial, cam_item) VALUES(?, ?, ?, ?)',
                                       (self.time_date, self.system_ids['name'], entry['serial'], entry['item']))
                        sqlite.commit()
            except:
                print('Error: RecordSystemIds: sqlite_update(): Failed to execute sql query please check system_ids')
        else:
            print('Error: RecordSystemIds: sqlite_update(): self.system_ids empty')


if __name__ == '__main__':
    CaptureSystemIds()
    try:
        sqlite.commit()
        sqlite.close()
    except:
        print('Error: Failed to close SQLite3 Database safely')
