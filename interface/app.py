import streamlit as st
from pathlib import Path
import sys
import tempfile
import os

from streamlit.runtime.uploaded_file_manager import UploadedFile

sys.path.append(str(Path(__file__).parent.parent))

from scripts.ClassroomDataExtractor import grade_table
from scripts.google_classrom_connection import classroom

st.set_page_config(layout="wide")

st.title("CRIADOR AUTOMÁTICO DE PLANILHA")

if classroom.SERVICE is None:
    if st.button("iniciar conexão com a API do google classroom"):
        classroom.connectToClassroomAPI()

elif classroom.COURSE["name"] is None:
    st.write(classroom.getAvailableCourses())

    course_name = st.text_input("insira o nome do curso à ser conectado")

    for activity_name in classroom.COURSE_ACTIVITIES:
        st.write(activity_name)
        st.checkbox(classroom.STUDENT_NAMES_FROM_ID[classroom.COURSE_ACTIVITIES[activity_name]])



# add source folder where the activities are

# st.write("### importar atividades")
# folder_path: str | None = st.text_input("caminho para o diretorio que os arquivos de atividades estão", key="folder name input")
# if folder_path is not None and st.button("process", key="submit button"):
#     find_rate: list = grade_table.importDataFromFile(folder_path)
#
#     if find_rate[0] == find_rate[1]:
#         st.success("done!")
#     else:
#         st.success(f"done! imported {find_rate[0]} / {find_rate[1]} files")



# add part to join activities
if len(grade_table.TABLE) > 0:
    st.write("## tabela")
    st.dataframe(grade_table.TABLE)

# st.write("### unir atividades")
# join_col1, join_col2 = st.columns(2)
# with join_col1:
#     join1: str | None = st.text_input("nome da primeira atividade", key= "join name 1 input")
# with join_col2:
#     join2: str | None = st.text_input("nome da segunda atividade", key= "join name 2 input")
#
# if join1 is not None and join2 is not None and st.button("unir", key= "join input") == True:
#     status = grade_table.joinActivities(join1, join2)
#
#     if status is True:
#         st.success("união feita com sucesso!")
#     else:
#         st.error("ERRO: "+status)

# draw all activities by name that are present in the grade table
# google_sheet_link = st.text_input("insira o link da planilha google sheets")

if st.button("exportar"): #st.button("export to google sheet"):
    # and google_sheet_link:
    grade_table.exportTableToGoogleSheets()