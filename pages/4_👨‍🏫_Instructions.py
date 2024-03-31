import streamlit as st
from Styles import Style
import base64
import datetime
import random
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
img_path = r"C:\Users\jofra\Desktop\Presentation\MachineKnight\Application\download.jpeg"

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

def display_description():
    description = """
    Empowering students to excel academically! Dive into personalized learning tracks, assignments, and feedback for holistic success.
    """
    st.sidebar.header("About \"Student Success Network:\"")
    st.sidebar.info(description)

# Function to display formatted date
def display_date():
    formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
    st.sidebar.title("⭐The Impactful Day Of Your Life")
    st.sidebar.info(formatted_date)

# Display description and date in the sidebar
display_description()
display_date()

def main():
    col1, col2 = st.columns([2, 1])

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

    st.title("Instructions Page")

    st.markdown(
        """
        <h2 style='font-weight: bold; color: white; font-size: 24px; text-shadow: 0 0 10px rgba(255,255,255,0.6), 
        0 0 20px rgba(255,255,255,0.6), 0 0 30px rgba(255,255,255,0.6);'>Instructions:</h2>
        <hr style='border: 2px solid White;'>

        **For Admins:**
        
        - Your main responsibility is to oversee the portal's functionality.
        - Upload and process general student data using the portal.
        - Generate and distribute General and Special Reports to the respective advisors.
        
        <hr style='border: 1px solid White;'>
        
        **For Advisors:**
        
        - Provide students with personalized learning tracks.
        - Assign regular assignments to students through the portal.
        - Review and provide timely feedback on submitted assignments.
        - Monitor student progress and offer guidance.
        - Create teams for students to facilitate collaboration.
        
        <hr style='border: 1px solid White;'>
        
        **For Students:**
        
        - Log in daily using the provided credentials.
        - No need to create accounts as they are pre-created.
        - Check your email for login details.
        - Follow the portal's guidelines to access your profile.
        - Complete assignments on time.
        - Update your progress regularly and communicate with your advisor.
        - Use the portal's resources for your learning and development.

        <hr style='border: 2px solid White;'>

        **NOTE:**

          This website is under extensive development. If you encounter bugs or issues, please contact us at abc@gmail.com.
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
