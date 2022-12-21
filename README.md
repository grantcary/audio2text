### YouTube Audio to Subtitles
Terminal based YouTube audio transcriber using [Whisper](https://github.com/openai/whisper)!

## Setup
```
git clone https://github.com/grantcary/youwhisp.git
cd youwhisp
pip3 install -r requirements.txt
```
It also requires Whisper to be installed. Refer to OpenAI's Whisper documentation on the [installation process](https://github.com/openai/whisper).

## Command-line usage
```
usage: python3 transcribe.py [--url] [--model] [--format] [--out]

options:
    --url         # any valid youtube url
    --model       # tiny, base, small, medium, large-v1, large-v2, large
    --format      # src, csv
    --out         # any valid folder path
```

## Convert file type
```
usage: python3 convert.py example.csv

options:
    --file (req)  # any file path with valid file extensions [.srt, .csv]
    --out         # any valid folder path

conversion logic:
    Input         Output
    .csv          .srt
    .srt          .csv
```