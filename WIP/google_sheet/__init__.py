from __future__ import print_function

import os.path
import sys
from typing import Any, Dict, List, Union

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

sys.path = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))] + sys.path
from google_sheet.types import (
    DateTimeRenderOption,
    Dimension,
    InsertDataOption,
    ValueInputOption,
    ValueRenderOption,
    camel_to_snake,
    snake_to_camel,
)

# If modifying these scopes, delete the file token.json.
DIR = os.path.dirname(__file__)
TOKEN = os.path.join(DIR, "token.json")
CREDENTIALS = os.path.join(DIR, "credentials.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class SpreadSheets:
    """
    https://github.com/googleworkspace/python-samples/blob/master/sheets/snippets/spreadsheet_snippets.py
    """

    _query_values = {
        "dateTimeRenderOption": DateTimeRenderOption,
        "includeValuesInResponse": [True, False],
        "insertDataOption": InsertDataOption,
        "majorDimension": Dimension,
        # "ranges": List[str],
        "responseDateTimeRenderOption": DateTimeRenderOption,
        "responseValueRenderOption": ValueRenderOption,
        "valueInputOption": ValueInputOption,
        "valueRenderOption": ValueRenderOption,
    }
    _default_query = {
        "dateTimeRenderOption": "SERIAL_NUMBER",
        "includeValuesInResponse": False,
        "insertDataOption": "OVERWRITE",
        "majorDimension": "ROWS",
        "responseDateTimeRenderOption": "SERIAL_NUMBER",
        "responseValueRenderOption": "FORMATTED_VALUE",
        "valueInputOption": "RAW",
        "valueRenderOption": "FORMATTED_VALUE",
    }

    def __init__(self, spreadsheet_id: str = None, **kwargs) -> None:
        """
        Args:
            spreadsheet_id: `str`
                The ID of the spreadsheet to query.

            ranges: `List[str]`
                The A1 notation of the values to retrieve.

            major_dimension: `Dimension`, default "ROWS"
                The major dimension that results should use. For example, if the
                spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting
                range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
                whereas requesting range=A1:B2,majorDimension=COLUMNS will
                return [[1,3],[2,4]].
                Options: "DIMENSION_UNSPECIFIED", "ROWS", "COLUMNS".
                https://developers.google.com/sheets/api/reference/rest/v4/Dimension


            value_input_option: `ValueInputOption`, default "RAW"
                Determines how input data should be interpreted.
                Options: "INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption

            insert_data_option: `InsertDataOption`, default "OVERWRITE"
                Determines how existing data is changed when new data is input.
                Options: "OVERWRITE", "INSERT_ROWS".
                https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#insertdataoption

            include_values_in_response: `bool`, default False
                Determines if the update response should include the values of the
                cells that were appended. By default, responses do not include the
                updated values.

            value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
            response_value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
            response_date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption
        Examples:
            >>> from google_sheet import SpreadSheets
            >>> spreadsheet_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            >>> spreadsheet = SpreadSheets(spreadsheet_id)
        For more information, see:
                https://developers.google.com/sheets/api/guides/create
        """
        creds = self.auth()
        service = build("sheets", "v4", credentials=creds)
        self.spreadsheet = service.spreadsheets()
        self.query = {"spreadsheet_id": spreadsheet_id, **self._default_query}
        self.valid_query(kwargs)

    def auth(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN):
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(CREDENTIALS, "w") as token:
                token.write(creds.to_json())
        return creds

    @property
    def id(self):
        """Returns the spreadsheet id."""
        return self.query["spreadsheet_id"]

    @id.setter
    def id(self, spreadsheet_id: str):
        """Sets the spreadsheet id."""
        self.query["spreadsheet_id"] = spreadsheet_id

    @id.deleter
    def id(self):
        """Deletes the spreadsheet id."""
        del self.query["spreadsheet_id"]

    def valid_query(self, kwargs: dict = {}, valid_keys=None):
        """
        Args:
            kwargs: `Dict`
                The query parameters.

            valid_keys: `List[str]`
                The valid keys.
        """
        if valid_keys is None:
            valid_keys = tuple(self._query_values.keys())
        for k, v in kwargs.items():
            if snake_to_camel(k) not in valid_keys:
                raise KeyError(f"{k} is not a valid query parameter.")
            if v in self._query_values[snake_to_camel(k)]:
                self.query[k] = v
            else:
                raise ValueError(f"{v} is not a valid value for {k}")

        self.query.update(camel_to_snake(kwargs))
        query = {k: v for k, v in snake_to_camel(self.query).items() if k in valid_keys}
        return query

    def values(self):
        """
        https://developers.google.com/sheets/api/guides/values
        """
        return self.spreadsheet.values()

    def get_values(self, range: str, **kwargs):
        """
        Args:
            range: `str`
                The A1 notation of the values to retrieve.

            spreadsheet_id: `str`
                The ID of the spreadsheet to query.

            major_dimension: `Dimension`, default "ROWS"
                The major dimension that results should use. For example, if the
                spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting
                range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
                whereas requesting range=A1:B2,majorDimension=COLUMNS will
                return [[1,3],[2,4]].
                Options: "DIMENSION_UNSPECIFIED", "ROWS", "COLUMNS".
                https://developers.google.com/sheets/api/reference/rest/v4/Dimension

            value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption

        Example:
            >>> range = "Sheet1!A1:B2"
            >>> values = spreadsheet.get_values(range)
            >>> values
            [[1, 2], [3, 4]]
            >>> values = spreadsheet.get_values(range, major_dimension="COLUMNS")
            >>> values
            [[1, 3], [2, 4]]

        For more information, see:
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
        """
        valid_keys = {
            "spreadsheetId",
            "majorDimension",
            "valueRenderOption",
            "dateTimeRenderOption",
        }
        query = self.valid_query(kwargs, valid_keys)
        query["range"] = range
        response = self.values().get(**query).execute()
        values = response.get("values", [])
        return values

    def get_batch_values(self, ranges: List[str], **kwargs):
        """
        Args:
            ranges: `List[str]`
                The A1 notation of the values to retrieve.

            spreadsheet_id: `str`
                The ID of the spreadsheet to query.

            major_dimension: `Dimension`, default "ROWS"
                The major dimension that results should use. For example, if the
                spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting
                range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
                whereas requesting range=A1:B2,majorDimension=COLUMNS will
                return [[1,3],[2,4]].
                Options: "DIMENSION_UNSPECIFIED", "ROWS", "COLUMNS".
                https://developers.google.com/sheets/api/reference/rest/v4/Dimension

            value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption

        Example:
            >>> ranges = ["A1:B2", "C1:D2"]
            >>> values = spreadsheet.get_batch_values(ranges)
            >>> values
            [
                [[1, 2], [3, 4]], # A1:B2
                [[5, 6], [7, 8]]  # C1:D2
            ]
            >>> values = spreadsheet.get_batch_values(ranges, major_dimension="COLUMNS")
            >>> values
            [
                [[1, 3], [2, 4]], # A1:B2
                [[5, 7], [6, 8]]  # C1:D2
            ]

        For more information, see:
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
        """
        valid_keys = {
            "spreadsheetId",
            "ranges",
            "majorDimension",
            "valueRenderOption",
            "dateTimeRenderOption",
        }
        query = self.valid_query(kwargs, valid_keys)
        query["ranges"] = ranges
        response = self.values().batchGet(**query).execute()
        values = response.get("valueRanges", [])
        return values

    def append_values(self, range: str, values: List[List[Any]], **kwargs):
        """
        Args:
            range: `str`
                A range on a sheet.

            values: `List[List[Any]]`
                The values to append.

            spreadsheet_id: `str`
                The ID of the spreadsheet to update.

            value_input_option: `ValueInputOption`, default "RAW"
                Determines how input data should be interpreted.
                Options: "INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption

            insert_data_option: `InsertDataOption`, default "OVERWRITE"
                Determines how existing data is changed when new data is input.
                Options: "OVERWRITE", "INSERT_ROWS".
                https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#insertdataoption

            include_values_in_response: `bool`, default False
                Determines if the update response should include the values of the
                cells that were appended. By default, responses do not include the
                updated values.

            response_value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            response_date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption

        Example:
            >>> range = "Sheet1!A1:B2"
            >>> values = [[1, 2], [3, 4]]
            >>> response = spreadsheet.append_values(range, values)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "tableRange": "Sheet1!A1:B2"
                "updates": {
                    "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "updatedRange": "Sheet1!A1:B2",
                    "updatedRows": 2,
                    "updatedColumns": 2,
                    "updatedCells": 4
                },
            }
            >>> response = spreadsheet.append_values(range, values, include_values_in_response=True)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "tableRange": "Sheet1!A1:B2",
                "updates": {
                    "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "updatedRange": "Sheet1!A1:B2",
                    "updatedRows": 2,
                    "updatedColumns": 2,
                    "updatedCells": 4,
                    "updatedData": {
                        "range": "Sheet1!A1:B2",
                        "majorDimension": "ROWS",
                        "values": [[1, 2], [3, 4]]
                    }
                }
            }

        For more information, see:
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
        """
        valid_keys = {
            "spreadsheetId",
            "valueInputOption",
            "insertDataOption",
            "includeValuesInResponse",
            "responseValueRenderOption",
            "responseDateTimeRenderOption",
        }
        query = self.valid_query(kwargs, valid_keys)
        query["range"] = range
        query["body"] = {"values": values}
        response = self.values().append(**query).execute()
        return response.get("updates", {})

    def set_values(self, range: str, values: List[List[Any]], **kwargs):
        """
        Args:
            range: `str`
                A range on a sheet.

            values: `List[List[Any]]`
                A list of values to update.

            spreadsheet_id: `str`
                The ID of the spreadsheet to update.

            value_input_option: `ValueInputOption`, default "RAW"
                Determines how input data should be interpreted.
                Options: "INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption

            include_values_in_response: `bool`, default False
                Determines if the update response should include the values of the
                cells that were updated. By default, responses do not include the
                updated values.

            response_value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            response_date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

        Example:
            >>> range = "Sheet1!A1:B2"
            >>> values = [[1, 2], [3, 4]]
            >>> response = spreadsheet.set_values(range, values)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "updatedRange": "Sheet1!A1:B2",
                "updatedRows": 2,
                "updatedColumns": 2,
                "updatedCells": 4
            }
            >>> response = spreadsheet.set_values(range, values, include_values_in_response=True)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "updatedRange": "Sheet1!A1:B2",
                "updatedRows": 2,
                "updatedColumns": 2,
                "updatedCells": 4,
                "updatedData": {
                    "range": "Sheet1!A1:B2",
                    "majorDimension": "ROWS",
                    "values": [[1, 2], [3, 4]]
                }
            }

        For more information, see:
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
        """
        valid_keys = {
            "spreadsheetId",
            "valueInputOption",
            "includeValuesInResponse",
            "responseValueRenderOption",
            "responseDateTimeRenderOption",
        }
        query = self.valid_query(kwargs, valid_keys)
        query["range"] = range
        query["body"] = {"values": values}
        response = self.values().update(**query).execute()
        return response

    def set_batch_values(self, rows: List[Dict[str, Union[str, List]]], **kwargs):
        """
        Args:
            body: `Dict[str, Any]`
                A dictionary of the request body.

            spreadsheet_id: `str`
                The ID of the spreadsheet to update.

            value_input_option: `ValueInputOption`, default "RAW"
                Determines how input data should be interpreted.
                Options: "INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption

            include_values_in_response: `bool`, default False
                Determines if the update response should include the values of the
                cells that were updated. By default, responses do not include the
                updated values.

            response_value_render_option: `ValueRenderOption`, default "FORMATTED_VALUE"
                Determines how values in the response should be rendered.
                Options: "FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

            response_date_time_render_option: `DateTimeRenderOption`, default "SERIAL_NUMBER"
                How dates, times, and durations should be represented in the output.
                This is ignored if value_render_option is FORMATTED_VALUE.
                Options: "SERIAL_NUMBER", "FORMATTED_STRING".
                https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

        Example:
            >>> rows = [
            ...     { "range": "Sheet1!A1:B2", "values": [[1, 2], [3, 4]] },
            ...     { "range": "Sheet1!C1:D2", "values": [[5, 6], [7, 8]] }
            ... ]
            >>> response = spreadsheet.set_batch_values(rows, include_values_in_response=True)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "responses": [ response1, response2, ... ] # List of responses(like set_values) for each row in rows list above
                "totalUpdatedCells": 8,
                "totalUpdatedColumns": 4,
                "totalUpdatedRows": 2,
                "totalUpdatedSheets": 1
            }

        For more information, see:
            https://developers.google.com/sheets/api/guides/batchupdate
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate
        """
        valid_keys = {
            "spreadsheetId",
            "valueInputOption",
            "includeValuesInResponse",
            "responseValueRenderOption",
            "responseDateTimeRenderOption",
        }
        query = self.valid_query(kwargs, valid_keys)
        spreadsheet_id = query.pop("spreadsheetId")
        body = {"data": rows, **query}
        response = (
            self.values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        )
        return response

    def clear_values(self, range: str, **kwargs):
        """
        Args:
            range: `str`
                The A1 notation of the values to clear.

            spreadsheet_id: `str`
                The ID of the spreadsheet to update.

        Example:
            >>> range = "Sheet1!A1:B2"
            >>> response = spreadsheet.clear_values(range)
            >>> response
            {
                "spreadsheetId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "clearedRange": "Sheet1!A1:B2"
            }

        For more information, see:
            https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear
        """
        valid_keys = {"spreadsheetId"}
        query = self.valid_query(kwargs, valid_keys)
        query["range"] = range
        response = self.values().clear(**query).execute()
        return response


if __name__ == "__main__":
    import time

    spreadsheet = SpreadSheets(spreadsheet_id=os.environ["SPREADSHEET_ID"])
    print(spreadsheet.get_values("sheet!A1:H"))
    print(
        spreadsheet.set_values(
            "sheet!C2:F2", [[time.time(), None, 3, "jun.hyeok@g.skku.edu"]]
        )
    )
