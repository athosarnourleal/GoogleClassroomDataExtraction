
import os
from pathlib import Path

# fix root

from scripts.ClassroomDataExtractor import GradeTable

def run():
    print("running")

    folder = Path(__file__).parent.parent / "activities"

    grade_table = GradeTable()

    for file in folder.iterdir():
        print(file)
        grade_table.extractActivityCsv()

if __name__ == "__main__":
    run()
