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

## Project Screenshots

### Summarizer Interface  
![Summarizer](<img width="960" alt="3" src="5 ">)

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

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Meeting-Summarizer.git
   cd Meeting-Summarizer
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Install ffmpeg:

Windows: Download from ffmpeg.org and add it to the system PATH.
macOS: Install via Homebrew:
bash
Copy code
brew install ffmpeg
Linux:
bash
Copy code
sudo apt-get install ffmpeg
Usage
Place your video files in the input_videos directory.
Run the main script:
bash
Copy code
python final_optimized_app.py
The processed audio, transcriptions, summaries, and plans of action will be saved in their respective directories.
The email containing the summarized information and plan of action will be sent to predefined recipients.
Tools and Frameworks
Frameworks/Libraries:
Streamlit: For building the user interface.
NLTK (Natural Language Toolkit): For text preprocessing and analysis.
OpenAI API: For summarization and action plan generation.
Whisper: For speech-to-text transcription.
Tools/Platforms:
GitHub: For version control and collaborative development.
VS Code: Integrated Development Environment (IDE).
AWS/Azure: For deploying the application with scalability and reliability.
Microsoft OneDrive and SMTP (for Gmail): For email integration and file management.
Configuration
Modify the script to set up your email credentials and recipients in the following section:

python
Copy code
email_sender = "your_email@gmail.com"
email_password = "your_password"
email_recipients = ["recipient1@gmail.com", "recipient2@gmail.com"]
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature/YourFeature
Commit your changes:
bash
Copy code
git commit -m "Add YourFeature"
Push the branch:
bash
Copy code
git push origin feature/YourFeature
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
OpenAI: For Whisper and GPT-3.5 Turbo models.
FFmpeg: For high-quality audio processing.
Infosys: For the internship opportunity and project support.
javascript
Copy code

You can adjust placeholders like `your-username`, `your_email@gmail.com`, a
