### YouTube Audio to Subtitles
Terminal based YouTube audio transcriber using [Whisper](https://github.com/openai/whisper)!
```
python3 transcribe.py --url "https://youtu.be/x7X9w_GIm1s" --model "base" --out "/home/user/Desktop"
```
Outputs a subtitle file (.srt) and an CSV file with subtitle phrase level start and end timestamps.
