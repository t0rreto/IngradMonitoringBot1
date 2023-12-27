import config
import pygsheets
from pygsheets.worksheet import Worksheet


class TableConnector:
    connector = pygsheets.authorize(service_file="auth-google.json")

    def __init__(self):
        self.worksheet: Worksheet = self.connector.open_by_key(config.SHEET_ID)[1]

    def get_free_id(self):
        worksheet_values = self.worksheet.get_all_values()
        first_empty_row_id = None
        for idx, row in enumerate(worksheet_values):
            if not any(row):
                first_empty_row_id = idx + 1
                break
        return first_empty_row_id

    def insert_row(self, data):
        free_row_id = self.get_free_id()
        self.worksheet.update_values(f"A{free_row_id}", data)



