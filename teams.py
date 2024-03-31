import streamlit as st
import sqlite3
import os
import pandas as pd

class TeamAssigner:
    def __init__(self):
        self.create_database_if_not_exists()

    @staticmethod
    def create_database_if_not_exists():
        db_file = "team.db"
        if not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE teams (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            assignment_title TEXT NOT NULL,
                            mentor TEXT NOT NULL,
                            members TEXT NOT NULL
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

    def create_team(self, assignment_title, mentor, members):
        db_file = "team.db"
        conn = self.create_connection(db_file)
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute('''INSERT INTO teams (assignment_title, mentor, members)
                             VALUES (?, ?, ?)''', (assignment_title, mentor, members))
                conn.commit()
                st.success("Team created successfully!")
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")

    def display_team_input(self):
        st.header("Team Details for the Projects:")
        st.success("Everyone has the potential to lead in their own way; there's no one true leader. Therefore, we do not assign a specific team leader.")

        
        # Input field for Assignment Title
        assignment_title = st.text_input("Enter Assignment Title")
        
        # Dropdown options for Mentor
        mentor_options = ["Mr.Simon", "Mr.Peter", "Mr.Saint", "Mr.Pietro"]
        mentor = st.selectbox("Mentor Name", mentor_options)
        
        # Read student names from students.csv
        df_students = pd.read_csv("students.csv")
        student_names = df_students['Name'].tolist()
        
        # Get already selected members
        db_file = "team.db"
        conn = self.create_connection(db_file)
        already_selected_names = []
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT members FROM teams")
                teams = c.fetchall()
                
                for team in teams:
                    members = team[0].split(',')
                    already_selected_names.extend(members)
                
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        
        # Remove already selected members from student_names
        available_student_names = [name for name in student_names if name not in already_selected_names]
        
        # Select Team Size
        team_size = st.selectbox("Select Team Size", options=[2, 3, 4])
        
        members = st.multiselect("Team Members", available_student_names, default=available_student_names[:team_size])
        
        if not members:
            st.warning("Please select team members.")
            return
        
        members_str = ','.join(members)
        
        # Structured button arrangement
        col1, col2, col3 = st.columns([3,1,1])
        
        with col2:
            if st.button("Create Team"):
                self.create_team(assignment_title, mentor, members_str)
        
        with col1:
            if st.button("Show Created Teams"):
                self.display_created_teams()
        
        with col3:
            if st.button("Clear Teams"):
                self.clear_teams()

    def display_created_teams(self):
        st.subheader("Created Teams")
        
        db_file = "team.db"
        conn = self.create_connection(db_file)
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT assignment_title, mentor, members FROM teams")
                teams = c.fetchall()
                
                if not teams:
                    st.info("No teams created yet.")
                else:
                    teams_html = "<div style='font-family: Arial, sans-serif; margin-bottom: 20px;'>"
                    for idx, team in enumerate(teams, start=1):
                        assignment_title, mentor, members = team
                        teams_html += f"<div style='border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 15px; background-color: rgba(255, 255, 255, 0.5)'>"
                        teams_html += f"<h3 style='color: #333; margin-bottom: 10px; border-bottom: 2px solid #333; padding-bottom: 5px;'>Team {idx}</h3>"
                        teams_html += f"<strong>Assignment Title:</strong> {assignment_title}<br>"
                        teams_html += f"<strong>Mentor:</strong> {mentor}<br>"
                        teams_html += "<strong>Team Members:</strong><ul>"
                        for member in members.split(','):
                            teams_html += f"<li>{member}</li>"
                        teams_html += "</ul></div>"
                        # for member in members.split(','):
                        #     teams_html += f"<li>{member}</li>"
                        # teams_html += "</ul></div>"
                    
                    teams_html += "</div>"
                    
                    st.markdown(f"<div style='height:400px; overflow:auto;'>{teams_html}</div>", unsafe_allow_html=True)
                
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")

    def clear_teams(self):
        db_file = "team.db"
        conn = self.create_connection(db_file)
        
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM teams")
                conn.commit()
                st.warning("All teams cleared successfully!")
            except sqlite3.Error as e:
                st.error(e)
            finally:
                conn.close()
        else:
            st.error("Error: Cannot create database connection.")

# Uncomment the following lines to test the class
# team_assigner = TeamAssigner()
# team_assigner.display_team_input()
