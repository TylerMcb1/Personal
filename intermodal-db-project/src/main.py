import os

from db import Reservation, DBManager

host_name = 'localhost'
db_name = 'testdb'

def main():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    db_manager = DBManager(host_name, db_name, user, password)
    db_manager.connect()

    if db_manager.connection:
        db_manager.disconnect()
        return "Connection success"
    else:
        return "Connection failed"
    
if __name__ == '__main__':
    main()