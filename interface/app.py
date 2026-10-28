import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from scripts.ClassroomDataExtractor import grade_table
from scripts.google_classrom_connection import classroom

st.set_page_config(layout="wide")

st.title("CRIADOR AUTOMÁTICO DE PLANILHA")

if classroom.SERVICE is None:
    st.write("# conectar com sua conta no google")
    if st.button("conectar"):
        classroom.connectToClassroomAPI()
        st.rerun()
elif classroom.COURSE["name"] is None:
    st.write("### escolha um dos cursos para exportar:")
    chosen_course = st.radio(label="cursos disponiveis:", options= classroom.AVAILABLE_COURSES)

    if st.button("confirmar"):
        classroom.loadDataFromCourse(str(chosen_course))
        st.rerun()
else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("### escolha as atividades que serao carregadas")

        activity_checkboxes = [st.checkbox(label= activity_name) for activity_name in list(classroom.COURSE_ACTIVITIES)]

        if st.button("carregar dados de notas"):
            grade_table.clearTable()

            for index,checkbox in enumerate(activity_checkboxes):
                if checkbox:
                    activity_name = list(classroom.COURSE_ACTIVITIES)[index]
                    grade_table.loadActivityGrades(activity_name, classroom.getStudentGradesInActivity(activity_name))

    if not grade_table.TABLE.empty:
        with col2:
            # add part to join activities
            st.write("## tabela")
            st.dataframe(grade_table.TABLE)

        st.write("## exportar")
        title = st.text_input(label="insira o titulo da planilha", value="planilha de notas")
        if st.button("export to google sheet") and str(title).strip() != "":
            # and google_sheet_link:
            grade_table.exportTableToGoogleSheets(sheet_title=title)




