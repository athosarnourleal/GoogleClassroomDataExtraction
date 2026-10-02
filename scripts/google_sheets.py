import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials

def connectToSpreadsheet(
        sheet_id: str = "1BagQlqKf07k6ByUVKWyFsetI2U2syr_X1q1Hf4HjyUE"
    ):

    # client setup
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(Path(__file__).parent.parent / "credentials.json"), scopes= scopes)
    client = gspread.authorize(creds)

    # accessing worksheet
    sheet = client.open_by_key(sheet_id)

    return sheet

def format_table(
        row_num: int,
        col_num: int,
        sheet: gspread.spreadsheet.Spreadsheet
    ) -> None:

    start_row = 1
    start_col = 0

    position_range = gspread.utils.rowcol_to_a1(row=start_row+1, col=start_col+1) + ":" + gspread.utils.rowcol_to_a1(row=row_num+start_row, col=col_num+start_col)

    spreadsheet.get_worksheet(0).format(position_range,
    {
            "horizontalAlignment": "CENTER",
            "backgroundColor": {
                "red": 1.0,
                "green": 0.95,
                "blue": 0.95
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 0.0,
                    "blue": 0.0
                },
                "fontSize": 9,
                "bold": False
            }
        }
    )

    row_size_change_request = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet.get_worksheet(0).id,
                        "dimension": "ROWS",
                        "startIndex": start_row,
                        "endIndex": row_num+start_row
                    },
                    "properties": {
                        "pixelSize": 30
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }

    sheet.batch_update(row_size_change_request)
    col_size_change_request_names = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet.get_worksheet(0).id,
                        "dimension": "COLUMNS",
                        "startIndex": start_col,
                        "endIndex": start_col+3
                    },
                    "properties": {
                        "pixelSize": 200
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    sheet.batch_update(col_size_change_request_names)

    col_size_change_request_activities = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet.get_worksheet(0).id,
                        "dimension": "COLUMNS",
                        "startIndex": start_col+3,
                        "endIndex": col_num+start_col
                    },
                    "properties": {
                        "pixelSize": 100
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    sheet.batch_update(col_size_change_request_activities)

def insertData():
    # TODO
    pass

spreadsheet = connectToSpreadsheet()
format_table(10, 10, spreadsheet)
