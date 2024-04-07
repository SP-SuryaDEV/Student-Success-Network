import anthropic
import streamlit as st
import datetime
import random

# Set Streamlit page configuration
st.set_page_config(
    page_title="Student Success Network",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

now = datetime.datetime.now()
formatted_date = now.strftime('%Y-%m-%d')

# Define custom styles
custom_styles = f"""
<style>
.stApp {{
  background-image: url("https://i.gifer.com/2iiB.gif");
  background-size: cover;
  background-position: center;
}}

.chat-container {{
    max-width: 800px;
    height: 500px;
    overflow-y: auto;
    margin-top: 50px;
    margin-bottom: 50px;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}}

.user-message {{
    background-color: #e6f7ff;
    color: #0066cc;
    padding: 10px;
    margin: 5px;
    border-radius: 10px;
}}

.assistant-message {{
    background-color: #f0f0f0;
    color: #333333;
    padding: 10px;
    margin: 5px;
    border-radius: 10px;
}}
</style>
"""

st.markdown(custom_styles, unsafe_allow_html=True)

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
# Initialize AnthropiC client
client = anthropic.Anthropic(
    api_key = st.secrets.API_KEY,
)

# Function to display quote
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

# Function to display formatted date
def display_date():
    formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
    text_with_date = f"""
    <h1 style='text-align: center; font-size: 2rem; margin-top: -20px;'>⭐A Day to be Remembered</h1>
    <p style='text-align: center; font-size : 2rem; margin-top: -20px;'>{formatted_date}</p>
    """
    st.markdown(text_with_date, unsafe_allow_html=True)

# Display quote and date in two columns
col1, col2 = st.columns(2)

with col1:
    display_quote()


with col2:
    
    display_date()

st.title("College Work Assistant - Chat")
st.warning("This Is a general Purpose Assistant and whoever can use it but we are not responsible")

def extract_text(content_blocks):
    return '\n'.join([block.text for block in content_blocks])

def add_to_chat(messages, prompt, response):
    messages.append({'role':'user','content':prompt})
    messages.append({'role':'assistant','content':response})

if 'messages' not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input('You:')
if prompt:
    with st.spinner("Thinking..."):
        anthropic_response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}, {"role": "assistant", "content": ""}]
        )
    
    add_to_chat(st.session_state.messages, prompt, extract_text(anthropic_response.content))

with st.container():
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f"<div class='user-message'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        elif message['role'] == 'assistant':
            st.markdown(f"<div class='assistant-message'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)
