import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from run.runPipeline import runExtraction

st.title("SETUP")

# add source folder where the activities are
folder_name : str | None = st.text_input("name of the first file to join", key= "folder name input")

if folder_name is not None and st.button("process", key= "submit button"):
    runExtraction(folder_name)

    st.write("DONE!")

# add part to upload file
join1 : str | None = st.text_input("name of the first file to join", key= "join name 1 input")
join2 : str | None = st.text_input("name of the second file to join", key= "join name 2 input")

# add part to join activities

if join1 is not None and join2 is not None and st.button("join") == True:
    pass # join given activities

# display aditional data?

