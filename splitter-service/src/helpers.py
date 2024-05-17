import os

import src.constants as c

def make_dirs():
  try:
    os.makedirs(c.INPUT_DIR, exist_ok=True)
    os.makedirs(c.OUTPUT_DIR, exist_ok=True)
  except Exception as err:
    print(err) # TODO: Add to logs

async def delete_input_file(file_name):
  try:
    os.remove(c.INPUT_DIR + '/' + file_name)
  except Exception as err:
    return False
