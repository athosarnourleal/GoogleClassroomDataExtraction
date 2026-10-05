
from pathlib import Path
from scripts.ClassroomDataExtractor import GradeTable

def runExtraction(folder_path : Path | str):
    print("running")

    grade_table = GradeTable()

    for file in Path(folder_path).iterdir():
        grade_table.parseActivityFile(file_path= file)

    grade_table.exportTableToGoogleSheets()

if __name__ == "__main__":
    runExtraction(Path(__file__).parent.parent / "activities")
