import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from scripts.ClassroomDataExtractor import grade_table
from scripts.google_classrom_connection import classroom

st.set_page_config(layout="wide")

st.title("CRIADOR AUTOMÁTICO DE PLANILHA")

if classroom.SERVICE is None:
    if st.button("conectar com google classroom"):
        classroom.connectToClassroomAPI()
        st.rerun()
elif classroom.COURSE["name"] is None:
    st.write("### escolha um dos cursos para exportar:")
    chosen_course = st.radio(label="cursos disponiveis:", options= classroom.AVAILABLE_COURSES)

    if st.button("confirmar"):
        classroom.loadDataFromCourse(str(chosen_course))
        st.rerun()
else:
    st.write("### escolha as atividades que serao carregadas")

    activity_checkboxes = [st.checkbox(label= activity_name) for activity_name in list(classroom.COURSE_ACTIVITIES)]

    if st.button("carregar dados de notas"):
        grade_table.clearTable()

        for index,checkbox in enumerate(activity_checkboxes):
            if checkbox:
                activity_name = list(classroom.COURSE_ACTIVITIES)[index]
                grade_table.loadActivityGrades(activity_name, classroom.getStudentGradesInActivity(activity_name))


    if not grade_table.TABLE.empty:
        # add part to join activities
        st.write("## tabela")
        st.dataframe(grade_table.TABLE)

    if st.button("export to google sheet"):
        # and google_sheet_link:
        grade_table.exportTableToGoogleSheets()
