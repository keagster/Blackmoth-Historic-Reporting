"""

This application can be executed as a cron or from and alternate service bus such as systemd

Note: This process will be quite slow until threading has been re-enabled

Will record the following information to database
1. From system IDs
a. tigers
- name
- IP (Allows for SIM/IP Tracking)
- serial
- item
- Tiger/Nordic Firmware Version
- DVR Firmware Version (To Be added when API complete found issues with keys between versions)
- Atlas Firmware Version
b. cameras
- name - As corresponds to the unit it was connected to
- serial
- item
- Camera Firmware Version

Database schema currently in conversion from sqlite3 to postgresql.
- This will resolve issues with threading
- As well as unify with the database types Blackmoth are using

"""

import time
import sqlite3
import psycopg2
import datetime
import lib.trucks as trucks
import lib.BlackmothAPI as BlackmothAPI
import lib.settings as settings
from threading import Thread

# Start/Float database connection for use globally
try:
    sqlite = sqlite3.connect('bin\\system-history.db')
    query = sqlite.cursor()

    # Create a global connection to Postgresql database
    # Connection settings must be configured in lib/settings
    connection = psycopg2.connect(database=settings.postgresql_settings['database'],
                                  user=settings.postgresql_settings['user'],
                                  password=settings.postgresql_settings['password'],
                                  host=settings.postgresql_settings['host'],
                                  port=settings.postgresql_settings['port'])

    cur = connection.cursor()

    # Configure database schema if first run
    # Data base must exist
    cur.execute('''CREATE TABLE IF NOT EXISTS tigers(time_date text, name text , ip_address text,
    serial text, item text, firmware_atlas text, dvr_version text);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS cameras(time_date text, name text, cam_serial text,
    cam_item text, firmware_camera text);''')

except:
    print('Error: Unable to connect to PostgreSQL please check database server')


class CaptureSystemIds:
    def __init__(self):
        self.unit_ip = ''
        self.data = ''

        for truck in trucks.trucks:
            self.get_data_thread(truck)

    def get_data_thread(self, ip):
        """
        Thread enabled internally start connection per thread
        to avoid conflict errors
        """
        get_data_thread = Thread(target=self.get_data, args=[ip])
        get_data_thread.start()

    def get_data(self, ip):
        sys_ids = BlackmothAPI.SystemIds(ip)
        firmware_get = BlackmothAPI.FirmwareVersion(ip)
        firmware_data = firmware_get.version_data
        sys_ids_data = sys_ids.system_ids

        # Check sys_ids_data and firmware data are full and start saving to database
        # Send updated dictionary to RecordSystemIds
        if sys_ids_data != '' and firmware_data != '':
            sys_ids_data.update({'ip': ip})
            sys_ids_data.update({'atlas': firmware_data['atlas'],
                                 'camera': firmware_data['camera'],
                                 'dvr': firmware_data['dvr']})
            RecordSystemIds(sys_ids_data)
        else:
            print('Error: CaptureSystemIds: get_data: API did not return valid data or is offline')


class RecordSystemIds:
    def __init__(self, system_ids):
        self.system_ids = system_ids
        self.time_date = ''
        self.thread_connection = psycopg2.connect(database=settings.postgresql_settings['database'],
                                                  user=settings.postgresql_settings['user'],
                                                  password=settings.postgresql_settings['password'],
                                                  host=settings.postgresql_settings['host'],
                                                  port=settings.postgresql_settings['port'])

        self.thread_cur = self.thread_connection.cursor()

        self.calc_live_data()
        self.sqlite_update()

    def calc_live_data(self):
        # Any other information that is required in future can be calculated and converted to class var here
        time_date_stamp = time.time()
        self.time_date = datetime.datetime.fromtimestamp(time_date_stamp).strftime('%Y-%m-%d_%H:%M:%S')

    def sqlite_update(self):
        if self.system_ids != '':
            # Save Tiger Data to DB
            try:
                # Create strings for tigers query
                tigers_query = "INSERT INTO tigers (time_date,name,ip_address,serial,item,firmware_atlas,dvr_version) \
                               VALUES (" + \
                               "'" + self.time_date + "'" + "," + \
                               "'" + self.system_ids['name'] + "'" + "," + \
                               "'" + self.system_ids['ip'] + "'" + "," + \
                               "'" + self.system_ids['serial'] + "'" + \
                               "," + "'" + self.system_ids['item'] + "'" + "," + \
                               "'" + self.system_ids['atlas'] + "'" + "," + \
                               "'" + self.system_ids['dvr'] + "'" + ") "

                self.thread_cur.execute(tigers_query)
                self.thread_connection.commit()
                # Save Camera Data to DB
                for entry in self.system_ids['cameras']:
                    if entry != '':
                        # Create string for cameras query
                        cameras_query = "INSERT INTO cameras (time_date,name,cam_serial,cam_item,firmware_camera)  \
                                        VALUES (" + "'" + self.time_date + "'" + "," + \
                                        "'" + self.system_ids['name'] + "'" + "," + \
                                        "'" + entry['serial'] + "'" + "," + \
                                        "'" + entry['item'] + "'" + "," + \
                                        "'" + self.system_ids['camera'] + "'" + ") "

                        self.thread_cur.execute(cameras_query)
                        self.thread_connection.commit()
            except:
                print('Error: RecordSystemIds: sqlite_update(): Failed to execute sql query please check system_ids')
        else:
            print('Error: RecordSystemIds: sqlite_update(): self.system_ids empty')


if __name__ == '__main__':
    CaptureSystemIds()
    try:
        connection.commit()
        # Threading issues caused when closing connection in this location
        # connection.close()
    except:
        print('Error: Failed to close PostgreSQL Database safely')
