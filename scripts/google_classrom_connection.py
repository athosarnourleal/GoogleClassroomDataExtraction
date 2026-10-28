import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path

import numpy as np

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly" ,
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]

CREDENTIALS_FOLDER = Path(__file__).parent.parent / "google credentials"


class GoogleClassroomAPIManager:
    def __init__(self):
        self.SERVICE = None
        self.AVAILABLE_COURSES = []
        self.COURSE = {"name": None, "id": None}
        self.COURSE_ACTIVITIES = None
        self.STUDENT_NAMES_FROM_ID = None
        self.AVAILABLE_ACTIVITIES = []

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

            self.AVAILABLE_COURSES = self.getAvailableCourses()

            if len(self.AVAILABLE_COURSES) == 1:
                self.loadDataFromCourse(self.AVAILABLE_COURSES[0])

        except HttpError as error:
            raise  f"An error occurred: {error}"

    def loadDataFromCourse(self, course_name: str):
        if self.SERVICE is None:
            raise Exception("unable to request data from a unconnected API.")

        self.COURSE = {"name": course_name, "id": self.getCourseId(course_name)}

        self.COURSE_ACTIVITIES = self.getActivities()

        self.STUDENT_NAMES_FROM_ID = self.loadStudents()

        self.AVAILABLE_ACTIVITIES = self.COURSE_ACTIVITIES.keys()

    def getAvailableCourses(self) -> list:
        results = self.SERVICE.courses().list(pageSize= 10).execute()

        return [course["name"] for course in results.get("courses", [])]

    def loadStudents(self):
        students = self.SERVICE.courses().students().list(courseId=self.COURSE["id"]).execute().get("students", [])

        return {student["userId"] : student["profile"]["name"]["fullName"] for student in students}

    def getCourseId(self, course_name):
        courses = self.SERVICE.courses().list(pageSize=50).execute().get("courses", [])

        for c in courses:
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

        activities = self.SERVICE.courses().courseWork().list(
            courseId= self.COURSE["id"],
            pageSize=10
        ).execute().get("courseWork", [])

        return {str(a["title"]).strip().lower(): str(a["id"])    for a in activities }

    def getStudentGradesInActivity(self, coursework_name: str):
        """
            extract grading information
        """
        submissions = self.SERVICE.courses().courseWork().studentSubmissions().list(
            courseId=self.COURSE["id"],
            courseWorkId=self.COURSE_ACTIVITIES[coursework_name],
            pageSize=10
        ).execute().get("studentSubmissions", [])

        activity_grades = []

        for sub in submissions:
            if "assignedGrade" in sub:
                activity_grades.append(
                    (self.STUDENT_NAMES_FROM_ID[sub["userId"]], sub["assignedGrade"])
                )
            elif "draftGrade" in sub:
                activity_grades.append(
                    (self.STUDENT_NAMES_FROM_ID[sub["userId"]], sub["draftGrade"])
                )
            else:
                activity_grades.append(
                    (self.STUDENT_NAMES_FROM_ID[sub["userId"]], np.nan)
                )

        return activity_grades

classroom = GoogleClassroomAPIManager()



