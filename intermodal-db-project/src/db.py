import mysql.connector
from mysql.connector import Error

from objects import Reservation, Timetable, Route, Train

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
                SEC_TO_TIME(r.duration * 60) AS duration 
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
                SEC_TO_TIME(r.duration * 60) AS duration 
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
                SEC_TO_TIME(r.duration * 60) AS duration 
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
    
    def get_departures(self, station: str) -> list[Timetable]:
        """
        Gets all departing trains from a specified station

        Args:
            station (str): The ID of the station
        """
        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                e.location AS city,
                e.`name` AS station_name,
                r.start_time,
                ADDTIME(
                    r.start_time,
                SEC_TO_TIME( r.duration * 60 )) AS arrival_time,
                r.start_platform 
            FROM
                route r
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            WHERE
                r.`start` = %s 
            ORDER BY
                r.start_time,
                arrival_time DESC;
            """,
            (station,)
        )

        timetable = []
        for row in cur.fetchall():
            timetable.append(Timetable(row[0], row[1], row[2], row[3], row[4]))
        
        cur.close()
        return timetable
    
    def get_arrivals(self, station: str) -> list[Timetable]:
        """
        Gets all arriving trains from a specified station

        Args:
            station (str): The ID of the station
        """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                s.location AS city,
                s.`name` AS station_name,
                r.start_time,
                ADDTIME(
                    r.start_time,
                SEC_TO_TIME( r.duration * 60 )) AS arrival_time,
                r.end_platform 
            FROM
                route r
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            WHERE
                r.`destination` = %s 
            ORDER BY
                arrival_time,
                r.start_time DESC;
            """,
            (station,)
        )

        timetable = []
        for row in cur.fetchall():
            timetable.append(Timetable(row[0], row[1], row[2], row[3], row[4]))
        
        cur.close()
        return timetable
    
    def get_routes_by_train(self, train_id: int) -> list[Route]:
        """
        Gets all routes travelled from a specified train

        Args:
            train_id (int): The train ID of the routes
        """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                s.location AS `start`,
                s.`name` AS start_station,
                e.location AS city,
                e.`name` AS end_station,
                r.start_time,
                ADDTIME(
                    r.start_time,
                SEC_TO_TIME( r.duration * 60 )) AS arrival_time
            FROM
                route r
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            WHERE
                r.train_id = CAST(%s AS UNSIGNED)
            ORDER BY
                r.start_time,
                arrival_time ASC;
            """,
            (train_id,)
        )

        routes = []
        for row in cur.fetchall():
            routes.append(Route(row[0], row[1], row[2], row[3], row[4], row[5]))
        
        cur.close()
        return routes
    
    def get_all_routes(self) -> list[Route]:
        """ Returns a list of all routes. """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                s.location AS `start`,
                s.`name` AS start_station,
                e.location AS city,
                e.`name` AS end_station,
                r.start_time,
                ADDTIME(
                    r.start_time,
                SEC_TO_TIME( r.duration * 60 )) AS arrival_time
            FROM
                route r
                INNER JOIN start_station s ON s.station_id = r.`start`
                INNER JOIN end_station e ON e.station_id = r.destination 
            ORDER BY
                r.start_time,
                arrival_time ASC;
            """
        )

        routes = []
        for row in cur.fetchall():
            routes.append(Route(row[0], row[1], row[2], row[3], row[4], row[5]))
        
        cur.close()
        return routes
    
    def get_all_trains(self) -> list[Train]:
        """ Returns a list of all active trains. """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                tr.*,
                AVG( r.service_speed ) AS average_service_speed,
                SEC_TO_TIME( SUM( r.duration ) * 60 ) AS total_duration 
            FROM
                train tr
                INNER JOIN route r ON r.train_id = tr.train_id 
                AND r.num_stops = 0 
            GROUP BY
                tr.train_id 
            ORDER BY
                total_duration DESC;
            """
        )

        trains = []
        for row in cur.fetchall():
            trains.append(Train(row[0], row[1], row[2], row[3], row[4], 
                                row[5], row[6], row[7]))
        
        cur.close()
        return trains
    
    def get_train_by_id(self, train_id: int) -> list[Train]:
        """ 
        Returns the attributes of a train specified by train ID.

        Args:
            train_id (int): The ID of a train
        """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                tr.*,
                AVG( r.service_speed ) AS average_service_speed,
                SEC_TO_TIME( SUM( r.duration ) * 60 ) AS total_duration 
            FROM
                train tr
                INNER JOIN route r ON r.train_id = tr.train_id 
                AND r.num_stops = 0
            WHERE tr.train_id = CAST(%s AS UNSIGNED)
            GROUP BY
                tr.train_id 
            ORDER BY
                total_duration DESC;
            """,
            (train_id,)
        )

        trains = []
        for row in cur.fetchall():
            trains.append(Train(row[0], row[1], row[2], row[3], row[4], 
                                row[5], row[6], row[7]))
        
        cur.close()
        return trains
    
    def get_train_by_station(self, station_id: str) -> list[Train]:
        """ 
        Returns the attributes of all train(s) specified by station ID.

        Args:
            station_id (int): The ID of a station that the train passes through
        """

        if not self.connection:
            raise Exception('No connection established to intermodal database')
        cur = self.connection.cursor()
        cur.execute(
            """
            SELECT
                tr.*,
                AVG( r.service_speed ) AS average_service_speed,
                SEC_TO_TIME( SUM( r.duration ) * 60 ) AS total_duration
            FROM
                train tr
                INNER JOIN route r ON r.train_id = tr.train_id 
                AND r.num_stops = 0 
            WHERE
                r.`start` = %s
                OR r.destination = %s
            GROUP BY
                tr.train_id 
            ORDER BY
                total_duration DESC;
            """,
            (station_id, station_id)
        )

        trains = []
        for row in cur.fetchall():
            trains.append(Train(row[0], row[1], row[2], row[3], row[4], 
                                row[5], row[6], row[7]))
        
        cur.close()
        return trains