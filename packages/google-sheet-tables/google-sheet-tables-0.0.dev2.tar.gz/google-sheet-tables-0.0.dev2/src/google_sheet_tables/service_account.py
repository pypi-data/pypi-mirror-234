from string import ascii_uppercase

from gspread import service_account, Worksheet


class ServiceAccount:
    def __init__(self, file: str, sheet_name: str) -> None:
        self._path = file
        self._name = sheet_name
        self._account = service_account(filename=self._path)
        self._worksheet = self._account.open(self._name).sheet1
        self._column_names: tuple[str] = tuple()

    def create_data_table(self, column_names: tuple[str]) -> None:
        columns = len(column_names)
        letters = tuple(ascii_uppercase)

        if columns > 26:
            raise ValueError("Количество колонок не может превышать 26.")

        self._column_names = column_names

        self._worksheet.batch_update(
            [
                {
                    "range": f"A1:{letters[columns - 1]}1",
                    "values": [[value for value in column_names]]
                }
            ]
        )

    def _get_last_row_id(self) -> int:
        return len(self._worksheet.get_all_values())

    def insert_row(self, *columns) -> None:
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
