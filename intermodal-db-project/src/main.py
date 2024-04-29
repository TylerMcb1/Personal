import os

from db import Reservation, Timetable, DBManager
from rich.console import Console
from rich.table import Table

db_name = 'intermodal train db'

def display_reservations(reservations: list[Reservation], title: str):
        """
        Display a list of all reservation from a selected query.

        Args:
            title: The title of the table
        """
        console = Console()

        table = Table(show_header=True, header_style="bold green", title=title)

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
        table.add_column('Number of Stops')
    
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

    if db_manager.connection:
        db_manager.disconnect()
        print("Connection success")
    else:
        print("Connection failed")
    
if __name__ == '__main__':
    main()