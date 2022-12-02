from utils import timer, format_timestamp, illegal_chars, path_reformat
from pytube import YouTube
import whisper as wp
import pandas as pd

from os.path import expanduser
import argparse
import os


@timer
def download_audio(url):
  print("Downloading...")

  # filters audio only formats, then downloads 160kbs webm file
  yt = YouTube(url)
  audio = yt.streams.filter(only_audio=True, file_extension='webm').last()
  audio.download(filename='audio.webm')

  return illegal_chars(yt.title)


@timer
def transcribe_audio(model_size):
  print("Transcribing audio...")

  # transcribe audio with whisper, with the ability to change model size
  model = wp.load_model(model_size)
  result = model.transcribe("audio.webm")
  
  # removes audio file
  os.remove("audio.webm")

  data = {'timestamp': [], 'text': []}

  # add timestamp/text phrase pairs to data dictionary
  for seg in result["segments"]:
    data['timestamp'].append(format_timestamp(seg['start']))
    data['text'].append(seg['text'])

  return data


def save_transcription(title, data, out):
  out = f'{path_reformat(out)}/{title}.csv'

  print("Saving...")
  
  # convert data dictionary to dataframe then export to a CSV file 
  df = pd.DataFrame(data)
  df.to_csv(out, index=False)
  
  print(f"    Saved to: {out}")


if __name__ == "__main__":
  home = f'{path_reformat(expanduser("~"))}/Desktop'

  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--url', type=str, default="https://youtu.be/dQw4w9WgXcQ", help="YouTube URL")
  parser.add_argument('--model', type=str, default="base", help="Model size. e.g., tiny, base, small, medium, large")
  parser.add_argument('--out', type=str, default=home, help="Output destination. Default: /home/user/Desktop")  
  args = parser.parse_args()

  title = download_audio(args.url)
  data = transcribe_audio(args.model)
  save_transcription(title, data, args.out)
  
  print("Done!")