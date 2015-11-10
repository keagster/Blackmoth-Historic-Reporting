"""

Settings stores all configurable aspects to the logging

This file should be configured when ever the application is run on a new system

Use of getpass should be implemented on any production version of this system. DO NOT STORE PRODUCTION PASSWORDS.

"""

# PostgreSQL Configuration
# Must create database before use
postgresql_settings = {'database': 'data_tracking',
                       'user': 'postgres',
                       'password': 'alpha123',
                       'host': '127.0.0.1',
                       'port': '5432'
                       }
