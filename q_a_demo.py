from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI API
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Initialize the generative model
model = genai.GenerativeModel('gemini-pro')

# Function to load Gemini Pro model response
@st.cache_data(ttl=300)  # Cache the response for 5 minutes
def load_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app configuration
st.set_page_config(
    page_title="Q&A Demo",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar configuration
st.sidebar.header("Settings")
response_length = st.sidebar.slider("Response Length", min_value=1, max_value=500, value=200, step=10)

# App header
st.header('Q&A Demo')

# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []

# Input form
with st.form(key='question_form'):
    input_question = st.text_input("Ask a question:", key="input")
    submit_button = st.form_submit_button(label='Ask')

# When the submit button is clicked
if submit_button:
    if not input_question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            response = load_gemini_response(input_question)
        st.session_state.history.append({"question": input_question, "response": response})

# Display the history of questions and responses
if st.session_state.history:
    st.subheader("Chat History")
    for i, entry in enumerate(st.session_state.history):
        st.markdown(f"**Question {i+1}:** {entry['question']}")
        st.markdown(f"**Response:** {entry['response']}")

# Clear history button
if st.button("Clear History"):
    st.session_state.history = []

# Custom CSS for better styling
st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .st-form {
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .stMarkdown {
            padding: 10px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
