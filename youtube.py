import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
import whisper
from transformers import pipeline
import datetime

# ==== Step 1: Download YouTube Audio ====
def download_audio(youtube_url, download_folder="downloads"):
    yt = YouTube(youtube_url)
    title = yt.title.replace(" ", "_").replace("|", "")
    audio_stream = yt.streams.filter(only_audio=True).first()

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    audio_path = audio_stream.download(output_path=download_folder, filename=title + ".mp4")

    # Convert to .wav for Whisper
    wav_path = os.path.join(download_folder, title + ".wav")
    clip = AudioFileClip(audio_path)
    clip.write_audiofile(wav_path)
    clip.close()

    return wav_path, title

# ==== Step 2: Transcribe with Whisper ====
def transcribe_audio(audio_path):
    print("🔍 Transcribing audio...")
    model = whisper.load_model("base")  # Or use "small" for better results
    result = model.transcribe(audio_path)
    return result["text"]

# ==== Step 3: Summarize Transcript ====
def summarize_text(text):
    print("🧠 Summarizing text...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""

    for chunk in chunks:
        out = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary += out[0]["summary_text"] + " "

    return summary.strip()

# ==== Step 4: Save Output ====
def save_output(title, transcript, summary, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{title}_{time_stamp}"

    transcript_path = os.path.join(output_dir, base_name + "_transcript.txt")
    summary_path = os.path.join(output_dir, base_name + "_summary.txt")

    with open(transcript_path, "w", encoding="utf-8") as t_file:
        t_file.write(transcript)

    with open(summary_path, "w", encoding="utf-8") as s_file:
        s_file.write(summary)

    print(f"\n✅ Transcript saved to: {transcript_path}")
    print(f"✅ Summary saved to: {summary_path}")

# ==== 🔁 Main Function ====
def main():
    print("🎧 Smart YouTube Podcast Summarizer 🎧")
    youtube_url = input("📺 Enter the YouTube video URL: ").strip()

    try:
        audio_path, title = download_audio(youtube_url)
        transcript = transcribe_audio(audio_path)
        summary = summarize_text(transcript)
        save_output(title, transcript, summary)
        print("\n🌟 Done! Your video has been summarized successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
