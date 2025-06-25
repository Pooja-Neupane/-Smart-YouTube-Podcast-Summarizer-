# 🎧 Smart YouTube Podcast Summarizer

Save time and boost productivity by instantly summarizing long YouTube podcasts and videos into short, readable text.

---

## 🚀 Features

- 🎥 Download audio from any YouTube video
- 🔊 Transcribe spoken audio into text using OpenAI Whisper
- 🧠 Summarize long transcripts using Facebook's BART model
- 💾 Save both transcript and summary as `.txt` files
- 📂 Automatically organizes files with timestamped names

---

## 📌 How It Works

1. Enter a YouTube video link
2. Audio is extracted and converted to `.wav`
3. Whisper AI transcribes the audio
4. HuggingFace Transformers summarize the transcript
5. Files are saved in the `output/` folder

---

## 📦 Requirements

Install all dependencies:

```bash
pip install pytube moviepy openai-whisper transformers torch
