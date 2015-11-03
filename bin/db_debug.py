import sqlite3

# Start/Float database connection for use globally
try:
    sqlite = sqlite3.connect('bin\\system-history.db')
    query = sqlite.cursor()
except:
    print('Error: Unable to start or float to SQLite3 database')


query.execute('select * from')


try:
    sqlite.close()
except:
    print('Error: Failed to close SQLite3 Database safely')
