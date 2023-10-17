from typing import Literal, Self

from gspread_formatting import CellFormat, Color, Padding, TextFormat

from .client import Client


class Format:
    def __init__(self, client: Client) -> None:
        self._client = client
        self._fields = {
            "textFormat": {}
        }

    def set_background_color(self, red: float, green: float, blue: float) -> Self:
        self._fields["backgroundColor"] = Color(red=red, green=green, blue=blue, alpha=1.0)
        return self

    def set_padding(self, top: float, right: float, bottom: float, left: float) -> Self:
        self._fields["padding"] = Padding(top=top, right=right, bottom=bottom, left=left)
        return self

    def set_horizontal_alignment(self, alignment: Literal["CENTER", "LEFT", "RIGHT"]) -> Self:
        self._fields["horizontalAlignment"] = alignment
        return self

    def set_text_font_size(self, font_size: int) -> Self:
        self._fields["textFormat"]["fontSize"] = font_size
        return self

    def set_text_foreground_color(self, red: float, green: float, blue: float) -> Self:
        self._fields["textFormat"]["foregroundColor"] = Color(red=red, green=green, blue=blue)
        return self

    def get_format(self) -> CellFormat:
        cell_format = CellFormat()
        text_format = TextFormat()

        if background_color := self._fields.get("backgroundColor"):
            cell_format.backgroundColor = background_color

        if padding := self._fields.get("padding"):
            cell_format.padding = padding

        if text_font_size := self._fields["textFormat"].get("fontSize"):
            text_format.fontSize = text_font_size

        if text_foreground_color := self._fields["textFormat"].get("foregroundColor"):
            text_format.foregroundColor = text_foreground_color

        if horizontal_alignment := self._fields.get("horizontalAlignment"):
            cell_format.horizontalAlignment = horizontal_alignment

        cell_format.textFormat = text_format

        return cell_format
