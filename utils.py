from datetime import datetime
from time import time

# function timer
def timer(func):
  def wrapper(*args, **kwargs):
    st = time()
    result = func(*args, **kwargs)
    print(f'    {func.__name__!r} executed in {(time()-st):.2f}s')
    return result
  return wrapper

# safeguard for windows users
def path_reformat(path: str) -> str: return path.replace('\\', '/')

# saveguard for windows/linux users
def illegal_chars(title: str) -> str:
  for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
    title = title.replace(c, ' ')
  return title

# converts int/float to timestamp, normalized with norm mask, then converted to a time object for string formatting
def format_timestamp(num: float) -> str:
  ts = datetime.fromtimestamp(num)
  norm = datetime(1969, 12, 31, 16, 0, 0)
  return ((datetime.min+(ts-norm)).time()).strftime('%H:%M:%S,%f')[:-3]