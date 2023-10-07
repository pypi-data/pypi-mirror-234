"""Python package for submitting/getting data from Lens SC"""

import os
import numpy as np

from typing import List
from typing import Union
from pathlib import Path

from .common import get_uuid
from .common import common

from .typing import Species
from .typing import StudyType
from .typing import ChunkSize
from .typing import TechnologyType
from .typing import INPUT_LENS_SC

from .connector import Connector


class LensSCConnector(Connector):
  """
  Create a connector object to submit/get data from BioTuring Lens Single-cell (Xenium/Cosmx/Vizgen/Proteomics)

  Parameters
  ----------
  host : str
    The URL of the LENS SC server, only support HTTPS connection\n
    Example:
      https://talk2data.bioturing.com/lens_sc/
  token : str
    The API token to verify authority. Generated in-app.
  """

  def _check_vizgen_version_2(self, study_type, all_input_files):
    if study_type != StudyType.VIZGEN.value:
      return study_type
    for i in all_input_files:
      if i.lower().endswith('.parquet'):
        return StudyType.VIZGEN_V2.value
    return StudyType.VIZGEN.value


  def _check_valid_input_lens_sc(
      self,
      server_files_path,
      server_folders_path,
      study_type,
    ):
    input_files = INPUT_LENS_SC[study_type]['files'].values()
    input_folders = INPUT_LENS_SC[study_type]['folders'].values()
    file_paths = []
    folder_paths = []
    for f in input_files:
      try:
        file_path = [x for x in server_files_path if x.lower().endswith(f)][0]
        file_paths.append(file_path.split('/')[-1])
      except Exception as e:
        raise ValueError('Cannot find ***{} in selected folder. Error: {}'.format(f, e))
    for f in input_folders:
      try:
        folder_path = [x for x in server_folders_path if x.lower().endswith(f)][0]
        folder_paths.append(folder_path.split('/')[-1])
      except Exception as e:
        raise ValueError('Cannot find {} in selected folder. Error: {}'.format(f, e))
    return file_paths, folder_paths


  def _get_required_files_fols_lens_sc(self, server_dir_path, study_type):
    all_files_fols = [
      os.path.join(server_dir_path, x)
      for x in os.listdir(server_dir_path)
    ]
    all_files = [
      x for x in all_files_fols if os.path.isfile(x)
    ]
    all_folders = [
      x for x in all_files_fols if os.path.isdir(x)
    ]
    study_type = self._check_vizgen_version_2(study_type, all_files_fols)
    return self._check_valid_input_lens_sc(all_files, all_folders, study_type)


  def _upload_fol_lens_sc(self, batch_info, study_type, chunk_size):
    final_file_names = []
    final_files = []
    try:
      for batch in batch_info:
        files_path, fols_path = self._get_required_files_fols_lens_sc(
          batch['folder'],
          study_type
        )
        zip_path = os.path.join(
          batch['folder'], '{}.zip'.format(batch['name'])
        )

        print ('Zipping neccesary files of batch [{}]. \nLocation: {}'.format(batch['name'], zip_path))
        final_file_names.append('{}.zip'.format(batch['name']))
        final_files.append(zip_path)
        os.system('cd {} && zip -r {} {} && cd -'.format(
          batch['folder'],
          zip_path,
          ' '.join(files_path + fols_path)
        ))

      print ('Uploading all files to server...')
      output_dir = common.upload_chunk(
        final_file_names,
        [Path(zip_path)],
        self.__token,
        self.__host,
        chunk_size
      )

    except Exception as e:
      raise e

    finally:
      for zip_path in final_files:
        print ('Delete zip files: [{}]'.format(zip_path))
        os.system('rm {}'.format(zip_path))

    return output_dir


  def _submit_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    technology_type: str = TechnologyType.LENS_SC.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
  ):
    if study_id is None:
      study_id = get_uuid()

    if min_counts is None:
      min_counts = 0

    if min_genes is None:
      min_genes = 0

    if max_counts is None:
      max_counts = 1e9

    if max_genes is None:
      max_genes = 1e9

    if neg_controls_percentage is None:
      neg_controls_percentage = 100

    study_info = {
      'study_hash_id': study_id,
      'name': name,
      'authors': authors if authors else [],
      'abstract': abstract
    }

    return {
      'species': species,
      'group_id': group_id,
      'filter_params': {
        'min_counts': min_counts,
        'min_genes': min_genes,
        'max_counts': max_counts,
        'max_genes': max_genes,
        'neg_controls_percentage': neg_controls_percentage,
      },
      'study_type': technology_type,
      'platform': study_type,
      'study_info': study_info,
    }


  def submit_study_from_s3_lens_sc(
    self,
    group_id: str,
    batch_info: List[dict],
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
  ):
    """
    Submit multiple single cell - spatial folders.

    Parameters
    ----------
    group_id : str
        ID of the group to submit the data to.
    batch_info : List[dict]
        File path and batch name information, the path DOES NOT include bucket path configured on platform!\n
        Example:
          [{
            'name': 'study_1',\n
            'folder': 's3_path/study_folder',
          }, {...}]
    study_id : str, optional
        Will be displaying name of study (eg: COSMX_BRAIN). Default: uuidv4\n
    name : str, optional
        Name of the study. Default: 'TBD'
    authors : List[str], optional
        Authors of the study. Default: []
    abstract : str, optional
        Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
        Species of the study. Default: 'human'.\n
        Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    study_type : bioturing_connector.typing.StudyType, optional
        Format of dataset. Default: 11.\n
        Support:
                bioturing_connector.typing.StudyType.VIZGEN.value\n
                bioturing_connector.typing.StudyType.COSMX.value\n
                bioturing_connector.typing.StudyType.XENIUM.value\n
    min_counts : int, optional
        Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
        Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
        Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
        Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    neg_controls_percentage : int, optional
        Maximum number of control/negative genes percentage required for a cell to pass filtering. Default: 100\n
        Ranging from 0 to 100

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.LENS_SC.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      neg_controls_percentage,
    )
    data['batch_info'] = {o['name']: o for o in batch_info}

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_s3',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id
    )


  def submit_study_from_s3_proteomics(
    self,
    group_id: str,
    batch_info: dict,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None
  ):
    """
    Submit one Proteomics image.

    Parameters
    ----------
    group_id : str
        ID of the group to submit the data to.
    batch_info : Dict[]
        File path and batch name information, the path should EXCLUDE bucket path!\n
        Example:
          {
            'image': 's3_path/image.ome.tiff'
          }
    study_id : str, optional
        Will be displaying name of study (eg: CODEX_BRAIN). Default: uuidv4
    name : str, optional
        Name of the study. Default: 'TBD'
    authors : List[str], optional
        Authors of the study. Default: []
    abstract : str, optional
        Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
        Species of the study. Default: 'human'.\n
        Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    min_counts : int, optional
        Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
        Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
        Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
        Maximum number of genes expressed required for a cell to pass filtering. Default: inf

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      -1,
      TechnologyType.PROTEOMICS.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes
    )
    batch_info['name'] = batch_info['image']
    data['batch_info'] = [batch_info]

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_s3',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id
    )


  def submit_study_from_local_lens_sc(
    self,
    group_id: str,
    batch_info: List[dict],
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.XENIUM.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    neg_controls_percentage: Union[int, float] = None,
    chunk_size: int = ChunkSize.CHUNK_100_MB.value,
  ):
    """
    Submit multiple single cell - spatial folders.

    Parameters
    ----------
    group_id : str
        ID of the group to submit the data to.
    batch_info : List[dict]
        File path and batch name information\n
        Example:
          [{
            'name': 'dataset_1',\n
            'folder': 'server_path/dataset_folder_1',
          }, {...}]
    study_id : str, optional
        Will be displaying name of study (eg: COSMX_BRAIN). Default: uuidv4
    name : str, optional
        Name of the study. Default: 'TBD'
    authors : List[str], optional
        Authors of the study. Default: []
    abstract : str, optional
        Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
        Species of the study. Default: 'human'.\n
        Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    study_type : bioturing_connector.typing.StudyType, optional
        Format of dataset. Default: 11\n
        Support:
                bioturing_connector.typing.StudyType.VIZGEN.value\n
                bioturing_connector.typing.StudyType.COSMX.value\n
                bioturing_connector.typing.StudyType.XENIUM.value\n
    min_counts : int, optional
        Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
        Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
        Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
        Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    neg_controls_percentage : int, optional
        Maximum number of control/negative genes percentage required for a cell to pass filtering. Default: 100\n
        Ranging from 0 to 100
    chunk_size : bioturing_connector.typing.ChunkSize, optional
        Size of each separated chunk for uploading. Default: 104857600\n
        Support:
                bioturing_connector.typing.ChunkSize.CHUNK_5_MB.value
                bioturing_connector.typing.ChunkSize.CHUNK_100_MB.value
                bioturing_connector.typing.ChunkSize.CHUNK_500_MB.value
                bioturing_connector.typing.ChunkSize.CHUNK_1_GB.value

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """

    if len(np.unique([x['name'] for x in batch_info])) != len(batch_info):
      raise Exception('Names of batches must be unique')

    if chunk_size not in [e.value for e in ChunkSize]:
      return 'only support:\n{},\n{},\n{},\n{}'.format(
        'ChunkSize.CHUNK_5_MB.value',
        'ChunkSize.CHUNK_100_MB.value',
        'ChunkSize.CHUNK_500_MB.value',
        'ChunkSize.CHUNK_1_GB.value',
      )

    output_dir = self._upload_fol_lens_sc(batch_info, study_type, chunk_size)

    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.LENS_SC.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      neg_controls_percentage,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [o['name'] for o in batch_info]

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_local',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id
    )


  def submit_study_from_local_proteomics(
    self,
    group_id: str,
    batch_info: dict,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    chunk_size: int = ChunkSize.CHUNK_100_MB.value,
  ):
    """
    Submit one Proteomics image.

    Parameters
    ----------
    group_id : str
        ID of the group to submit the data to.
    batch_info : List[]
        File path and batch name information\n
        Example:
          {
            'image': 'server_path/image.ome.tiff'
          }
    study_id : str, optional
        Will be displaying name of study (eg: CODEX_BRAIN). Default: uuidv4
    name : str, optional
        Name of the study. Default: 'TBD'
    authors : List[str], optional
        Authors of the study. Default: []
    abstract : str, optional
        Abstract of the study. Default: ''
    species : bioturing_connector.typing.Species, optional
        Species of the study. Default: 'human'\n
        Support:
                bioturing_connector.typing.Species.HUMAN.value\n
                bioturing_connector.typing.Species.MOUSE.value\n
                bioturing_connector.typing.Species.PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    min_counts : int, optional
        Minimum number of counts required for a cell to pass filtering. Default: 0
    min_genes : int, optional
        Minimum number of genes expressed required for a cell to pass filtering. Default: 0
    max_counts : int, optional
        Maximum number of counts required for a cell to pass filtering. Default: inf
    max_genes : int, optional
        Maximum number of genes expressed required for a cell to pass filtering. Default: inf
    chunk_size : bioturing_connector.typing.ChunkSize, optional
        Size of each separated chunk for uploading. Default: 104857600.\n
        Support:
              bioturing_connector.typing.ChunkSize.CHUNK_5_MB.value\n
              bioturing_connector.typing.ChunkSize.CHUNK_100_MB.value\n
              bioturing_connector.typing.ChunkSize.CHUNK_500_MB.value\n
              bioturing_connector.typing.ChunkSize.CHUNK_1_GB.value\n

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    study_type = -1
    batch_info['name'] = batch_info['image'].split('/')[-1]
    file_names = [batch_info['name']]
    files = [batch_info['image']]
    output_dir = common.upload_chunk(
      file_names,
      [Path(x) for x in files],
      self.__token,
      self.__host,
      chunk_size
    )

    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      study_type,
      TechnologyType.PROTEOMICS.value,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [batch_info['name']]

    submission_status = self.post_request(
      api_route='api/v1/submit_study_from_local',
      data=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return False

    return self.get_submission_log(
      group_id=group_id,
      task_id=task_id
    )