import time
import json
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy import sparse
from urllib.parse import urljoin
from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoderMonitor

from . import get_uuid
from . import decode_base64_array
from .https_agent import HttpsAgent


def check_result_status(result):
  if not result:
    raise ConnectionError('Connection failed')

  if 'status' not in result:
    raise ValueError(result['detail'])

  if result['status'] != 200:
    if 'message' in result:
      raise Exception(f"Something went wrong: {result['message']}")
    else:
      raise Exception('Something went wrong')


def parse_submission_status(submission_status):
  """
    Parse submission status response
  """
  if not submission_status:
    print('Connection failed')
    return None

  if 'status' not in submission_status:
    print('Internal server error. Please check server log.')
    return None

  if submission_status['status'] != 200:
    if 'message' in submission_status:
      print(f"Submission failed. {submission_status['message']}")
      return None
    else:
      print('Submission failed.')
      return None

  return submission_status['data']['id']


def parse_query_genes_result(query_genes_result):
  """Parse query genes result
  """
  check_result_status(query_genes_result)

  indptr = decode_base64_array(query_genes_result['data']['indptr'], 'uint64')
  indices = decode_base64_array(query_genes_result['data']['indices'], 'uint32')
  data = decode_base64_array(query_genes_result['data']['data'], 'float32')
  shape = query_genes_result['data']['shape']
  csc_mtx = sparse.csc_matrix((data, indices, indptr), shape=shape)
  return csc_mtx


def _add_file_upload(folder_id, n_chunks, file_name, token, host):
  headers = {
    'bioturing-api-token': token
  }
  params = {
    'folder_id': folder_id,
    'n_chunks': n_chunks,
    'original_file_name': file_name
  }
  response = requests.post(
    urljoin(host, 'api/v1/add_file_upload'),
    json=params,
    headers=headers
  )
  try:
    response = response.json()
  except requests.exceptions.RequestException as e:
    print(e)

  check_result_status(response)
  id = response['data'][0]['id']
  return id


def _upload_each_file_in_chunk(
    folder_id,
    id,
    file_path,
    file_name,
    token,
    host,
    chunk_size,
    n_chunks
  ):
  file = open(file_path, 'rb')
  for chunk_order in range(n_chunks):
    chunk = file.read(chunk_size)

    if not chunk:
      raise Exception('Something went wrong')

    with tqdm(
      desc='{} - chunk_{}'.format(file_name, chunk_order),
      total=chunk_size,
      unit='MB',
      unit_scale=True,
      unit_divisor=1024,
    ) as bar:
      fields = {
        'params': json.dumps({
          'folder_id': folder_id,
          'id': id,
          'chunk': chunk_order,
          'n_chunks': n_chunks,
        }),
        'file': (file_name, chunk)
      }

      encoder = MultipartEncoder(fields=fields)
      multipart = MultipartEncoderMonitor(
        encoder, lambda monitor: bar.update(monitor.bytes_read - bar.n)
      )
      headers = {
        'Content-Type': multipart.content_type,
        'bioturing-api-token': token
      }
      response = requests.post(
        urljoin(host, 'api/v1/upload_chunk'),
        headers=headers,
        data=multipart,
      ).json()
      if not response:
        raise Exception('Something went wrong')
      if 'status' not in response or response['status'] != 200:
        raise Exception(response)

  output_dir = response['data']['output_dir']
  return output_dir


def upload_chunk(file_names, files, token, host, chunk_size):
  folder_id = get_uuid()
  for file_name, file in zip(file_names, files):
    file_size = file.stat().st_size
    n_chunks = int(np.ceil(file_size / chunk_size))
    id = _add_file_upload(
      folder_id,
      n_chunks,
      file_name,
      token,
      host
    )
    output_dir = _upload_each_file_in_chunk(
      folder_id,
      id,
      file,
      file_name,
      token,
      host,
      chunk_size,
      n_chunks
    )
  return output_dir


def upload_local(file_names, files, group_id, study_type, token, host):
  dir_id = get_uuid()
  output_dir = ''
  for file_name, file in zip(file_names, files):
    total_size = file.stat().st_size
    with tqdm(
      desc=file_name, total=total_size, unit='MB',  unit_scale=True, unit_divisor=1024,
    ) as bar:
      fields = {
        'params': json.dumps({
          'name': file_name,
          'file_id': dir_id,
          'group_id': group_id,
          'study_type': study_type,
        }),
        'file': (file_name, open(file, 'rb'))
      }

      encoder = MultipartEncoder(fields=fields)
      multipart = MultipartEncoderMonitor(
        encoder, lambda monitor: bar.update(monitor.bytes_read - bar.n)
      )
      headers = {
        'Content-Type': multipart.content_type,
        'bioturing-api-token': token
      }
      response = requests.post(
        urljoin(host, 'api/v1/upload'),
        data=multipart,
        headers=headers
      ).json()
      if not response:
        raise Exception('Something went wrong')
      if 'status' not in response or response['status'] != 200:
        raise Exception(response)
      output_dir = response['data']
  return output_dir


def dataframe2dictionary(df):
  res = dict()
  res['barcodes'] = df.index.values.tolist()
  for column in df.columns:
    tmp_data = df.loc[:, column].values
    try:
      data = [int(x) for x in tmp_data]
    except:
      data = [str(x) for x in tmp_data]
    res[column] = data
  return res


def read_csv(path, **kwargs):
  df = pd.read_csv(filepath_or_buffer = path, sep='\t', **kwargs)

  if 'index_col' in kwargs:
    if len(df.columns) == 0:
      return pd.read_csv(filepath_or_buffer = path, sep=',', **kwargs)
  else:
    if len(df.columns) < 2:
      return pd.read_csv(filepath_or_buffer = path, sep=',', **kwargs)

  return df


def parse_root_leaf_name(
    ontologies_tree,
    root_name,
    leaf_name,
  ):
  root_ids = []
  for id in ontologies_tree['tree']:
    if ontologies_tree['tree'][id]['name'] == root_name:
      root_ids.append(id)
  for root_id in root_ids:

    children = ontologies_tree['tree'][root_id]['children']
    for child in children:
      if child['name'] == leaf_name:
        leaf_id = child['id']
        return root_id, leaf_id

      grand_children = child['children']
      for grand_child in grand_children:
        if grand_child['name'] == leaf_name:
          leaf_id = grand_child['id']
          return root_id, leaf_id

  raise Exception('Cannot find "{}" - "{}"'.format(root_name, leaf_name))
