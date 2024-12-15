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
git clone https://github.com/your-username/Meeting-Summarizer.git cd Meeting-Summarizer

yaml
Copy code

---

### 2. Install Required Python Dependencies
Install all the required Python libraries listed in the `requirements.txt` file:
pip install -r requirements.txt

markdown
Copy code

**Key Dependencies:**
- `ffmpeg-python`
- `pydub`
- `nltk`
- `openai`
- `smtplib`

Ensure `pip` is updated to the latest version for smooth installation:
`pip install --upgrade pip`

yaml
Copy code

---

### 3. Install FFmpeg
FFmpeg is required for audio and video processing. Install it based on your operating system:

- **Windows**:  
  1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org).  
  2. Extract the files and add the FFmpeg binary to your system PATH.  
  3. Verify installation by running:
     ```
     ffmpeg -version
     ```

- **macOS**:  
  Install FFmpeg using Homebrew:
`brew install ffmpeg`

markdown
Copy code

- **Linux**:  
Install FFmpeg using the following command:
`sudo apt-get install ffmpeg`

yaml
Copy code

---

### 4. Set Up NLTK
NLTK is used for text processing. After installing NLTK, download the necessary corpora:
`import nltk nltk.download('punkt')`

yaml
Copy code

---

### 5. Install Whisper
Whisper is used for transcription. Install it via pip:
`pip install whisper`

yaml
Copy code

---

### 6. Set Up OpenAI API
OpenAI API is used for summarization and action plan generation.

1. Sign up for an API key at [OpenAI](https://platform.openai.com/signup/).  
2. Add your API key to the script (or environment variables). Example:
`openai.api_key = "your_api_key_here"`

yaml
Copy code

---

### 7. Configure Email Sending
The `smtplib` library is used for sending emails. Configure the script with your email credentials:
`email_sender = "your_email@gmail.com" email_password = "your_password" email_recipients = ["recipient1@gmail.com", "recipient2@gmail.com"]`

yaml
Copy code

**Note**: For Gmail, ensure that "Allow less secure apps" is enabled or use an app-specific password for better security.

---

### 8. Install Streamlit
Streamlit is used for building the user interface. Install it with:
`pip install streamlit`

arduino
Copy code

To run the Streamlit app, use:
`streamlit run your_app.py`

yaml
Copy code

---

### 9. Set Up Cloud Deployment (Optional)
If deploying to the cloud:
- **AWS or Azure**: Follow the respective deployment guides for setting up Python applications.
- **Streamlit Cloud**: Push your code to GitHub and deploy using [Streamlit Cloud](https://streamlit.io/cloud).

---

### 10. Verify Everything Works
Test the installation by running the main script:
`python Meeting_Summarizer.py`

css
Copy code

Output files (audio, transcripts, summaries, and action plans) will be saved in their respective directories, and emails will be sent to the predefined recipients.
