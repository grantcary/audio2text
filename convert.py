from os.path import expanduser
from pathlib import Path
import argparse

from utils import format_timestamp, path_reformat
from transcribe import save_srt, save_csv
from pandas import DataFrame, read_csv
import srt


def csv_to_srt(in_path: str, out_path: srt) -> None:
  csv_data = read_csv(in_path)
  title = Path(in_path).stem
  save_srt(title, csv_data, out_path)

def srt_to_csv(in_path: str, out_path: str) -> None:
  with open(in_path, 'r') as srt_file:
    srt_data = srt_file.read()
  
  data = {'start': [], 'end':[], 'subtitle': []}
  for seg in srt.parse(srt_data):
    data['start'].append(format_timestamp(seg.start.total_seconds()))
    data['end'].append(format_timestamp(seg.end.total_seconds()))
    data['subtitle'].append(seg.content)
  
  title = Path(in_path).stem
  save_csv(title, DataFrame(data), out_path)

if __name__ == "__main__":
  home = f'{path_reformat(expanduser("~"))}/Desktop'

  parser = argparse.ArgumentParser(description='Run Audio2Text', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--file', type=str, required=True, help="Input file path")
  parser.add_argument('--out', type=str, default=home, help="Output destination")
  args = parser.parse_args()

  file_extension = Path(args.file).suffix
  if file_extension == '.srt':
    srt_to_csv(args.file, args.out)
  elif file_extension == '.csv':
    csv_to_srt(args.file, args.out)