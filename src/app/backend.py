'Backend code for choir attendance project'


import configparser
import datetime


import pygsheets


_CONFIG = configparser.ConfigParser()
_CONFIG.read('config.ini')
SHEET_NAME = _CONFIG['DEFAULT']['Sheet']


def _get_sheet():
    'Load google sheet named {SHEET_NAME}'
    google_login = pygsheets.authorize(service_file='client_secret.json')
    sheet = google_login.open(SHEET_NAME)
    return sheet.sheet1


def read_names():
    'Read all the names present in the sheet'
    sheet = _get_sheet()
    name_cells = sheet.get_values(start='B2', end='B150', returnas='cells')
    names = [name_cell[0].value for name_cell in name_cells]
    return names


def update_attendance(attendance):
    'Write the attendance log'
    sheet = _get_sheet()
    # Get current date
    date = datetime.date.today().strftime('%d-%B-%Y')
    # Get table width
    date_cells_with_empty = sheet.get_values(
        start='A1',
        end='ZZ1',
        returnas='cells')
    date_cells = [cell for cell in date_cells_with_empty[0] if cell.value]
    last_column = date_cells[-1].col

    attendance = ['kohal' if there else 'puudus' for there in attendance]
    attendance.insert(0, date)
    sheet.insert_cols(col=last_column, values=attendance)


def update_names(names):
    'Write all names to table'
    sheet = _get_sheet()
    names = [[name] for name in names]
    sheet.update_values('A1:A150', names)
