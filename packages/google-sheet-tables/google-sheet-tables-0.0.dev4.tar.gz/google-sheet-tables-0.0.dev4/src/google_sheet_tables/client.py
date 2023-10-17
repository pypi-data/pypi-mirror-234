from string import ascii_uppercase

from gspread import service_account, Worksheet
from gspread_formatting import format_cell_ranges

from . import Format


class Client:
    def __init__(self, file: str, title: str) -> None:
        self._path = file
        self._name = title
        self._account = service_account(filename=self._path)
        self._worksheet = self._account.open(self._name).sheet1
        self._column_names: tuple = tuple()

    def create_data_table(self, *columns: str) -> None:
        columns_ = len(columns)
        letters = tuple(ascii_uppercase)

        if columns_ > 26:
            raise ValueError(f"Количество колонок не может превышать {len(letters)}.")

        self._column_names = columns

        self._worksheet.batch_update(
            [
                {
                    "range": f"A1:{letters[columns_ - 1]}1",
                    "values": [[value for value in columns]]
                }
            ]
        )

    def _get_last_row_id(self) -> int:
        return len(self._worksheet.get_all_values())

    def insert_row(self, *columns: str) -> None:
        if len(columns) != len(self._column_names):
            raise ValueError(f"Необходимо заполнить все {len(self._column_names)} колонок.")

        letters = tuple(ascii_uppercase)
        row_id = self._get_last_row_id() + 1

        self._worksheet.batch_update(
            [
                {
                    "range": f"A{row_id}:{letters[len(columns) - 1]}{row_id}",
                    "values": [[value for value in columns]]
                }
            ]
        )

    @property
    def worksheet(self) -> Worksheet:
        return self._worksheet

    def format_cells(self, range_: str, cell_format: Format) -> None:
        format_cell_ranges(worksheet=self.worksheet, ranges=[(range_, cell_format.get_format())])
