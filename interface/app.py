import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from scripts.ClassroomDataExtractor import grade_table

st.title("criador de planilha automático")

# add source folder where the activities are
folder_path : str | None = st.text_input("path for the activities folder", key= "folder name input")

if folder_path is not None and st.button("process", key= "submit button"):
    status = grade_table.importDataFromFile(folder_path= folder_path)

    if status is True:
        st.success("done!")
    else:
        st.error("ERROR:")

# draw all activities by name that are present in the grade table
for atv_name in grade_table.ACTIVITY_NAMES:
    st.write(atv_name)

# add part to upload file
join1 : str | None = st.text_input("name of the first file to join", key= "join name 1 input")
join2 : str | None = st.text_input("name of the second file to join", key= "join name 2 input")

# add part to join activities

if join1 is not None and join2 is not None and st.button("join", key= "join input") == True:
    pass # join given activities

# display aditional data?

