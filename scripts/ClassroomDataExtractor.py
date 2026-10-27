import csv
from pathlib import Path
import numpy as np
import pandas as pd

from scripts.google_sheets_connection import format_table, connectToSpreadsheet, insertData

class GradeTablePandas:

    def __init__(self):
        self.TABLE = pd.DataFrame({"STUDENT NAMES": []})

        # rows --> ALUNOS_NOME
        # columns --> ATIVIDADES_NOME

    def addStudent(self, student_name: str, student_surname: str, student_email: str):
        if student_email in self.TABLE.index:
            return

        student_name = student_name.title().strip() + " " + student_surname.title().strip()
        student_email = student_email.strip()

        self.TABLE.loc[student_email] = pd.Series()
        self.TABLE.at[student_email, "STUDENT NAMES"] = student_name

    def addActivity(self, activity_name: str) -> None:
        if activity_name in self.TABLE.columns:
            return

        self.TABLE[activity_name] = [None]*len(self.TABLE)

    def insertData(self,
           new_data: str | int | float,
           student_email: str,
           activity_name: str
       ) -> None:

        if new_data == '': # avoid other types of nan
            new_data = np.nan

        if student_email not in self.TABLE.index:
            raise Exception(f"STUDENT({student_email}) IS NOT IN DATABASE.")
        elif activity_name not in self.TABLE.columns:
            raise Exception(f"ACTIVITY({activity_name}) IS NOT IN DATABASE.")

        # insert
        previous: str = self.TABLE.at[student_email, activity_name]

        if previous == new_data or pd.isnull(previous) or pd.isna(previous):
            # place value to a slot
            self.TABLE.at[student_email, activity_name] = new_data

        elif float(previous) == 0.0:
            # replace a slot when value is 0
            print(f"replaced the grade from student '{student_email}' of the activity '{activity_name}' from {previous} to {new_data}")
            self.TABLE.at[student_email, activity_name] = new_data

        elif pd.isnull(new_data) == False and pd.isna(new_data) == False:
            # confirm to replace slot
            response = input(
                f"system wants to replace the grade from student '{student_email}' of the activity '{activity_name}' from '{previous}' to '{new_data}', is it ok?[s/n]"
            )

            if response.upper() == "S":
                self.TABLE.at[student_email, activity_name] = new_data
                print("grade was SUCCESSFULLY replaced!")
            else:
                print("grade was NOT replaced!")


    def parseSingleActivityFile(self, file_path: Path) -> bool:
        """
        Sobrenome, Nome, Endereço de e-mail, Nota, Status da atividade, Comentários
        """

        if file_path.suffix != ".csv":
            print(f"file {file_path.name} cant be parsed")
            return False

        # get table name and add if it doesnt exist

        activity_name = file_path.name.replace("_", " ").removesuffix(".csv").upper()
        if activity_name not in self.TABLE.columns:
            self.addActivity(activity_name= activity_name)

        with open(str(file_path), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            next(reader)  # skip header

            for row in reader:
                email = row[2]
                grade = row[3]

                # add student if not in database
                if email not in self.TABLE.index:
                    self.addStudent(student_name=row[1], student_surname=row[0], student_email=email)

                self.insertData(new_data=grade, student_email=email, activity_name=activity_name)

        return True

    def exportTableToCsv(self, result_path: Path):
        self.TABLE.to_excel(result_path / "resultados.csv", sheet_name="notas", index=False)

    def joinActivities(self, activity_name1: str, activity_name2: str) -> bool | str:
        activity_name1 = activity_name1.strip().upper()
        activity_name2 = activity_name2.strip().upper()

        if (activity_name1 not in self.TABLE.columns
                or activity_name2 not in self.TABLE.columns):
            return "atividade não encontrada."

        for index in self.TABLE.index:
            previous = self.TABLE.at[index, activity_name1]

            if pd.isnull(previous) or pd.isna(previous) or float(previous) == 0.0:
                self.TABLE.at[index, activity_name1] = self.TABLE.at[index, activity_name2]

        self.TABLE.drop(activity_name2, axis="columns", inplace= True)

        return True

    def importDataFromFile(self, folder_path: Path | str) -> list[int]:
        file_number: int = 0
        files_found: int = 0

        for file in Path(folder_path).iterdir():
            successfully_imported: bool = self.parseSingleActivityFile(file_path=file)

            if successfully_imported:
                files_found += 1

            file_number += 1

        return [files_found, file_number]

    def exportTableToGoogleSheets(self, google_sheet_link: str) -> str | bool:
        """
        HEADER STRUCTURE:
            [ Nome+Sobrenome,  email,  atividade 1,  atividade 2 ...  atividade N,  total ]
        """

        if len(self.TABLE.index) == 0 or len(self.TABLE.columns) == 0:
            return "unable to export"

        sheet = connectToSpreadsheet(google_sheet_link)

        format_table(row_num=len(list(self.TABLE.index.array))+1, col_num=len(list(self.TABLE.columns.array)), sheet=sheet)

        table_cleaned = self.TABLE.fillna('0.0')
        formatted_table = [list(table_cleaned.columns.array)] + [list(table_cleaned.loc[row]) for row in list(table_cleaned.index)]

        print(formatted_table)

        insertData(sheet.get_worksheet(0), formatted_table)

        return True

grade_table = GradeTablePandas()

if __name__ == "__main__":
    grade_table.importDataFromFile("/home/athos/PycharmProjects/GoogleClassroomDataExtraction/activities")

    grade_table.joinActivities("AOC AMBIENTES X86 X ARM SUB B","ATIVIDADE TESTE 1")

    grade_table.exportTableToGoogleSheets("https://docs.google.com/spreadsheets/d/1BagQlqKf07k6ByUVKWyFsetI2U2syr_X1q1Hf4HjyUE/edit?gid=0#gid=0")

