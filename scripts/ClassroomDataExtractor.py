
import numpy as np
import pandas as pd

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

    def exportTableToGoogleSheets(
            self,
            google_sheet_link: str = "https://docs.google.com/spreadsheets/d/1BagQlqKf07k6ByUVKWyFsetI2U2syr_X1q1Hf4HjyUE/edit?gid=0#gid=0"
        ) -> str | bool:
        """
        HEADER STRUCTURE:
            [ Nome,  atividade 1,  atividade 2 ...  atividade N,  total ]
        """

        if len(self.TABLE.index) == 0 or len(self.TABLE.columns) == 0:
            return "unable to export"

        sheet = connectToSpreadsheet(google_sheet_link)

        format_table(row_num=len(list(self.TABLE.index.array))+1, col_num=len(list(self.TABLE.columns.array)), sheet=sheet)

        table_cleaned = self.TABLE.fillna(0)
        formatted_table = [list(table_cleaned.columns.array)] + [list(table_cleaned.loc[row]) for row in list(table_cleaned.index)]

        print(formatted_table)

        insertData(sheet.get_worksheet(0), formatted_table)

        return True

grade_table = GradeTablePandas()

# if __name__ == "__main__":
#
#     print(grade_table.TABLE)
#
#     foo = [("athos",10),("athos2", 20),("athos3", 300)]
#     grade_table.loadActivityGrades("foo atv", foo)
#
#     foo = [("athos",10),("athos2", 20),("athos3", 300),("athos4", 350)]
#     grade_table.loadActivityGrades("foo atv 2", foo)
#
#     print("\n\nagain.\n\n")
#
#     foo = [("athos4", 350)]
#     grade_table.loadActivityGrades("foo atv", foo)
#
#     print(list(grade_table.TABLE.index))
#     print("ATHOS4" in list(grade_table.TABLE.index))
#
#     # print("\n\n\n")
#     # print(grade_table.TABLE)
