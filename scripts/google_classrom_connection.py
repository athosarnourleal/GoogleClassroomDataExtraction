import os.path

import numpy as np
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path

from oauthlib.oauth1.rfc5849.endpoints import access_token

# If modifying these scopes, delete the file token.json
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly" ,
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]

def callAPIList(api_caller, target_item, **kwargs):
    results = []
    page_token = None

    # get other pages from the API response
    while True:
        api_response = api_caller.list(
            pageSize=100,
            pageToken=page_token,
            **kwargs
        ).execute()

        results.extend(api_response.get(target_item, []))
        page_token = api_response.get("nextPageToken", [])

        if not page_token:
            break

    return results

class GoogleClassroomAPIManager:
    def __init__(self):
        # general data
        self.SERVICE = None
        self.AVAILABLE_COURSES: dict = {}

        # course data
        self.COURSE = {"name": None, "id": None}
        self.COURSE_ACTIVITIES = None
        self.STUDENT_NAMES_FROM_ID = None


    def connectToClassroomAPI(self):
        """
          original sourced from google-classroom API documentation(adapted to project)
        """

        creds = None
        if os.path.exists(str(Path(__file__).parent.parent / "google credentials" / "token.json")):
            print("GETTING FROM TOKEN")
            creds = Credentials.from_authorized_user_file(str(Path(__file__).parent.parent / "google credentials" / "token.json"), SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("REFRESING TOKEN")
                creds.refresh(Request())
            else:
                print("NOT GETTING FROM TOKEN")
                creds_path = Path(__file__).parent.parent / "google credentials" / "credentials_client_google_classroom.json"

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(creds_path), SCOPES
                )

                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(Path(__file__).parent.parent / "google credentials" / "token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.SERVICE = build("classroom", "v1", credentials=creds)

            self.AVAILABLE_COURSES = self.getAvailableCourses()

            if len(self.AVAILABLE_COURSES) == 1:
                self.loadDataFromCourse(self.AVAILABLE_COURSES[0])

        except HttpError as error:
            raise  f"An error occurred: {error}"

    def unloadDataFromCourse(self):
        self.COURSE = {"name": None, "id": None}
        self.COURSE_ACTIVITIES = None
        self.STUDENT_NAMES_FROM_ID = None

    def loadDataFromCourse(self, course_name: str):
        if self.SERVICE is None:
            raise Exception("unable to request data from a unconnected API.")

        self.COURSE = {"name": course_name, "id": self.AVAILABLE_COURSES[course_name]}

        self.COURSE_ACTIVITIES = self.getActivities()

        self.STUDENT_NAMES_FROM_ID = self.loadStudents()

    def getAvailableCourses(self) -> dict:
        results = self.SERVICE.courses().list(pageSize= 50).execute().get("courses", [])

        courses_dict = {}
        for course in results:
            if "section" in course:
                courses_dict[f"{course["name"]}({course["section"]})"] = course["id"]
            else:
                courses_dict[f"{course["name"]}"] = course["id"]

        return courses_dict

    def loadStudents(self):

        students_raw = callAPIList(
            api_caller=self.SERVICE.courses().students(),
            target_item="students",
            courseId=self.COURSE["id"]
        )

        students = {student["userId"] : student["profile"]["name"]["fullName"] for student in students_raw}

        return students

    def getActivities(self):
        """
        returns a dictionary following the format:
            [
                (<COURSEWORK_NAME>, <COURSEWORK_ID>)
            ]
        """

        coursework = callAPIList(
            api_caller= self.SERVICE.courses().courseWork(),
            target_item="courseWork",
            courseId=self.COURSE["id"]
        )

        activities_raw = []
        for index, a in enumerate(coursework):
            name = str(a["title"]).strip().upper()

            activities_raw.append((name, a["id"]))

        # fix names to account for repeating
        activities_names = [name[0] for name in activities_raw]
        activities = []

        for index, (actv_name, actv_id) in enumerate(activities_raw):
            repeating = activities_names[index+1:].count(actv_name) + 1

            if repeating > 1:
                activities.append(  (actv_name+f" ({repeating})",actv_id)  )
            else:
                activities.append(  (actv_name,actv_id)  )

        return activities

    def getStudentGradesInActivity(self, course_index: int):
        """
            extract grading information
        """


        submissions = callAPIList(
            api_caller= self.SERVICE.courses().courseWork().studentSubmissions(),
            target_item="studentSubmissions",
            courseId=self.COURSE["id"],
            courseWorkId=self.COURSE_ACTIVITIES[course_index][1]
        )

        activity_grades = []
        for sub in submissions:
            if sub["userId"] not in self.STUDENT_NAMES_FROM_ID:
                print("STUDENT SKIPPED...")
                continue

            if "assignedGrade" in sub:
                activity_grades.append(
                    (self.STUDENT_NAMES_FROM_ID[sub["userId"]], sub["assignedGrade"])
                )
            else:
                activity_grades.append(
                    (self.STUDENT_NAMES_FROM_ID[sub["userId"]], np.nan)
                )


        return activity_grades


classroom = GoogleClassroomAPIManager()

classroom.connectToClassroomAPI()



