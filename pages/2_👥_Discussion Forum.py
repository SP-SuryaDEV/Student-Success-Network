import streamlit as st
import sqlite3
import os
import csv
import datetime
from Styles import Style
import base64
import random

st.set_page_config(
    page_title="Student Success Network",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

now = datetime.datetime.now()
formatted_date = now.strftime('%Y-%m-%d')

adding_gif_background = Style(f"""
<style>
.stApp {{
  background-image: url("https://i.gifer.com/2iiB.gif");
  background-size: cover;
  background-position: center;
}}

@keyframes glow {{
    0% {{
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
    50% {{
        text-shadow: 0 0 20px rgba(0,0,0,0.6), 0 0 30px rgba(0,0,0,0.6);
    }}
    100% {{
        text-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}
}}
</style>
""")

adding_gif_background.run()

# Function to encode image to base64
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get sidebar image as base64
img_path = r"download.jpeg"
img_base64 = get_img_as_base64(img_path)

# Apply sidebar image background
sidebar_background = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/jpeg;base64,{img_base64}");
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

# Function to display formatted date
def display_date():
    formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
    st.sidebar.title("⭐The Impactful Day Of Your Life")
    st.sidebar.info(formatted_date)

# Display description and date in the sidebar
display_description()
display_date()

# Initialize SQLite database
def init_db():
    if not os.path.exists('chats.db'):
        conn = sqlite3.connect('chats.db')
        c = conn.cursor()
        
        # Create table for chats
        c.execute('''CREATE TABLE IF NOT EXISTS chats (name TEXT, message TEXT, timestamp TEXT)''')
        
        conn.commit()
        conn.close()

# Read students.csv to get credentials
def get_credentials():
    credentials = {}
    with open('students.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials[row['Name']] = row['Password']
    credentials['Advisor'] = '12345'
    return credentials

# Function to insert chat message into database
def insert_chat(name, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('chats.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO chats (name, message, timestamp) VALUES (?, ?, ?)", (name, message, timestamp))
    
    conn.commit()
    conn.close()

# Function to retrieve chat messages from database
def get_chats():
    conn = sqlite3.connect('chats.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM chats")
    chats = c.fetchall()
    
    conn.close()
    return chats

def display_quote():
    quotes = [
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "It always seems impossible until it's done. - Nelson Mandela",
        "The only way to do great work is to love what you do. - Steve Jobs"
    ]
    quote = random.choice(quotes)
    st.success(quote)

# Main function to run the app
def main():
    st.title("Discussion Forum:")
    col1, col2 = st.columns([1, 1])

    # Display Quote in col1
    with col1:
        display_quote()

    # Display formatted date in col2
    with col2:
        formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
        text_with_date = f"""
        <h1 style='text-align: center; font-size: 2rem; margin-top: -20px;'>⭐A Day to be Remembered</h1>
        <p style='text-align: center; font-size : 2rem; margin-top: -20px;'>{formatted_date}</p>
        """
        st.markdown(text_with_date, unsafe_allow_html=True)
    
    # Initialize database
    init_db()

    # Get credentials from students.csv
    credentials = get_credentials()

    # Create empty slots for name and password fields
    name_placeholder = st.empty()
    password_placeholder = st.empty()

    # Chat input
    name_key = "name_input"  # Unique key for name input
    password_key = "password_input"  # Unique key for password input
    name = name_placeholder.text_input("Name", key=name_key)
    password = password_placeholder.text_input("Password", type="password", key=password_key)

    # Display chat messages only if correct credentials are entered
    if name in credentials and credentials[name] == password:
        # Hide name and password fields
        name_placeholder.empty()
        password_placeholder.empty()
        st.divider()
        st.warning("Please maintain respect and decorum when chatting with others. This platform is for both students and advisors to discuss assignments and collaborate effectively.")

        # Display chat history within a scrollable box with transparent background and border
        chats = get_chats()
        chat_history_formatted = "<div style='max-height: 400px; overflow-y: scroll; background-color: rgba(255, 255, 255, 0); padding: 10px; border: 1px solid #ccc; border-radius: 5px;'>"
        chat_history_formatted += "<div style='margin-bottom: 10px;'>"
        for chat in chats:
            timestamp = datetime.datetime.strptime(chat[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            if chat[0] == 'Advisor':
                chat_history_formatted += f"<div><span style='color: red;'>{chat[0]}</span> (<span style='font-size: small;'>{timestamp}</span>): {chat[1]}</div>"
            else:
                chat_history_formatted += f"<div><span style='color: green;'>{chat[0]}</span> (<span style='font-size: small;'>{timestamp}</span>): {chat[1]}</div>"
            chat_history_formatted += "</div><div style='margin-bottom: 10px;'>"
        chat_history_formatted += "</div></div>"
        
        st.subheader("Chat History")
        st.markdown(chat_history_formatted, unsafe_allow_html=True)

        # Message input
        message = st.text_input("Your Message", key="message")
        
        if st.button("Send"):
            insert_chat(name, message)
            st.experimental_rerun()  # Rerun the app to update chat history

    elif name and password:
        st.warning("Invalid credentials. Please check your name and password.")

if __name__ == "__main__":
    main()
