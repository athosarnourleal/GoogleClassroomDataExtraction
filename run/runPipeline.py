
from pathlib import Path
from scripts.ClassroomDataExtractor import GradeTable

def run():
    print("running")

    folder = Path(__file__).parent.parent / "activities"

    grade_table = GradeTable()

    for file in folder.iterdir():
        grade_table.parseActivityFile(file_path= file)

    grade_table.extractTableToCsv(result_path= Path(__file__).parent)

if __name__ == "__main__":
    run()
