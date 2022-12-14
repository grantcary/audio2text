### YouTube Audio Transcriber w/ Timestamps
Terminal based YouTube audio transcriber using [Whisper](https://github.com/openai/whisper)!
```
# any of the arguments below can be omitted
python3 transcribe.py --url "https://youtu.be/x7X9w_GIm1s" --model "base" --out "/home/user/Desktop"
```
Outputs an SRT file and an CSV file with subtitle phrase level start and end timestamps.
