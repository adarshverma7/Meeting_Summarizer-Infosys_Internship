import os
import requests
import whisper
import subprocess
import streamlit as st
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from dotenv import load_dotenv # type: ignore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from langchain_openai import ChatOpenAI # type: ignore
from langchain.schema import SystemMessage, HumanMessage
from concurrent.futures import ThreadPoolExecutor
import hashlib
from docx import Document # type: ignore
import webvtt # type: ignore
import msal # type: ignore
import aiohttp
import asyncio

# Load environment variables
load_dotenv()
open_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = open_api_key

# Initialize LangChain OpenAI model
llm = ChatOpenAI(model_name='gpt-3.5-turbo')

# MSAL and Graph API configurations
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
site_id = os.getenv("SITE_ID")
drive_id = os.getenv("DRIVE_ID")

# MSAL Configuration
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ["https://graph.microsoft.com/.default"]

def acquire_token():
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )
    result = app.acquire_token_for_client(scopes=scopes)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire token.")

# Function to make authenticated requests to Graph API
def make_api_call(endpoint, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to hash the content for caching purposes
def get_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

# Extract audio from video using ffmpeg
def extract_audio_from_video(video_file_path):
    audio_file_path = "output_audio.mp3"
    command = ["ffmpeg", "-i", video_file_path, "-vn", "-acodec", "libmp3lame", "-ar", "16000", "-ac", "1", audio_file_path]
    subprocess.run(command, check=True)
    return audio_file_path

# Asynchronous file download function
async def download_file_async(url, headers, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    return file_path

# Transcribe and preprocess audio using whisper
def transcribe_and_preprocess(audio_file):
    model = whisper.load_model("base")
    transcribed_text = model.transcribe(audio_file)["text"]
    tokens = word_tokenize(transcribed_text.lower().translate(str.maketrans('', '', string.punctuation)))
    stop_words = set(stopwords.words('english'))
    preprocessed_text = ' '.join([token for token in tokens if token not in stop_words])
    return transcribed_text, preprocessed_text

# Process .docx file
def process_docx(file):
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

# Process .vtt file
def process_vtt(file):
    vtt = webvtt.read_buffer(file)
    full_text = [caption.text for caption in vtt]
    return '\n'.join(full_text)

# Generate summary using the language model
def generate_summary(transcript):
    response = llm.invoke([
        SystemMessage(content='You are an expert assistant that can summarize meetings.'),
        HumanMessage(content=f'Please provide a detailed summary of the following Online Meet recording in a paragraph:\n TEXT: {transcript}\nInclude key decisions, action items, and any notable insights discussed.')
    ])
    return response.content

# Generate additional details for the email
def generate_additional_details(summary):
    responses = {}
    with ThreadPoolExecutor() as executor:
        futures = {
            'category': executor.submit(lambda: llm.invoke([
                SystemMessage(content=f'Here is the detailed summary of the meeting: {summary}'),
                HumanMessage(content='Type of meeting (e.g., Sales pitch, Team meeting, Project update, Client meeting, etc.). Choose one from the options provided in a word.')
            ]).content),

            'emotion': executor.submit(lambda: llm.invoke([
                SystemMessage(content=f'Here is the detailed summary of the meeting: {summary}'),
                HumanMessage(content='Emotion or tone conveyed in this meeting? (e.g., Professional, enthusiastic, urgent, persuasive, etc.). Choose one from the options provided in a word.')
            ]).content),

            'industry': executor.submit(lambda: llm.invoke([
                SystemMessage(content=f'Here is the detailed summary of the meeting: {summary}'),
                HumanMessage(content='Industry related to this meeting? (e.g., Technology, healthcare, finance, etc.). Choose one from the options provided in a word.')
            ]).content),

            'focus': executor.submit(lambda: llm.invoke([
                SystemMessage(content=f'Here is the detailed summary of the meeting: {summary}'),
                HumanMessage(content='Focus of this meeting? (e.g., Introducing a new product, discussing performance, setting goals, etc.). Choose one from the options provided in a word.')
            ]).content),

            'plan': executor.submit(lambda: llm.invoke([
                SystemMessage(content=f'Here is the detailed summary of the meeting: {summary}\nBased on this summary, what is the proposed plan of action?'),
                HumanMessage(content='Please outline a brief plan of action based on the topics discussed. Limit the plan to no more than five points, with each point consisting of no more than 1 or 2 lines.')
            ]).content)
        }
        for key, future in futures.items():
            responses[key] = future.result()
    return responses

# Email sending function
def send_email(subject, body, recipient_list):
    msg = MIMEMultipart()
    msg['From'] = "adarshsamrat678@gmail.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Use the generated app password here
    password = os.getenv("EMAIL_PASSWORD")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(msg['From'], password)
            msg['Bcc'] = ', '.join(recipient_list)
            server.sendmail(msg['From'], recipient_list, msg.as_string())
            st.success("Email sent to all recipients successfully.")
    except Exception as e:
        st.error(f"SMTP Error: {e}")


# Streamlit App
st.title("Meeting Summarizer and Emailer")
st.write("Upload a video file, or a transcription file directly in .docx or .vtt format, or select a video from OneDrive. This app will summarize the meeting and send the summary via email.")

# Add custom CSS for better visual presentation
st.markdown("""
    <style>
        .summary-box {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f0f8ff;
            margin-bottom: 20px;
        }
        .section-heading {
            font-size: 1.5em;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #007acc;
        }
        .email-section {
            margin-top: 40px;
            color: #007acc;
        }
        .stButton>button {
            background-color: #007acc;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #005b99;
        }
        .additional-details {
            margin-bottom: 20px;
        }
        .plan-of-action {
            margin-top: 10px;
        }
        .plan-of-action-item {
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

file_option = st.radio(
    "Choose the type of file to upload",
    ('Video File', 'Transcription File (.docx)', 'Transcription File (.vtt)', 'OneDrive Video File')
)

# Initialize state variables
if "show_summary" not in st.session_state:
    st.session_state["show_summary"] = False

if file_option == 'OneDrive Video File':
    access_token = acquire_token()
    if access_token:
        list_items_endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/Recordings:/children'
        items_response = make_api_call(list_items_endpoint, access_token)
        if items_response:
            video_files = [item for item in items_response['value'] if item['name'].lower().endswith(('.mp4', '.mov', '.avi'))]
            selected_video_file = st.selectbox('Select a video file from OneDrive', [file['name'] for file in video_files])
            selected_file_data = next((file for file in video_files if file['name'] == selected_video_file), None)
            if selected_file_data:
                file_id = selected_file_data['id']
                file_download_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{file_id}/content'
                video_file_path = f"{selected_video_file}"

                if st.button("Process File"):
                    with st.spinner('Downloading and Processing...'):
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(download_file_async(file_download_url, {'Authorization': 'Bearer ' + access_token}, video_file_path))
                        loop.close()

                        audio_file_path = extract_audio_from_video(video_file_path)
                        transcript, preprocessed_text = transcribe_and_preprocess(audio_file_path)
                        st.session_state.transcript = transcript
                        st.session_state.preprocessed_text = preprocessed_text
                        st.session_state["show_summary"] = True
else:
    uploaded_file = st.file_uploader("Choose a file", type=["mp4", "mov", "avi", "docx", "vtt"])
    if uploaded_file and st.button("Process File"):
        with st.spinner('Processing...'):
            if file_option == 'Video File':
                audio_file_path = extract_audio_from_video(uploaded_file.read())
                transcript, preprocessed_text = transcribe_and_preprocess(audio_file_path)
                st.session_state.transcript = transcript
                st.session_state.preprocessed_text = preprocessed_text
                st.session_state["show_summary"] = True
            elif file_option == 'Transcription File (.docx)':
                transcript = process_docx(uploaded_file)
                preprocessed_text = transcript
                st.session_state.transcript = transcript
                st.session_state.preprocessed_text = preprocessed_text
                st.session_state["show_summary"] = True
            elif file_option == 'Transcription File (.vtt)':
                transcript = process_vtt(uploaded_file)
                preprocessed_text = transcript
                st.session_state.transcript = transcript
                st.session_state.preprocessed_text = preprocessed_text
                st.session_state["show_summary"] = True

if st.session_state["show_summary"]:
    st.markdown("<div class='section-heading'>Meeting Summary</div>", unsafe_allow_html=True)
    summary = generate_summary(st.session_state.transcript)
    st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-heading'>Additional Details</div>", unsafe_allow_html=True)
    additional_details = generate_additional_details(summary)
    st.write(f"<div class='additional-details'><strong>Category</strong>: {additional_details['category']}</div>", unsafe_allow_html=True)
    st.write(f"<div class='additional-details'><strong>Emotion</strong>: {additional_details['emotion']}</div>", unsafe_allow_html=True)
    st.write(f"<div class='additional-details'><strong>Industry</strong>: {additional_details['industry']}</div>", unsafe_allow_html=True)
    st.write(f"<div class='additional-details'><strong>Focus</strong>: {additional_details['focus']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-heading plan-of-action'>Plan of Action</div>", unsafe_allow_html=True)
    for point in additional_details['plan'].split('\n'):
        st.markdown(f"<div class='plan-of-action-item'>{point}</div>", unsafe_allow_html=True)

    st.markdown("<div class='email-section'>Send Email</div>", unsafe_allow_html=True)
    recipient_list = st.text_area("Enter recipient email addresses (comma-separated)").split(',')
    if st.button("Send Email"):
        subject = "Meeting Summary"
        plan_of_action_html = additional_details['plan'].replace('\n', '<br>')
        body = f"""
            <div class='additional-details'><strong>Category</strong>: {additional_details['category']}</div>
            <div class='additional-details'><strong>Emotion</strong>: {additional_details['emotion']}</div>
            <div class='additional-details'><strong>Industry</strong>: {additional_details['industry']}</div>
            <div class='additional-details'><strong>Focus</strong>: {additional_details['focus']}</div>
            <p><strong>Summary:</strong></p>
            <div class='summary-box'>{summary}</div>
            <div class='section-heading plan-of-action'><p><strong>Plan of Action:</strong></p></div>
            <div class='plan-of-action-item'>{plan_of_action_html}</div>
            """
        send_email(subject, body, recipient_list)
