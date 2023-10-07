"""Common function"""

import os
import uuid
import base64
import datetime
import numpy as np


def get_datetime():
  return str(datetime.now()).split('.', maxsplit=1)[0]


def get_uuid():
  return uuid.uuid4().hex


def get_file_size(path):
    return os.path.getsize(path)


def decode_base64_array(base64_str: str, dtype: str, shape=(-1,)):
	decoded = base64.b64decode(base64_str)
	arr = np.frombuffer(decoded, dtype=dtype)
	return arr.reshape(shape)