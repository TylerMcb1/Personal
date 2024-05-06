import os
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from db import DBManager
from objects import Reservation, Timetable, Route, Train

db_name = 'intermodal-train-db'

def display_reservations(reservations: list[Reservation], title: str):
    """
    Display a list of all reservation from a selected query.

    Args:
        reservations: The list of reservations to display
        title: The title of the table
    """
    console = Console()

    table = Table(show_header=True, header_style="bold green", width=120, title=title)

    table.add_column('Reservation ID')
    table.add_column('First Name')
    table.add_column('Last Name')
    table.add_column('Start City')
    table.add_column('Desination City')
    table.add_column('Departure Time')
    table.add_column('Duration')

    for res in reservations:
        table.add_row(
            str(res.res_id),
            str(res.first_name),
            str(res.last_name),
            str(res.start),
            str(res.dest),
            str(res.start_time),
            str(res.duration)
        )

    console.print(table)

def display_timetable(timetable: list[Timetable], title: str):
    """
    Display a list of all timetable entries from a selected query.

    Args:
        timetable: The list of arrivals/departures to display
        title: The title of the table
    """
    console = Console()

    table = Table(show_header=True, header_style="bold green", title=title)

    table.add_column('City')
    table.add_column('Station Name')
    table.add_column('Start Time')
    table.add_column('Arrival Time')
    table.add_column('Platform')

    for entry in timetable:
        table.add_row(
            str(entry.city),
            str(entry.station_name),
            str(entry.start_time),
            str(entry.arrival_time),
            str(entry.num_stops)
        )

    console.print(table)

def display_routes(routes: list[Route], title: str):
    """
    Display a list of all routes from a selected query.

    Args:
        routes: The list of routes to display
        title: The title of the table
    """
    console = Console()

    table = Table(show_header=True, header_style="bold green", width=120, title=title)

    table.add_column('Start')
    table.add_column('Departing Station')
    table.add_column('Destination')
    table.add_column('Arriving Station')
    table.add_column('Departure Time')
    table.add_column('Arrival Time')

    for r in routes:
        table.add_row(
            str(r.start),
            str(r.s_station),
            str(r.destination),
            str(r.e_station),
            str(r.start_time),
            str(r.arrival_time)
        )

    console.print(table)

def display_trains(trains: list[Train], title: str):
    """
    Display a list of all trains from a selected query.

    Args:
        trains: The list of trains to display
        title: The title of the table
    """
    console = Console()

    table = Table(show_header=True, header_style="bold green", width=120, title=title)

    table.add_column('Train ID')
    table.add_column('Make')
    table.add_column('Model')
    table.add_column('Year')
    table.add_column('Max Speed')
    table.add_column('Capacity')
    table.add_column('Average Speed')
    table.add_column('Total Duration')

    for r in trains:
        table.add_row(
            str(r.train_id),
            str(r.make),
            str(r.model),
            str(r.year),
            str(r.max_speed),
            str(r.capacity),
            str(r.avg_speed),
            str(r.total_duration)
        )

    console.print(table)

def main():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    
    db_manager = DBManager(host, db_name, user, password)
    db_manager.connect()

    while True:
        which = Prompt.ask(
            "Access [bold]\[r][/]eservation details, [bold]\[t][/]imetable information, route [bold]\[i][/]nformation, train [bold]\[d][/]etails, or e[bold]\[x][/]it.",
            choices=['r', 't', 'i', 'd', 'x'],
        )

        if which == 'x':
            db_manager.disconnect()
            exit()
        elif which == 'r':
            while True:
                which_res = Prompt.ask(
                "Access [bold]\[a][/]ll reservation details, [bold]\[s][/]earch by name, search by [bold]\[r][/]eservation ID, or go [bold]\[b][/]ack.",
                choices=['a', 's', 'r', 'b'],
                )

                if which_res == 'b':
                    break
                elif which_res == 'a':
                    reservations = db_manager.get_all_reservations()
                    display_reservations(reservations, 'All Reservations')
                elif which_res == 's':
                    name = Prompt.ask("Enter name to search by")
                    reservations = db_manager.reservation_search_by_name(name)
                    display_reservations(reservations, f'All Reservations with name: {name}')
                elif which_res == 'r':
                    res_id = Prompt.ask("Enter reservation ID")
                    reservations = db_manager.reservation_search_by_id(res_id)
                    display_reservations(reservations, f'Reservation ID: {res_id}')
        elif which == 't':
            while True:
                which_time = Prompt.ask(
                "Access [bold]\[d][/]eparting trains, [bold]\[a][/]rriving trains, or go [bold]\[b][/]ack.",
                choices=['d', 'a', 'b'],
                )

                if which_time == 'b':
                    break
                elif which_time == 'd':
                    station_id = Prompt.ask("Enter station ID")
                    departing = db_manager.get_departures(station_id)
                    display_timetable(departing, f'Departures from {station_id}')
                elif which_time == 'a':
                    station_id = Prompt.ask("Enter station ID")
                    arriving = db_manager.get_arrivals(station_id)
                    display_timetable(arriving, f'Arrivals for {station_id}')
        elif which == 'i':
            while True:
                which_route = Prompt.ask(
                "Access [bold]\[a][/]ll routes, [bold]\[s][/]earch by train ID, or go [bold]\[b][/]ack.",
                choices=['a', 's', 'b'],
                )

                if which_route == 'b':
                    break
                elif which_route == 'a':
                    routes = db_manager.get_all_routes()
                    display_routes(routes, 'All Routes')
                elif which_route == 's':
                    train_id = Prompt.ask("Enter train ID")
                    routes = db_manager.get_routes_by_train(train_id)
                    display_routes(routes, f'All Routes for Train {train_id}')
        elif which == 'd':
            while True:
                which_train = Prompt.ask(
                "Access [bold]\[a][/]ll trains, Search by [bold]\[t][/]rain ID, Search by [bold]\[s][/]tation, or go [bold]\[b][/]ack.",
                choices=['a', 't', 's', 'b'],
                )

                if which_train == 'b':
                    break
                elif which_train == 'a':
                    trains = db_manager.get_all_trains()
                    display_trains(trains, 'All Active Trains')
                elif which_train == 't':
                    train_id = Prompt.ask("Enter train ID")
                    trains = db_manager.get_train_by_id(train_id)
                    display_trains(trains, f'Train {train_id}')
                elif which_train == 's':
                    station_id = Prompt.ask("Enter station ID")
                    trains = db_manager.get_train_by_station(station_id)
                    display_trains(trains, f'All Trains at Station {station_id}')
    
if __name__ == '__main__':
    main()