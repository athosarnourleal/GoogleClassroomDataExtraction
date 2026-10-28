from pprint import pprint

import numpy as np
import pandas as pd
import datetime
from gspread.utils import rowcol_to_a1

from scripts.google_sheets_connection import format_table, connectToSpreadsheet, insertData

class GradeTablePandas:

    def __init__(self):
        self.TABLE = pd.DataFrame({})

        # rows --> ALUNOS_NOME
        # columns --> ATIVIDADES_NOME

    @staticmethod
    def isEmpty(cell_value):
        if (
                cell_value is np.nan or
                cell_value == "" or
                cell_value is list and len(cell_value) == 0 or
                cell_value == 0
            ):
            return True

        return False

    def loadActivityGrades(self, activity_name: str, grades_data: list[tuple]):
        activity_name = activity_name.strip().upper()

        for student_name,grade in grades_data:
            student_name = student_name.strip().upper()

            if student_name in list(self.TABLE.index) and activity_name in self.TABLE.columns:
                previous = self.TABLE.at[student_name, activity_name]

                # update value if its worth it
                if self.isEmpty(previous) or not self.isEmpty(grade):
                    self.TABLE.at[student_name, activity_name] = grade
            else:
                # if does not exist then just insert it
                self.TABLE.at[student_name, activity_name] = grade

    def clearTable(self):
        self.TABLE = pd.DataFrame({})

    def exportTableToGoogleSheets(
            self,
            google_sheet_link: str = "https://docs.google.com/spreadsheets/d/1BagQlqKf07k6ByUVKWyFsetI2U2syr_X1q1Hf4HjyUE/edit?gid=0#gid=0",
            sheet_title: str = "NOTAS"
        ) -> str | bool:

        """
        HEADER STRUCTURE:
            [ Nome,  atividade 1,  atividade 2 ...  atividade N,  total ]
        """

        if len(self.TABLE.index) == 0 or len(self.TABLE.columns) == 0:
            return "unable to export"

        sheet = connectToSpreadsheet(google_sheet_link)

        # table_cleaned = self.TABLE.fillna(0)


        row_num = len(list(self.TABLE.index.array)) + 1
        col_num = len(list(self.TABLE.columns.array)) + 3

        table_formatted = (
                [["NOMES DOS ALUNOS", "PONTOS EXTRAS"] + list(self.TABLE.columns.array)+["SOMA ATIVIDADES"]] + # header
                [[row, 0] + list(self.TABLE.loc[row]) + [str(f"=SOMA({rowcol_to_a1(rownum+1, 3)}:{rowcol_to_a1(rownum+1, col_num-1)})")] for rownum, row in enumerate(list(self.TABLE.index),start=1)]
        )

        for row in table_formatted[1:]:
            print(row)

        worksheet_title = sheet_title+"-"+str(datetime.datetime.now().strftime("%d/%m/%Y"))

        # delete previous instances to avoid errors


        if worksheet_title in [ws.title for ws in sheet.worksheets()]:
            # spreadsheet already exists

            filler = None
            if len(sheet.worksheets()) == 1:
                # avoid removing all the worksheets from the project
                filler = sheet.add_worksheet(
                    title="filler",
                    rows=1,
                    cols=1
                )

            sheet.del_worksheet(worksheet=sheet.worksheet(worksheet_title))

            worksheet = sheet.add_worksheet(
                title=worksheet_title,
                rows=row_num,
                cols=col_num
            )

            if filler is not None:
                sheet.del_worksheet(filler)

        else:
            # spreadsheet is now being created

            worksheet = sheet.add_worksheet(
                title=worksheet_title,
                rows=row_num,
                cols=col_num
            )

        format_table(row_num=row_num, col_num=col_num, sheet= sheet, worksheet= worksheet)

        pprint(table_formatted)

        insertData(worksheet, table_formatted)

        return True

grade_table = GradeTablePandas()
