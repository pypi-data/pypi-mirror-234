import os
import io
import requests
from PIL import Image
from multiprocessing import Pool
import threading
from tqdm import tqdm

def download(args):
  """
  Download image from a specified website

  :param args: tuple formatted as (url, filename, target_folder, max_size) as input for process

  :return: error message or empty string if successful
  """
  # extract file extension from url
  url = args[0]
  name = args[1]
  target_folder = args[2]
  max_size = args[3]

  ext = url.split('.')[-1].split('?')[0]
  filename = os.path.join(target_folder, f"{name}.{ext}")
  if(os.path.exists(filename)):
    return("")
  # download image
  try:
    r = requests.get(url, allow_redirects=True)
    image = Image.open(io.BytesIO(r.content))
    # fix for: cannot write mode RGBA as JPEG
    image = image.convert('RGB')
    # reshape
    new_size = list(image.size)

    if(new_size[1] > max_size and new_size[1] >= new_size[0]):
      new_size[1] = max_size
      factor = max_size / float(image.size[1])
      new_size[0] = round((float(image.size[0]) * float(factor)))
    elif(new_size[0] > max_size and new_size[0] >= new_size[1]):
      new_size[0] = max_size
      factor = max_size / float(image.size[0])
      new_size[1] = round((float(image.size[1]) * float(factor)))

    # set width to keep aspect ratio
    image = image.resize(tuple(new_size), Image.Resampling.LANCZOS)
    image.save(filename, quality=95)
    return("")
  except Exception as e:
    return(f"{filename}: {e}\r\n")
  
def download_parallel(url_args, length):
  """
  Download images from a website on multiple processes

  :param url_args: zip(tuple) formatted as (url, filename, target_folder, max_size) as input for process
  :param length: number of images to download

  :return: error message or empty string if successful
  """
  fails = ""
  n_fails = 0
  lock = threading.Lock()
  pb = tqdm(total=length, desc="Downloading", unit="step")
  i = 0
  pool = Pool(60)  # set the processes number
  for result in pool.imap_unordered(download, url_args):
    lock.acquire()
    fails += result
    i += 1
    pb.update(1)
    lock.release()

  n_fails = len(fails.split('\r\n'))
  print(f"{n_fails} images failed to download.")
  print(fails)
  return fails