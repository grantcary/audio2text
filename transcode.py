from os.path import expanduser
from datetime import timedelta
import argparse
import time
import os

from pytube import YouTube
import whisper as wp
import pandas as pd

def path_reformat(path): return path.replace('\\', '/')
home = f'{path_reformat(expanduser("~"))}/Desktop'

def illegal_chars(title):
  for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
    title = title.replace(c, ' ')
  return title

def download_audio(url):
  print("Downloading...")
  yt = YouTube(url)
  audio = yt.streams.filter(only_audio=True, file_extension='webm').last()
  audio.download(filename='audio.webm')
  
  return illegal_chars(yt.title)

def encode_audio(model):
  print("Transcribing audio...")
  model = wp.load_model(model)
  result = model.transcribe("audio.webm")
  os.remove("audio.webm")

  data = {'timestamp': [], 'text': []}

  print("Segmenting...")
  for seg in result["segments"]:
    # timestamp = str(timedelta(seconds=seg['start'])
    data['timestamp'].append(time.strftime('%H:%M:%S', time.gmtime(seg['start'])))
    data['text'].append(seg['text'])

  return data

def save_transcription(title, data):
  print("Saving...")
  df = pd.DataFrame(data)
  df.to_csv(f'{title}.csv', index=False)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--url', type=str, default="https://youtu.be/dQw4w9WgXcQ", help="URL for transcriptable youtube video")
  parser.add_argument('--model', type=str, default="base", help="Choose a model: tiny, base, small, medium, large")
  args = parser.parse_args()

  title = download_audio(args.url)
  data = encode_audio(args.model)
  save_transcription(title, data)
    
  print("Done!")