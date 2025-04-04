#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
import multiprocessing

from youtube_blogger.src.youtube_blogger.crew import YoutubeBlogger


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

import os
import yt_dlp
import speech_recognition as sr
from pydub import AudioSegment
# from crewai import Agent, Task, Crew

# Create output folders
os.makedirs("downloads", exist_ok=True)
os.makedirs("blogs", exist_ok=True)

# Step 1: Download YouTube Audio
def download_audio(youtube_url, output_path="downloads/audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': output_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print("Audio Downloaded")
    print(output_path)
    return output_path

# Step 2: Split Long Audio into Chunks
def split_audio(audio_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    print("Splitting Successfully")
    return chunks


# # Step 3: Convert Speech to Text
# def transcribe_audio(audio_chunks):
#     recognizer = sr.Recognizer()
#     transcript = ""

#     for i, chunk in enumerate(audio_chunks):
#         chunk_path = f"downloads/chunk_{i}.wav"
#         chunk.export(chunk_path, format="wav")

#         with sr.AudioFile(chunk_path) as source:
#             audio_data = recognizer.record(source)

#             try:
#                 text = recognizer.recognize_google(audio_data)
#                 transcript += text + "\n"
#             except sr.UnknownValueError:
#                 print(f"Could not understand audio in chunk {i}")
#             except sr.RequestError:
#                 print("Could not request results from Google Speech Recognition service")
#     print(transcript)
#     return transcript


def transcribe_chunk(args):
    """Function to transcribe a single audio chunk."""
    chunk, index = args
    recognizer = sr.Recognizer()
    chunk_path = f"downloads/chunk_{index}.wav"
    chunk.export(chunk_path, format="wav")

    with sr.AudioFile(chunk_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return f"[Chunk {index}] Could not understand audio"
        except sr.RequestError:
            return "[Error] Could not request results from Google Speech Recognition service"

def transcribe_audio(audio_chunks, num_workers=4):
    """Processes audio chunks in parallel."""
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(transcribe_chunk, [(chunk, i) for i, chunk in enumerate(audio_chunks)])

    transcript = "\n".join(results)
    print(transcript)
    return transcript


# def run():
#     """
#     Run the crew.
#     """
#     youtube_url = input("Enter YouTube URL: ")
#     audio_path = download_audio(youtube_url)
#     audio_chunks = split_audio(audio_path)
#     transcript = transcribe_audio(audio_chunks)

#     inputs={"task_summarize": transcript}
    
#     try:
#         YoutubeBlogger().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")


# run()