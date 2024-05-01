import os

from db import Reservation, Timetable, DBManager
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

db_name = 'intermodal-train-db'

def display_reservations(reservations: list[Reservation], title: str):
        """
        Display a list of all reservation from a selected query.

        Args:
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

def main():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    
    db_manager = DBManager(host, db_name, user, password)
    db_manager.connect()

    while True:
        which = Prompt.ask(
            "Access [bold]\[r][/]eservation details, [bold]\[t][/]imetable information, or e[bold]\[x][/]it.",
            choices=['r', 't', 'x'],
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
                which_res = Prompt.ask(
                "Access [bold]\[d][/]eparting trains, [bold]\[a][/]arriving trains, or go [bold]\[b][/]ack.",
                choices=['d', 'a', 'b'],
                )

                if which_res == 'b':
                    break
                elif which_res == 'd':
                    station_id = Prompt.ask("Enter station ID")
                    departing = db_manager.get_departures(station_id)
                    display_timetable(departing, f'Departures from {station_id}')
                elif which_res == 'a':
                    station_id = Prompt.ask("Enter station ID")
                    arriving = db_manager.get_arrivals(station_id)
                    display_timetable(arriving, f'Arrivals for {station_id}')
    
if __name__ == '__main__':
    main()