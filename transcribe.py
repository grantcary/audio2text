import os
import argparse
from os.path import expanduser

from utils import format_timestamp, illegal_chars, path_reformat
from tempfile import TemporaryDirectory
from pandas import DataFrame
from pytube import YouTube
import whisper as wp
import srt


def download_audio(url: str, tmp_dir: str) -> str:
  print("downloading...")
  # filters audio only formats, then downloads 160kbs webm file
  yt = YouTube(url)
  audio = yt.streams.filter(only_audio=True, file_extension='webm').last()
  audio.download(filename=f'{tmp_dir}/audio.webm')
  return illegal_chars(yt.title)


def transcribe_audio(model_size: str, tmp_dir: str) -> dict:
  print("transcribing audio...")
  model = wp.load_model(model_size)
  result = model.transcribe(f'{tmp_dir}/audio.webm')
  return result

def compose_data(result) -> DataFrame:
  # timestamp/text phrase pair data dictionary
  data = {'start': [], 'end':[], 'subtitle': []}
  for seg in result["segments"]:
    data['start'].append(format_timestamp(seg['start']))
    data['end'].append(format_timestamp(seg['end']))
    data['subtitle'].append(seg['text'])
  return DataFrame(data)

def compose_srt(data: DataFrame) -> str:
  subtitles = []
  for i in range(len(data.index)):
    sub_start, sub_end, sub = data.iloc[i]
    sub_start, sub_end = srt.srt_timestamp_to_timedelta(sub_start), srt.srt_timestamp_to_timedelta(sub_end)
    subtitles.append(srt.Subtitle(index=i+1, start=sub_start, end=sub_end, content=sub))
  return srt.compose(subtitles)

def save_srt(title: str, data: DataFrame, out: str) -> str:
  srt_string = compose_srt(data)
  out = f'{path_reformat(out)}/{title}.srt'
  with open(out, 'w') as srt_file:
    srt_file.writelines(srt_string)
  return out

def save_csv(title: str, data: DataFrame, out: str) -> str:
  out = f'{path_reformat(out)}/{title}.csv'
  data.to_csv(out, index=False)
  return out

if __name__ == "__main__":
  home = f'{path_reformat(expanduser("~"))}/Desktop'

  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--url', required=True, type=str, help="YouTube URL")
  parser.add_argument('--model', type=str, default="base", help="Model size. e.g., tiny, base, small, medium, large")
  parser.add_argument('--format', type=str, default="srt", help="Output file format")  
  parser.add_argument('--out', type=str, default=home, help="Output destination")
  args = parser.parse_args()
 
  # create temporary directory
  tmp_dir = TemporaryDirectory()
  tmp = tmp_dir.name
  
  title = download_audio(args.url, tmp)
  data = compose_data(transcribe_audio(args.model, tmp))

  # close temporary directory
  tmp_dir.cleanup()

  out = save_csv(title, data, args.out) if args.format == "csv" else save_srt(title, data, args.out)
  print(f"saved to absolute path: {out}")