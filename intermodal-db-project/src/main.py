import os

from db import Reservation, DBManager

db_name = 'intermodal train db'

def main():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    
    db_manager = DBManager(host, db_name, user, password)
    db_manager.connect()

    if db_manager.connection:
        db_manager.disconnect()
        print("Connection success")
    else:
        print("Connection failed")
    
if __name__ == '__main__':
    main()