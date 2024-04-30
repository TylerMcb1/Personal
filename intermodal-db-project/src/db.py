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
    

class Timetable:
    def __init__(self, city: str, station_name: str, start_time: str, 
                 arrival_time: str, num_stops: int):
        """
        Initialize a Timetable object.

        Parameters:
            city (str): The city the train is arriving at/departing from
            station_name (str): The station the train is arriving at/departing from
            start_time (str): The start time of the trip
            arrival_time (str): The arrival time of the trip
            num_stops (int): The number of stops for the trip
        """
        self.city = city
        self.station_name = station_name
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.num_stops = num_stops

    def __repr__(self) -> str:
        return f"Timetable({self.city})"


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
        """ Connects to the MySQL database. """
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password
            )

    def disconnect(self):
        """ Disconnects from the MySQL database. """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def get_all_reservations(self) -> list[Reservation]:
        """ Returns a list of all Reservation objects. """
        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                t.reservation_id,
                p.first_name,
                p.last_name,
                s.location AS `start`,
                e.location AS desination,
                r.start_time,
                r.duration 
            FROM
                trip t
                INNER JOIN passenger p ON p.passenger_id = t.passenger_id
                INNER JOIN route r ON r.route_id = t.route_num
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            ORDER BY
                r.start_time,
                s.location ASC;
            """
        )

        reservations = []
        for row in cur.fetchall():
            reservations.append(Reservation(row[0], row[1], row[2], row[3], 
                                            row[4], row[5], row[6]))
        
        cur.close()
        return reservations
    
    def reservation_search_by_name(self, name: str) -> list[Reservation]:
        """ 
        Searches for a Reservation by first and last name.

        Args:
            name (str): The name of the person with a Reservation
        """
        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                t.reservation_id,
                p.first_name,
                p.last_name,
                s.location AS `start`,
                e.location AS desination,
                r.start_time,
                r.duration 
            FROM
                trip t
                INNER JOIN passenger p ON p.passenger_id = t.passenger_id
                INNER JOIN route r ON r.route_id = t.route_num
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            WHERE
                p.first_name LIKE CONCAT('%', %s, '%')
                OR p.last_name LIKE CONCAT('%', %s, '%')
            ORDER BY
                p.first_name,
                p.last_name,
                s.location ASC;
            """,
            (name, name)
        )

        reservations = []
        for row in cur.fetchall():
            reservations.append(Reservation(row[0], row[1], row[2], row[3], 
                                            row[4], row[5], row[6]))
        
        cur.close()
        return reservations
    
    def reservation_search_by_id(self, res_id: str) -> list[Reservation]:
        """ 
        Searches for a Reservation by first and last name.

        Args:
            name (str): The name of the person with a Reservation
        """
        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                t.reservation_id,
                p.first_name,
                p.last_name,
                s.location AS `start`,
                e.location AS desination,
                r.start_time,
                r.duration 
            FROM
                trip t
                INNER JOIN passenger p ON p.passenger_id = t.passenger_id
                INNER JOIN route r ON r.route_id = t.route_num
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            WHERE
                t.reservation_id = %s;
            """,
            (res_id,)
        )

        reservations = []
        for row in cur.fetchall():
            reservations.append(Reservation(row[0], row[1], row[2], row[3], 
                                            row[4], row[5], row[6]))
        
        cur.close()
        return reservations
    
    def get_departures(self, city: str) -> list[Timetable]:
        """
        Gets all departing trains from a specified city

        Args:
            city (str): The name of the city
        """
        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT 
                e.location AS departure,
                e.`name` AS station_name,
                r.start_time,
                ADDTIME(r.start_time, SEC_TO_TIME(r.duration * 60)) AS arrival_time,
                r.num_stops
            FROM route r
                INNER JOIN end_station e ON e.station_id = r.destination
            WHERE r.`start` = %s;
            """,
            (city,)
        )

        timetable = []
        for row in cur.fetchall():
            timetable.append(Timetable(row[0], row[1], row[2], row[3], row[4]))
        
        cur.close()
        return timetable
    
    def get_arrivals(self, city: str) -> list[Timetable]:
        """
        Gets all arriving trains from a specified city

        Args:
            city (str): The name of the city
        """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT 
                s.location AS departure,
                s.`name` AS station_name,
                r.start_time,
                ADDTIME(r.start_time, SEC_TO_TIME(r.duration * 60)) AS arrival_time,
                r.num_stops
            FROM route r
                INNER JOIN start_station s ON s.station_id = r.`start`
            WHERE r.`destination` = %s;
            """,
            (city,)
        )

        timetable = []
        for row in cur.fetchall():
            timetable.append(Timetable(row[0], row[1], row[2], row[3], row[4]))
        
        cur.close()
        return timetable