import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly" ,
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]
"""
"https://www.googleapis.com/auth/classroom.courses.readonly 
https://www.googleapis.com/auth/classroom.student-submissions.students.readonly 
https://www.googleapis.com/auth/classroom.coursework.students.readonly 
https://www.googleapis.com/auth/classroom.rosters.readonly"


"https://www.googleapis.com/auth/classroom.courses.readonly",
"https://www.googleapis.com/auth/classroom.student-submissions.students.readonly" ,
"https://www.googleapis.com/auth/classroom.rosters.readonly"
"""
CREDENTIALS_FOLDER = Path(__file__).parent.parent / "google credentials"


class GoogleClassroomAPIManager:
    def __init__(self):

        self.SERVICE = None
        self.COURSE = {"name": None, "id": None}
        self.COURSE_ACTIVITIES = None
        self.STUDENT_NAMES_FROM_ID = None

    def connectToClassroomAPI(self):
        """
          original sourced from google-classroom API documentation(adapted to project)
        """

        creds = None
        if os.path.exists("../google credentials/token.json"):
            creds = Credentials.from_authorized_user_file("../google credentials/token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds_path = CREDENTIALS_FOLDER / "credentials_client_google_classroom.json"

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_path), SCOPES
                )

                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(CREDENTIALS_FOLDER / "token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.SERVICE = build("classroom", "v1", credentials=creds)
        except HttpError as error:
            raise  f"An error occurred: {error}"

    def loadDataFromAPI(self, course_name: str):
        if self.SERVICE is None:
            raise Exception("unable to request data from a unconnected API.")

        self.COURSE = {"name": course_name, "id": self.getCourseId(course_name)}

        self.COURSE_ACTIVITIES = self.getActivities()

        self.STUDENT_NAMES_FROM_ID = self.loadStudents()

    def getAvailableCourses(self) -> list:
        results = self.SERVICE.courses().list(pageSize= 10).execute()

        return [course["name"] for course in results.get("courses", [])]

    def loadStudents(self):
        students = self.SERVICE.courses().students().list(courseId=self.COURSE["id"]).execute().get("students", [])
        # print("STUDENTS: ")
        # print(students)

        return {student["userId"] : student["profile"]["name"]["fullName"] for student in students}

    def getCourseId(self, course_name):
        courses = self.SERVICE.courses().list(pageSize=50).execute().get("courses", [])

        for c in courses:
            print(c["name"] + " -> " + c["id"])
            if c["name"] == course_name:
                return c["id"]

        raise Exception(f"no course named '{course_name}' exists")

    def getActivities(self) -> dict:
        """
        returns a dictionary following the format:
          {
            <COURSEWORK_NAME> : <COURSEWORK_ID>
          }
        """

        activities = self.SERVICE.courses().courseWork().list(courseId=self.COURSE["id"], pageSize=10).execute().get(
            "courseWork", [])

        return {str(a["title"]).strip().lower(): str(a["id"])    for a in activities }

    def getStudentGradesInActivity(self, coursework_name: str):
        """
            extract grading indormation
        """
        response = self.SERVICE.courses().courseWork().studentSubmissions().list(
            courseId=self.COURSE["id"],
            courseWorkId=self.COURSE_ACTIVITIES[coursework_name],
            pageSize=10
        ).execute()

        print("\n",response,"\n", sep="")

        submissions = response.get("studentSubmissions", [])

        for sub in submissions:
            print(sub)
            print(sub["userId"])
            print(self.STUDENT_NAMES_FROM_ID[sub["userId"]])

            if "assignedGrade" in sub:
                print(sub["assignedGrade"])
            else:
                print("assigned grade not found")

            if "draftGrade" in sub:
                print(sub["draftGrade"])
            else:
                print("draft grade not found")




classroom = GoogleClassroomAPIManager()

if __name__ == "__main__":
    classroom.connectToClassroomAPI()

    print(classroom.getAvailableCourses())

    classroom.loadDataFromAPI("Turma Teste")

    print(classroom.STUDENT_NAMES_FROM_ID)
    print(classroom.COURSE_ACTIVITIES)

    classroom.getStudentGradesInActivity("atividade teste 1")
    classroom.getStudentGradesInActivity("atividade teste 2")

"""
['Turma Teste']
Turma Teste -> 869946068551
{'108182077976741060636': 'Aluno Jonas'}
{'atividade teste 2': '869946684832', 'atividade teste 1': '869946150463'}
{'courseId': '869946068551', 'courseWorkId': '869946684832', 'id': 'Cg4IsrXW5qgZEKDr8-aoGQ', 'userId': '108182077976741060636', 'creationTime': '2026-09-30T11:41:55.023Z', 'updateTime': '2026-09-30T11:42:21.867Z', 'state': 'CREATED', 'late': True, 'draftGrade': 0, 'alternateLink': 'https://classroom.google.com/c/ODY5OTQ2MDY4NTUx/a/ODY5OTQ2Njg0ODMy/submissions/by-status/and-sort-last-name/student/ODY5OTQ2MjAyODAy', 'courseWorkType': 'ASSIGNMENT', 'assignmentSubmission': {'attachments': [{'driveFile': {'id': '1lCXoisMzw9KFMyK2RTFqq7ZRY2EyoXWd', 'alternateLink': 'https://drive.google.com/open?id=1lCXoisMzw9KFMyK2RTFqq7ZRY2EyoXWd'}}]}, 'submissionHistory': [{'stateHistory': {'state': 'CREATED', 'stateTimestamp': '2026-09-30T11:41:55.015Z', 'actorUserId': '108182077976741060636'}}]}
108182077976741060636
Aluno Jonas
"""