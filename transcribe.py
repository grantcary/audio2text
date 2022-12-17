from utils import timer, format_timestamp, illegal_chars, path_reformat
from pytube import YouTube
import whisper as wp
import srt

from os.path import expanduser
import argparse
import os

@timer
def download_audio(url: str) -> str:
  print("Downloading...")
  
  # filters audio only formats, then downloads 160kbs webm file
  yt = YouTube(url)
  audio = yt.streams.filter(only_audio=True, file_extension='webm').last()
  audio.download(filename='audio.webm')
  return illegal_chars(yt.title)

@timer
def transcribe_audio(model_size: str) -> dict:
  print("Transcribing audio...")

  # transcribe audio with whisper, with the ability to change model size
  model = wp.load_model(model_size)
  result = model.transcribe("audio.webm")
  
  # removes audio file
  os.remove("audio.webm")

  # add timestamp/text phrase pairs to data dictionary
  data = {'start': [], 'end':[], 'subtitle': []}
  for seg in result["segments"]:
    data['start'].append(format_timestamp(seg['start']))
    data['end'].append(format_timestamp(seg['end']))
    data['subtitle'].append(seg['text'])
  return data

def compose_srt(data: dict) -> srt:
  subtitles = []
  for i, sub in enumerate(data['subtitle']):
    sub_start = srt.srt_timestamp_to_timedelta(data['start'][i])
    sub_end = srt.srt_timestamp_to_timedelta(data['end'][i])
    subtitles.append(srt.Subtitle(index=i, start=sub_start, end=sub_end, content=sub))
  return srt.compose(subtitles)

def save_srt(title: str, data: dict, out: str) -> None:
  srt_string = compose_srt(data)
  out = f'{path_reformat(out)}/{title}.srt'
  with open(out, 'w') as srt_file:
    srt_file.writelines(srt_string)

if __name__ == "__main__":
  home = f'{path_reformat(expanduser("~"))}/Desktop'

  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--url', type=str, default="https://youtu.be/dQw4w9WgXcQ", help="YouTube URL")
  parser.add_argument('--model', type=str, default="base", help="Model size. e.g., tiny, base, small, medium, large")
  parser.add_argument('--out', type=str, default=home, help="Output destination. Default: /home/user/Desktop")  
  args = parser.parse_args()

  title = download_audio(args.url)
  data = transcribe_audio(args.model)

  save_srt(title, data, args.out)
  print("Done!")