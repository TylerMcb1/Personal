import mysql.connector
from mysql.connector import Error

class Reservation:
    def __init__(self, reservation_id: str, first_name: str, last_name: str, 
                 start: str, destination: str, start_time: str, duration: int):
        """
        Initialize a Reservation object.

        Parameters:
            res_id (str): The reservation id of a passenger trip
            first_name (str): The first name of the passenger
            last_name (str): The last name of the passenger
            start (str): The start city of the trip
            destination (str): The desination city of the trip
            start_time (str): The start time of the trip
            duration (int): The duration of the trip
        """
        self.res_id = reservation_id
        self.first_name = first_name
        self.last_name = last_name
        self.start = start
        self.dest = destination
        self.start_time = start_time
        self.duration = duration
    
    def __repr__(self) -> str:
        return f"Reservation({self.res_id} {self.first_name} {self.last_name})"

    def __hash__(self) -> int:
        return hash(self.res_id)
    
class Timetable:
    def __init__(self, is_departure: bool, city: str, station_name: str,
                 start_time: str, arrival_time: str, num_stops: int):
        """
        Initialize a Timetable object.

        Parameters:
            is_departure (bool): 1 if train is departing, 0 if train is arriving
            city (str): The city the train is arriving at/departing from
            station_name (str): The station the train is arriving at/departing from
            start_time (str): The start time of the trip
            arrival_time (str): The arrival time of the trip
            num_stops (int): The number of stops for the trip
        """
        self.is_departure = is_departure
        self.city = city
        self.station_name = station_name
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.num_stops = num_stops

    def __repr__(self) -> str:
        return f"Timetable({self.is_departure} {self.city})"
    
    #def display(self):


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Initialize a Database object.

        Args:
            host (str): The host name or IP address of the database server.
            database (str): The name of the database.
            user (str): The username for the database connection.
            password (str): The password for the database connection.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        """ Connects to the PostgreSQL database. """
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )
        except Error as e:
            print('Error while attempting to connect to database', e)

    def disconnect(self):
        """ Disconnects from the PostgreSQL database. """
        if self.connection:
            self.connection.close()
            self.connection = None