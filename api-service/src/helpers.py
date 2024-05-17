import os
from typing import Union

import src.constants as c

import ulid
from fastapi import UploadFile

def make_dirs():
  try:
    os.makedirs(c.INPUT_DIR, exist_ok=True)
  except Exception as err:
    print(err)
    pass # TODO: Add to logs

def create_hash() -> ulid.ULID:
  return ulid.new()

def split_path(path: Union[str, None]):
  return os.path.splitext(path)

def verify_file(file_ext: str, file_size: int) -> Union[dict, None]:
  if file_ext not in c.ALLOWED_EXTENSIONS:
    allowed_extensions_str = ', '.join(c.ALLOWED_EXTENSIONS)
    return {"success": False, "error": f"The file type must be one of {allowed_extensions_str}"}
  elif file_size > c.FILE_SIZE_MAX_MB * c.MB:
    return {"success": False, "error": f"The maximum allowed filesize is {c.FILE_SIZE_MAX_MB}MB"}
  else:
    return None

def create_meta(file_name: str, file_ext: str, file_size: int, stems: int, timestamp: float):
  return {
    'name': str(file_name),
    'ext': str(file_ext),
    'size': str(file_size),
    'stems': str(stems),
    'timestamp': str(timestamp)
  }

async def write_file(file: UploadFile, file_name):
  try:
    contents = await file.read()
    with open(os.path.join(c.INPUT_DIR, file_name), "wb") as f:
      f.write(contents)
    await file.close()

    return True

  except Exception as err:
    return False

async def delete_input_file(file_name):
  try:
    os.remove(c.INPUT_DIR + '/' + file_name)
  except Exception as err:
    return False
