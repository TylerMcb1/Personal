import pytest
import os

from db import DBManager
from objects import Reservation, Timetable, Route, Train

db_name = 'intermodal-train-db'

# Set up pytest fixture for database connection
@pytest.fixture
def db_connection():
    db_connection = DBManager(host=os.getenv('DB_HOST'),
        database=db_name,
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'))
    db_connection.connect()
    yield db_connection
    db_connection.disconnect()

# Test reservation queries

def test_get_all_reservations(db_connection):
    reservations = db_connection.get_all_reservations()
    assert len(reservations) == 200
    assert all([isinstance(res, Reservation) for res in reservations])

@pytest.mark.parametrize("name, expected",
    [("bertha", 5), ("paige", 4), ("wilson", 3)])

def test_res_by_name(db_connection, name, expected):
    reservations = db_connection.reservation_search_by_name(name)
    assert len(reservations) == expected
    assert all([isinstance(res, Reservation) for res in reservations])
    assert all([type(res.first_name) == str for res in reservations])
    assert all([type(res.last_name) == str for res in reservations])
    assert all([name in res.first_name.lower() for res in reservations])

@pytest.mark.parametrize("id, first, last, expected",
    [("4FDC7D09", "Cathy", "Manning", 1), 
     ("B32D5D3C", "Cecelia", "Mendez", 1), 
     ("65CF8232", "Joyce", "Stevens", 1)])

def test_res_by_id(db_connection, id, first, last, expected):
    reservations = db_connection.reservation_search_by_id(id)
    assert len(reservations) == expected
    assert all([isinstance(res, Reservation) for res in reservations])
    assert all([res.first_name == first for res in reservations])
    assert all([res.last_name == last for res in reservations])

# Test arrival and departure queries

@pytest.mark.parametrize("station, expected",
    [("ST001", 11), ("ST002", 6), ("ST003", 6), 
     ("ST004", 7) , ("ST005", 6), ("ST006", 4)])

def test_get_departures(db_connection, station, expected):
    departures = db_connection.get_departures(station)
    assert len(departures) == expected
    assert all([isinstance(dep, Timetable) for dep in departures])
    assert all([type(dep.city) == str for dep in departures])

@pytest.mark.parametrize("station, expected",
    [("ST001", 11), ("ST002", 6), ("ST003", 6), 
     ("ST004", 7) , ("ST005", 6), ("ST006", 4)])

def test_get_arrivals(db_connection, station, expected):
    arrivals = db_connection.get_arrivals(station)
    assert len(arrivals) == expected
    assert all([isinstance(arr, Timetable) for arr in arrivals])
    assert all([type(arr.city) == str for arr in arrivals])

# Test route route queries

def test_get_all_routes(db_connection):
    routes = db_connection.get_all_routes()
    assert len(routes) == 40
    assert all([isinstance(route, Route) for route in routes])
    assert all([type(route.start) == str for route in routes])
    assert all([type(route.destination) == str for route in routes])

@pytest.mark.parametrize("train, expected",
    [(1, 6), (3, 6), (6, 1), (8, 6) , (10, 1), (13, 2)])

def test_get_routes_by_train(db_connection, train, expected):
    routes = db_connection.get_routes_by_train(train)
    assert len(routes) == expected
    assert all([isinstance(route, Route) for route in routes])
    assert all([type(route.start) == str for route in routes])
    assert all([type(route.destination) == str for route in routes])

# Test train queries

def test_get_all_trains(db_connection):
    trains = db_connection.get_all_trains()
    assert len(trains) == 13
    assert all([isinstance(tr, Train) for tr in trains])
    assert all([type(tr.make) == str for tr in trains])
    assert all([type(tr.model) == str for tr in trains])

@pytest.mark.parametrize("id, make, model, expected",
    [(2, "GE", "Genesis P42DC", 1), 
     (4, "Siemens", "Sprinter ACL-42", 1), 
     (5, "Siemens", "Sprinter ACL-42", 1), 
     (7, "GE", "Genesis P42DC", 1) ,
     (9, "Siemens", "Sprinter ACL-42", 1), 
     (12, "Siemens", "Sprinter ACL-42", 1)])

def test_get_train_by_id(db_connection, id, make, model, expected):
    trains = db_connection.get_train_by_id(id)
    assert len(trains) == expected
    assert all([isinstance(tr, Train) for tr in trains])
    assert all([tr.make == make for tr in trains])
    assert all([tr.model == model for tr in trains])

@pytest.mark.parametrize("station, expected",
    [("ST001", 6), ("ST002", 3), ("ST003", 5), 
     ("ST004", 5) , ("ST005", 5), ("ST006", 7)])

def test_get_train_by_station(db_connection, station, expected):
    trains = db_connection.get_train_by_station(station)
    assert len(trains) == expected
    assert all([isinstance(tr, Train) for tr in trains])
    assert all([type(tr.make) == str for tr in trains])
    assert all([type(tr.model) == str for tr in trains])