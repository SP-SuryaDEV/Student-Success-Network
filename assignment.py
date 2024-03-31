import streamlit as st
import sqlite3
import os
from datetime import datetime

class AssignmentManager:
    def __init__(self):
        self.create_database_if_not_exists()

    @staticmethod
    def create_database_if_not_exists():
        db_file = "assignment_db.db"
        if not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE assignments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            assignment_type TEXT,
                            passing_grade TEXT,
                            last_date TEXT,
                            category TEXT,
                            drive_link TEXT,
                            submission_link TEXT
                        )''')
            conn.commit()
            conn.close()

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            st.error(e)
        return conn

    def assign_assignment(self, title, description, assignment_type, passing_grade, last_date, category, drive_link, submission_link):
        db_file = "assignment_db.db"
        conn = self.create_connection(db_file)
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute('''INSERT INTO assignments (title, description, assignment_type, passing_grade, last_date, category, drive_link, submission_link)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (title, description, assignment_type, passing_grade, last_date, category, drive_link, submission_link))
                conn.commit()
                st.success("Assignment assigned successfully!")
            except sqlite3.Error as e:
                st.error(e)
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")

    def view_assignments(self):
        db_file = "assignment_db.db"
        conn = self.create_connection(db_file)
        assignments = []
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM assignments")
                rows = c.fetchall()
                for row in rows:
                    assignments.append({
                        'title': row[1],
                        'description': row[2],
                        'assignment_type': row[3],
                        'passing_grade': row[4],
                        'last_date': row[5],
                        'category': row[6],
                        'drive_link': row[7],
                        'submission_link': row[8]
                    })
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")
        
        return assignments

    def clear_assignments(self):
        db_file = "assignment_db.db"
        conn = self.create_connection(db_file)
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM assignments")
                conn.commit()
                st.warning("All assignments cleared successfully!")
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")

    def display_assignments_tab(self):
        st.title("Assignment Manager")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Assignment Title")
            description = st.text_area("Assignment Description")
            assignment_type = st.selectbox("Assignment Type", ["Essay", "Project", "Presentation", "Quiz", "Homework"])
            passing_grade = st.selectbox("Passing Grade", ["A", "B", "C", "D","-"])
            
        
        with col2:
            last_date = st.date_input("Last Date", value=datetime.today())
            category = st.selectbox("Category", ["Team of 4","Team of 3","Team of 2","Individual"])
            drive_link = st.text_input("Drive Link")
            submission_link = st.text_input("Submission Link (Google Form)")

        cole1,cole2,cole3 = st.columns([3,1,1])

        with cole2:
         if st.button("Update Assignment"):
            self.assign_assignment(title, description, assignment_type, passing_grade, last_date, category, drive_link, submission_link)

        assignments = self.view_assignments()
        
        with cole1:
         if st.button("View Assigned Works"): 
            if assignments:
                st.subheader("Assigned Assignments:")
                for idx, assignment in enumerate(assignments, start=1):
                    st.markdown(
                        f"""
                        <div style='border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 15px; background-color: rgba(255, 255, 255, 0.5)'>
                            <h3 style='color: #333; margin-bottom: 10px; border-bottom: 2px solid #333; padding-bottom: 5px;'>Assignment {idx}</h3>
                            <strong>Title:</strong> {assignment['title']}<br>
                            <strong>Description:</strong> {assignment['description']}<br>
                            <strong>Type:</strong> {assignment['assignment_type']} | <strong>Category:</strong> {assignment['category']} | <strong>Last Date:</strong> {assignment['last_date']} | <strong>Passing Grade:</strong> {assignment['passing_grade']}<br>
                            <strong>Drive Link:</strong> <a href='{assignment['drive_link']}' target='_blank'>{assignment['drive_link']}</a><br>
                            <strong>Submission Link:</strong> <a href='{assignment['submission_link']}' target='_blank'>{assignment['submission_link']}</a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("No assignment")

        with cole3:

         if st.button("Clear All Assignments"):
            self.clear_assignments()

        st.write("")

#manager = AssignmentManager()
#manager.display_assignments_tab()
