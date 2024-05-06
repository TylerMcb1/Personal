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

class Route:
    def __init__(self, start: str, s_station: str, destination: str, 
                 e_station, start_time: str, arrival_time: str):
        """
        Initialize a Route object.

        Parameters:
            start (str): The name of the city the train is departing from
            s_station (str): The name of the station train is departing from
            destination (str): The name of the city the train is arriving at
            e_station (str): The name of the station the city is arriving at
            start_time (str): The start time of the trip
            arrival_time (str): The arrival time of the trip
        """
        self.start = start
        self.s_station = s_station
        self.destination = destination
        self.e_station = e_station
        self.start_time = start_time
        self.arrival_time = arrival_time
    
    def __repr__(self) -> str:
        return f"Route({self.start} {self.destination})"

class Train:
    def __init__(self, train_id: int, make: str, model: str, year: int,
                 max_speed: int, capacity: int, avg_speed: float, 
                 total_duration: str):
        """
        Initialize a Train object.

        Parameters:
            train_id (int): The ID of a train
            make (str): The make of the train
            model (str): The model of the train
            year (int): The year of manufacturing of the train
            max_speed (int): The max speed of the train
            capacity (int): The capacity of the train
            avg_speed (float): The average service speed of the train
            total_duration (str): The total duration of travel of the train
        """
        self.train_id = train_id
        self.make = make
        self.model = model
        self.year = year
        self.max_speed = max_speed
        self.capacity = capacity
        self.avg_speed = avg_speed
        self.total_duration = total_duration
        
    def __repr__(self) -> str:
        return f"Train({self.train_id})"