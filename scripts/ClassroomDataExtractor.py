import csv
from pathlib import Path
import pandas as pd

class GradeTable:

    def __init__(self):
        self.STUDENT_EMAILS = [] # será usado como "primary key"
        self.STUDENT_NAMES = []
        self.ACTIVITY_NAMES = []
        self.DATABASE = [[]] # 2d array

        # rows --> ALUNOS_NOME
        # columns --> ATIVIDADES_NOME

    def addStudent(self, student_name: str, student_surname: str, student_email: str):
        if student_email in self.STUDENT_EMAILS:
            return

        if len(student_name) == 0 | len(student_name.strip()) == 0:
            raise Exception(f"INSERTED STUDENT({student_email}) DOES NOT HAVE A NAME.")

        self.STUDENT_NAMES.append(student_name.strip().title() + " " + student_surname.strip().title())
        self.STUDENT_EMAILS.append(student_email)

        if len(self.DATABASE) == len(self.STUDENT_EMAILS):
            # avoid creating extra lines
            return

        # add a new line
        self.DATABASE.append(['' for i in range(len(self.DATABASE[0]))])

    def addActivity(self, activity_name: str) -> None:
        if activity_name in self.ACTIVITY_NAMES:
            return

        self.ACTIVITY_NAMES.append(activity_name.strip().upper())

        # add a new collumn
        for i in range(len(self.DATABASE)):
            self.DATABASE[i].append("")

    def insertData(self, new_data: str | int | float, student_email: str, activity_name: str) -> None:
        if student_email not in self.STUDENT_EMAILS:
            raise Exception(f"STUDENT({student_email}) IS NOT IN DATABASE.")
        elif activity_name not in self.ACTIVITY_NAMES:
            raise Exception(f"ACTIVITY({activity_name}) IS NOT IN DATABASE.")

        # get position
        row_num = self.STUDENT_EMAILS.index(student_email)
        col_num = self.ACTIVITY_NAMES.index(activity_name)

        # insert
        previous: str = self.DATABASE[row_num][col_num]
        if self.isEmpty(previous):
            # place value to a slot
            self.DATABASE[row_num][col_num] = new_data

        elif int(previous) == 0.0:
            # replace a slot when value is 0
            print(f"replaced the grade from student '{student_email}' of the activity '{activity_name}' from {previous} to {new_data}")
            self.DATABASE[row_num][col_num] = new_data

        else:
            # confirm to replace slot
            response = input(
                f"system wants to replace the grade from student '{student_email}' of the activity '{activity_name}' from '{previous}' to '{new_data}', is it ok?[s/n]"
            )

            if response.upper() == "S":
                self.DATABASE[row_num][col_num] = new_data
                print("grade was SUCCESSFULLY replaced!")
            else:
                print("grade was NOT replaced!")

    @staticmethod
    def isEmpty(slot) -> bool:
        if slot is None or len(slot) == 0 or str(slot).strip() == "" or int(slot) == 0.0:
            return True

        return False

    def parseActivityFile(self, file_path: Path):
        """
        Sobrenome, Nome, Endereço de e-mail, Nota, Status da atividade, Comentários
        """

        if file_path.suffix != ".csv":
            print(f"file {file_path.name} cant be parsed")
            return

        # get table name and add
        activity_name = file_path.name.replace("_", " ").removesuffix(".csv").upper()
        if activity_name not in self.ACTIVITY_NAMES:
            self.addActivity(activity_name= activity_name)

        with open(str(file_path), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            next(reader)  # skip header

            for row in reader:
                email = row[2]
                grade = row[3]

                # add student if not in database
                if email not in self.STUDENT_EMAILS:
                    self.addStudent(student_name=row[1], student_surname=row[0], student_email=email)

                self.insertData(new_data=grade, student_email=email, activity_name=activity_name)

    def getActivitiesCollumns(self) -> dict:
        activities = {}

        for index, atv in enumerate(self.ACTIVITY_NAMES):
            atv_grades = []

            for line in range(len(self.DATABASE)):
                atv_grades.append(self.DATABASE[line][index])

            activities.update({atv: atv_grades})

        return activities

    def extractTableToCsv(self, result_path: Path):
        """
        STRUCTURE:
            [ Nome+Sobrenome,  email,  atividade 1,  atividade 2 ...  atividade N,  total ]
        """

        dataset_dict = {"NOME DO ALUNO": self.STUDENT_NAMES, "EMAIL DO ALUNO": self.STUDENT_EMAILS}

        # add activities part of the spreadsheet
        dataset_dict.update(self.getActivitiesCollumns())

        # extrair
        df = pd.DataFrame(dataset_dict)
        
        df.to_excel(result_path / "resultados.xlsx", sheet_name="notas", index=False)

