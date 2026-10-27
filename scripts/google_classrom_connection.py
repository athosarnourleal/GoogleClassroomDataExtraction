import os.path

import numpy as np
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly"
]

CREDENTIALS_FOLDER = Path(__file__).parent.parent / "google credentials"


class GoogleAPIManager:
    def __init__(self, course_name: str):

        self.SERVICE = self.getClassroomAPIServiceObject()

        self.COURSE = {"name": course_name, "id": self.getCourseId(course_name)}

        self.COURSE_ACTIVITIES = self.getActivities()

        self.STUDENT_NAMES = self.getStudents()

    @staticmethod
    def getClassroomAPIServiceObject():
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
            return build("classroom", "v1", credentials=creds)
        except HttpError as error:
            raise f"An error occurred: {error}"

    def getStudents(self):

        students = self.SERVICE.courses().students().list(courseId=self.COURSE["id"]).execute().get("students")

        return {students["id"]: students["name"]}

    def getCourseId(self, course_name):
        courses = self.SERVICE.courses().list(pageSize=50).execute().get("courses", [])

        for c in courses:
            print(c["name"] + " -> " + c["id"])
            if c["name"] == course_name:
                return c["id"]

        raise f"no course named '{course_name}' exists"

    def getActivities(self) -> dict:
        """
        returns a dictionary following the format:
          {
            <COURSEWORK_NAME> : <COURSEWORK_ID>
          }
        """

        activities = self.SERVICE.courses().courseWork().list(courseId=self.COURSE["id"], pageSize=10).execute().get(
            "courseWork", [])

        return {   str(a["title"]).strip().lower() : str(a["id"])    for a in activities }

    def getStudentGradesInActivity(self, coursework_name: str):
        """
            extract grading indormation
        """
        response = self.SERVICE.courses().courseWork().studentSubmissions().list(
            courseId=self.COURSE["id"],
            courseWorkId=self.COURSE_ACTIVITIES[coursework_name],
            pageSize=10
        ).execute()

        # TODO: format to a table for pandas

if __name__ == "__main__":
    manager = GoogleAPIManager("Turma Teste")



