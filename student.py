import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import random

class StudentInformationViewer:
    def __init__(self):
        self.db_file = None
        self.conn = None
        self.students_df = pd.read_csv("students.csv")

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            return True
        except sqlite3.Error:
            st.error(f"Connection to {db_file} not established!")
            return False

    def get_student_info(self, student_name):
        try:
            c = self.conn.cursor()
            c.execute('''SELECT * FROM student_info WHERE student_name=?''', (student_name,))
            rows = c.fetchall()
            return rows
        except sqlite3.Error:
            st.error("Error fetching student information from database.")
            return None
        
    def display_quote(self):
        quotes = [
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "It always seems impossible until it's done. - Nelson Mandela",
            "The only way to do great work is to love what you do. - Steve Jobs"
        ]
        quote = random.choice(quotes)
        st.success(quote)

    def run(self):
        student_name_placeholder = st.empty()
        password_placeholder = st.empty()
        explore_button_placeholder = st.empty()

        student_name = student_name_placeholder.text_input("Enter Student Name:")
        password_ = password_placeholder.text_input("Personal Password", type="password")
        enter = explore_button_placeholder.button("Explore")

        if enter:
            student_name_placeholder.empty()
            password_placeholder.empty()
            explore_button_placeholder.empty()

            if student_name in self.students_df['Name'].tolist():
                correct_password = self.students_df.loc[self.students_df['Name'] == student_name, 'Password'].iloc[0]
                if password_ == correct_password:
                    self.db_file = f"student_databases/{student_name}.db"
                    if self.create_connection(self.db_file):

                        col1, col2 = st.columns([1, 1])

                        # Display quote in col1
                        with col1:
                            self.display_quote()

                        # Display formatted date in col2
                        with col2:
                            formatted_date = datetime.now().strftime('%Y-%m-%d')
                            text_with_date = f"""
                            <h1 style='text-align: center; font-size: 2rem; margin-top: -20px;'>⭐A Day to be Remembered</h1>
                            <p style='text-align: center; font-size : 2rem; margin-top: -20px;'>{formatted_date}</p>
                            """
                            st.markdown(text_with_date, unsafe_allow_html=True)

                        st.header(f"Information for {student_name}:")

                        rows = self.get_student_info(student_name)
                        tab1, tab2, tab3 = st.tabs(['Assigned Works','Your Team','Report'])

                        with tab3:
                         if rows is not None:
                            if rows:
                                for row in rows:
                                   with st.expander("You Have An Update From Your Advisor!!! Click To View More", expanded=False): 
                                    st.warning("Note : Please review the entire report for insights on your personal growth and development. Your advisors have invested their time in crafting it. Additionally, refer to the materials provided and follow the prescribed solutions and plans.")
                                    st.write("----")
                                    st.markdown(f"<h6>{row[2]}</h6>", unsafe_allow_html=True)
                                    st.write("******************")
                                    st.markdown(f"<h6>{row[3]}</h6>", unsafe_allow_html=True)
                                    st.write("******************")
                                    
                                    study_plan = row[4]
                                    if study_plan:
                                        for i, line in enumerate(study_plan.split('\n'), start=1):
                                            st.markdown(f"<h6>{line}</h6>", unsafe_allow_html=True)
                                    st.write("***********")

                                    links = row[5]
                                    if links:
                                        for i, lines in enumerate(links.split('\n'), start =1):
                                           if not lines.startswith("Study Materials:"):
                                                st.markdown(f"<a href='{lines}' target='_blank'>{lines}</a>", unsafe_allow_html=True)
                                           else:
                                                st.markdown(f"<h6>{lines}</h6>", unsafe_allow_html=True)
                                    st.write("********")
                                    st.markdown("*You can always contact the faculties in times of need we are always here to help you*")
                                    st.write("*******")

                                
                            else:
                                    st.info("No information found for the student.")
                            #else:
                             #   st.info("Error fetching student information.")

                        with tab1:
                            st.subheader("Assigned Assignments:")
                            assignment_db_file = "assignment_db.db"
                            if self.create_connection(assignment_db_file):
                                c = self.conn.cursor()
                                c.execute("SELECT * FROM assignments")
                                assignments = c.fetchall()
                                if assignments:
                                    for idx, assignment in enumerate(assignments, start=1):
                                        st.markdown(
                                            f"""
                                            <div style='border: 1px solid #ccc; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: rgba(255, 255, 255, 0.3);line-height: 2.2;'>
                                                <h3 style='color: #333; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 5px;'>Assignment {idx}</h3>
                                                <strong>Title:</strong> {assignment[1]}<br>
                                                <strong>Description:</strong> {assignment[2]}<br>
                                                <strong>Type:</strong> {assignment[3]} | <strong>Category:</strong> {assignment[4]} | <strong>Last Date:</strong> {assignment[5]} | <strong>Passing Grade:</strong> {assignment[6]}<br>
                                                <strong>Drive Link:</strong> <a href='{assignment[7]}' target='_blank'>{assignment[7]}</a><br>
                                                <strong>Submission Link:</strong> <a href='{assignment[8]}' target='_blank'>{assignment[8]}</a>
                                            </div>
                                            """, unsafe_allow_html=True)
                                        st.warning("Submit the Work Before The Deadline to Avoid Unnecessary Trouble")
                                else:
                                    st.info("No assignments found.")

                        with tab2:
                            st.subheader("Assigned Teams:")
                            team_db_file = "team.db"
                            if self.create_connection(team_db_file):
                                c = self.conn.cursor()
                                c.execute("SELECT assignment_title, mentor, members FROM teams WHERE members LIKE ?", ('%'+student_name+'%',))
                                teams = c.fetchall()
                                
                                if teams:
                                    teams_html = "<div style='font-family: Arial, sans-serif; margin-bottom: 20px;'>"
                                    for idx, team in enumerate(teams, start=1):
                                        assignment_title, mentor, members = team
                                        teams_html += f"<div style='border: 1px solid #ccc; border-radius: 5px; padding: 15px; margin-bottom: 15px; background-color: rgba(255, 255, 255, 0.3);line-height: 2.0;'>"
                                        teams_html += f"<h3 style='color: #333; margin-bottom: 10px; border-bottom: 2px solid #333; padding-bottom: 5px;'>Team {idx}</h3>"
                                        teams_html += f"<strong>Assignment Title:</strong> {assignment_title}<br>"
                                        teams_html += f"<strong>Mentor:</strong> {mentor}<br>"
                                        teams_html += "<strong>Team Members:</strong><ul>"
                                        for member in members.split(','):
                                            teams_html += f"<li>{member}</li>"
                                        teams_html += "</ul></div>"
                                    teams_html += "</div>"
                                    st.markdown(teams_html, unsafe_allow_html=True)
                                    st.warning("If You Have any issues with the Assigned Team Please Contact the Faculty")
                                else:
                                    st.info("No teams assigned.")

                    else:
                        st.info("Connection to student database not established.")
                else:
                    st.error("Unauthorized access! Please enter the correct password.")
            else:
                st.error("Unauthorized access! Please enter a valid student name.")

# if __name__ == "__main__":
#     information = StudentInformationViewer()
#     information.run()
