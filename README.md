# Meeting Summarizer and Plan of Action Generator

![demo gif](https://github.com/user-attachments/assets/2374537f-7f58-4cdd-b46b-290522b91f3f)


This project aims to develop a web application that generates concise summaries of meetings and produces actionable plans based on the discussed topics. The summarized information and plans of action are automatically sent to the attendees via email.

![Workflow](https://github.com/user-attachments/assets/142376ae-86cc-4da2-a65b-da612ee2a535)

---

## Features

- **Video/Audio Processing**  
  Converts video files to audio using `ffmpeg` and removes silent regions using `pydub`.
  
- **Transcription**  
  Uses OpenAI's Whisper base model for accurate speech-to-text transcription.
  
- **Summarization**  
  Leverages OpenAI's GPT-3.5 Turbo model to generate concise meeting summaries.
  
- **Sentiment and Tone Analysis**  
  Analyzes the sentiment and tone of the transcribed content.
  
- **Plan of Action**  
  Automatically generates a plan of action based on the meeting discussion.
  
- **Email Sending**  
  Summarized content and plans of action are emailed to predefined recipients using the `smtplib` library.

---

## Audio Processing and Text Preprocessing

### Audio Processing  
1. **Conversion to Audio**  
   Video files are converted to audio using `ffmpeg`, enabling easier processing without requiring visual data.  

2. **Silent Region Removal**  
   `pydub` is used to remove silent segments from the audio files, focusing on meaningful speech for improved transcription and analysis accuracy.  

### Text Preprocessing  
Before applying NLP techniques for summarization and action plan generation, the transcribed text is preprocessed:  
- **Tokenization**: Splits the text into individual tokens (words or phrases).  
- **Stopword Removal**: Removes common stopwords like "the", "is", "and" to reduce noise and enhance relevance.

These preprocessing steps optimize the performance of summarization and sentiment analysis models, ensuring concise, accurate, and meaningful outputs.

---

## Workflow  

1. **Audio Extraction**  
   - **FFmpeg**: A powerful multimedia framework used to decode, encode, transcode, stream, and filter content.  
   - **Subprocess**: Python's `subprocess` module is used to run `ffmpeg` commands directly from the script.  

   Benefits:  
   - Automation of tasks.  
   - Seamless integration with the project.  
   - Resource-efficient parallel execution.  

2. **Transcription and Summarization**  
   - **Whisper**: For real-time, high-accuracy speech-to-text conversion.  
   - **OpenAI GPT-3.5 Turbo**: For generating summaries and actionable plans.

3. **Email Automation**  
   - Processed content is emailed to recipients automatically using the `smtplib` library.

---

## Installation

Follow these steps to set up the project on your local machine:

---

### 1. Clone the Repository
Clone the project repository to your local system:
bash
git clone https://github.com/your-username/Meeting-Summarizer.git
cd Meeting-Summarizer

2. Install Required Python Dependencies
Install all the required Python libraries listed in the requirements.txt file:

bash
Copy code
pip install -r requirements.txt
Key Dependencies:

ffmpeg-python
pydub
nltk
openai
smtplib
Ensure pip is updated to the latest version for smooth installation:

bash
Copy code
pip install --upgrade pip

3. Install FFmpeg
FFmpeg is required for audio and video processing. Install it based on your operating system:

Windows:

Download FFmpeg from ffmpeg.org.
Extract the files and add the FFmpeg binary to your system PATH.
Verify installation by running:
bash
Copy code
ffmpeg -version
macOS:
Install FFmpeg using Homebrew:

bash
Copy code
brew install ffmpeg
Linux:
Install FFmpeg using the following command:

bash
Copy code
sudo apt-get install ffmpeg

4. Set Up NLTK
NLTK is used for text processing. After installing NLTK, download the necessary corpora:

python
Copy code
import nltk
nltk.download('punkt')

5. Install Whisper
Whisper is used for transcription. Install it via pip:

bash
Copy code
pip install whisper

6. Set Up OpenAI API
OpenAI API is used for summarization and action plan generation.

Sign up for an API key at OpenAI.
Add your API key to the script (or environment variables). Example:
python
Copy code
openai.api_key = "your_api_key_here"

7. Configure Email Sending
The smtplib library is used for sending emails. Configure the script with your email credentials:

python
Copy code
email_sender = "your_email@gmail.com"
email_password = "your_password"
email_recipients = ["recipient1@gmail.com", "recipient2@gmail.com"]
Note: For Gmail, ensure that "Allow less secure apps" is enabled or use an app-specific password for better security.

8. Install Streamlit
Streamlit is used for building the user interface. Install it with:

bash
Copy code
pip install streamlit
To run the Streamlit app, use:

bash
Copy code
streamlit run your_app.py
