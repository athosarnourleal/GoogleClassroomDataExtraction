
import gspread
from pathlib import Path

from google.oauth2.service_account import Credentials

from dotenv import load_dotenv
from gspread.utils import ValueInputOption

load_dotenv()

def connectToSpreadsheet(spreadsheet_link: str):

    # client setup
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    credentials_path = Path(__file__).parent.parent / "google credentials" / "credentials_service_googleSheets.json"

    if not credentials_path.exists():
        raise "google sheets service account credentials does not exist."

    creds = Credentials.from_service_account_file(str(credentials_path), scopes= scopes)
    # creds = Credentials.from_authorized_user_file(str(credentials_path))
    client = gspread.authorize(creds)

    # accessing worksheet
    sheet = client.open_by_url(spreadsheet_link) # access token ur

    return sheet

def format_table(
        row_num: int,
        col_num: int,
        sheet: gspread.spreadsheet.Spreadsheet,
        worksheet: gspread.spreadsheet.Worksheet
    ) -> None:

    position_range_header = gspread.utils.rowcol_to_a1(row=1, col=1) + ":" + gspread.utils.rowcol_to_a1(row=1, col=col_num)

    # format header
    worksheet.format(position_range_header,
    {
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "backgroundColor": {
                "red": float(26/255),
                "green": float(26/255),
                "blue": float(50/255)
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "fontSize": 9,
                "bold": True
            }
        }
    )

    position_range = gspread.utils.rowcol_to_a1(row= 2  , col=1) + ":" + gspread.utils.rowcol_to_a1(row=row_num, col=col_num)

    # format rows
    worksheet.format(position_range,
    {
            "verticalAlignment": "MIDDLE",
            "horizontalAlignment": "CENTER",
            "backgroundColor": {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
            },
            "textFormat": {
                "foregroundColor": {
                    "red": 0.0,
                    "green": 0.0,
                    "blue": 0.0
                },
                "fontSize": 9,
                "bold": False
            }
        }
    )

    # resize header row
    header_size_change_request = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "ROWS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 50
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    sheet.batch_update(header_size_change_request)

    # resize other rows
    row_size_change_request = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "ROWS",
                        "startIndex": 1,
                        "endIndex": row_num
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

    # resize the initial columns
    col_size_change_request_names = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                    },
                    "properties": {
                        "pixelSize": 300
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    sheet.batch_update(col_size_change_request_names)

    # resize the activity cols
    col_size_change_request_activities = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": 1,
                        "endIndex": col_num
                    },
                    "properties": {
                        "pixelSize": 200
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    sheet.batch_update(col_size_change_request_activities)

def insertData(
        worksheet: gspread.worksheet.Worksheet,
        data: list, # 2d array
    ) -> None:
    range_positions = "A1:" + gspread.utils.rowcol_to_a1(len(data), len(data[0]))

    worksheet.update(range_name= range_positions, values= data, value_input_option=ValueInputOption.user_entered)


