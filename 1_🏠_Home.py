import streamlit as st
import pandas as pd
from admin import Uploader_UI
from advisor import StudentReportMaker
from student import StudentInformationViewer
import base64
import datetime

st.set_page_config(
    page_title="Student Success Network",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

now = datetime.datetime.now()
formatted_date = now.strftime('%Y-%m-%d')

# Adding GIF background for main page
gif_background = """
<style>
.stApp {
  background-image: url("https://i.gifer.com/2iiB.gif");
  background-size: cover;
  background-position: center;
}

@keyframes glow {
    0% {
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    50% {
        text-shadow: 0 0 20px rgba(0,0,0,0.6), 0 0 30px rgba(0,0,0,0.6);
    }
    100% {
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
}
</style>
"""

st.markdown(gif_background, unsafe_allow_html=True)

# Adding image background for sidebar
img_path = r"download.jpeg"

sidebar_background = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/jpeg;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}}
</style>
"""

st.markdown(sidebar_background, unsafe_allow_html=True)

def display_description():
    description = """
    Empowering students to excel academically! Dive into personalized learning tracks, assignments, and feedback for holistic success.
    """
    st.sidebar.header("About \"Student Sucess Network:\"")
    st.sidebar.info(description)

def display_date():
    st.sidebar.title("⭐The Impactful Day Of Your Life")
    st.sidebar.info(formatted_date)

display_description()
display_date()

def show_login_page():
    st.markdown("<h1 style='text-align: center; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>\"Student Success Network\"</h1>", unsafe_allow_html=True)
    
    roles = ["Student", "Advisor", "Admin"]
    role = st.selectbox("Select Role", roles)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    st.warning("Please Select Your Designated Role and Enter Your Credentials Properly")

    if login_button:
        if role == "Student":
            if username == "Test" and password == "pass23":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.experimental_rerun()
        elif role == "Advisor":
            if username == "Teach" and password == "pass":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.experimental_rerun()
        elif role == "Admin":
            if username == "Admin" and password == "222":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.experimental_rerun()

if st.session_state.get("logged_in"):
    if st.session_state.username == "Admin":
        st.markdown("<h1 style='text-align: center; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>Student's Performance Analyser</h1>", unsafe_allow_html=True)
        st.warning("Note: The Files Generated in this process need to be sent to the respective advisors")
        data_Updater = Uploader_UI()
        data_Updater.run()   
    
    if st.session_state.username == "Teach":
        col1, col2 = st.columns([1,1])
        with col1:
            st.info("""
    * As an advisor, you can:
        * Monitor students' performance.
        * Provide personalized feedback.
        * Assign custom assignments based on individual needs.
        * Create tailored learning plans.
        * Provide relevant learning materials to support progress.
    """)
        with col2:
            st.success("""
    "The mediocre teacher tells. The good teacher explains. The superior teacher demonstrates. The great teacher inspires."
    
    Your role goes beyond simply providing information. By being a source of inspiration and motivation, you can help students reach their full potential.""", icon="✨")

            text_with_date = f"""
    <h1 style='text-align: center; font-size: 2rem;'>A Day to be Remembered</h1>
    <p style='text-align: center; font-size: 2rem'>{formatted_date}</p>
    """
            st.markdown(text_with_date, unsafe_allow_html=True)

        review_system = StudentReportMaker()
        review_system.run()

    if st.session_state.username == "Test":
        st.write("<h4 style='text-align: left; color: white; -webkit-text-stroke-width: 1px; -webkit-text-stroke-color: black; font-family: Arial, sans-serif; animation: glow 1.5s ease-in-out infinite;'>📚📚Welcome Champ!!📚📚</h4>", unsafe_allow_html=True)
        information = StudentInformationViewer()
        information.run()
    
    if st.button("Log out"):
        st.session_state.logged_in = False
else:
    show_login_page()
