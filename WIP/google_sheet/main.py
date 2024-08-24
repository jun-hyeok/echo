import time
import os
import sys

sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))] + sys.path
from google_sheet import SpreadSheets

# The range of a spreadsheet.
SHEET_RANGE = "sheet!C2:F"


class Booker(SpreadSheets):
    def __init__(self, spreadsheet_id: str, **kwargs):
        """
        Booker.

        Args:
            spreadsheet_id: `str`
        """
        super().__init__(spreadsheet_id, **kwargs)

    def read_current_state(self):
        """
        Read current state.

        Example:
            >>> booker.read_current_state()
        """
        values = self.get_values("current!A1:D")
        return values

    def take_a_seat(self, seat_num: int, email: str):
        """
        Take a seat.

        Args:
            seat_num: `int`
            email: `str`

        Example:
            >>> booker.take_a_seat(1, "example@email.com")
        """
        if self.seat_is_in_use(seat_num):
            return False
        # logging
        start_time = time.time()
        values = [[start_time, None, seat_num, email]]
        self.set_values(SHEET_RANGE, values)
        time.sleep(0.1)
        # state set
        self.set_values(f"current!B{seat_num+1}", [[2]])
        index_column = self.get_values(
            "current!B2:B", value_render_option="UNFORMATTED_VALUE"
        )
        index_column_add_1 = [
            [v] for v in map(lambda i: i[0] + 1 if i else None, index_column)
        ]
        self.set_values(f"current!B2", index_column_add_1)

    def return_a_seat(self, seat_num):
        """
        Return a seat.

        Args:
            seat_num: `int`

        Example:
            >>> booker.return_a_seat(1)
        """
        # logging
        index = self.get_values(
            f"current!B{seat_num+1}", value_render_option="UNFORMATTED_VALUE"
        )[0][0]
        end_time = time.time()
        values = [[end_time]]
        self.set_values(f"sheet!D{index}", values)

        # state clear
        self.clear_values(f"current!B{seat_num+1}")

    def seat_is_in_use(self, seat_num):
        """
        Seat is in use.

        Args:
            seat_num: `int`

        Example:
            >>> booker.seat_is_in_use(1)
            True
        """
        values = self.get_values(
            f"current!B{seat_num+1}", value_render_option="UNFORMATTED_VALUE"
        )
        return values[0][0] if values else None


if __name__ == "__main__":
    t = 3
    booker = Booker(spreadsheet_id=os.environ.get("SPREADSHEET_ID"))
    for i in range(1, 5):
        booker.take_a_seat(i + 2, "jun.hyeok@g.skku.edu")
        time.sleep(t)
    for j in range(1, 5):
        booker.return_a_seat(j)
        # time.sleep(t)
