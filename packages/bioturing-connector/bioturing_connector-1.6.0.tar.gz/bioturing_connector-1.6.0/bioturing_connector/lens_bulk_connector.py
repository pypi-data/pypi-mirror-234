"""Python package for submitting/getting data from Lens Bulk"""

from typing import List
from pathlib import Path

from .common import common
from .common import get_uuid

from .typing import Species
from .typing import StudyType
from .typing import ChunkSize

from .connector import Connector


class LensBulkConnector(Connector):
  """
  Create a connector object to submit/get data from BioTuring Lens Bulk (Visium/GeoMx DSP)

  Parameters
  ----------
  host : str
    The URL of the LENS BULK server, only support HTTPS connection\n
    Example:
      https://talk2data.bioturing.com/lens_bulk/
  token : str
    The API token to verify authority. Generated in-app.
  """

  def _submit_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.VISIUM.value,
  ):
    if study_id is None:
      study_id = get_uuid()

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
        'min_counts': 0,
        'min_genes': 0,
        'max_counts': 1e9,
        'max_genes': 1e9,
        'mt_percentage': 1,
      },
      'study_type': study_type,
      'normalize': True,
      'subsample': -1,
      'study_info': study_info,
    }


  def submit_study_from_s3(
    self,
    group_id: str,
    batch_info: List[dict],
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.DSP.value,
  ):
    """
    Submit one or multiple data folders.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    batch_info : List[dict]
          File path and batch name information, the path does not include bucket path!\n
          Example:
            For DSP format:
              [{
                'matrix': 's3_path/data_1/matrix.xlsx',\n
                'image': 's3_path/data_1/image.ome.tiff',
              }, {...}]
            For Visium format:
              [{
                'matrix': 's3_path/data_1/matrix.h5',\n
                'image': 's3_path/data_1/image.tiff'\n
                'position': 's3_path/data_1/tissue_positions_list.csv'\n
                'scale': 's3_path/data_1/scalefactors_json.json'\n
              }, {...}]
            For Visium RDS format:
              [{
                'matrix': 's3_path/GSE128223_1.rds'
              }, {...}]
            For Visium Anndata format:
              [{
                'matrix': 's3_path/GSE128223_1.h5ad'
              }, {...}]
    study_id : str, optional
          Will be name of study (eg: VISIUM_PBMC). Default: uuidv4
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
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    study_type : bioturing_connector.typing.StudyType, optional
          Format of dataset. Default: 7\n
          Support:
                bioturing_connector.typing.StudyType.DSP.value\n
                bioturing_connector.typing.StudyType.VISIUM.value\n
                bioturing_connector.typing.StudyType.VISIUM_RDS.value\n
                bioturing_connector.typing.StudyType.VISIUM_ANN.value\n

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
      study_type
    )
    if study_type == StudyType.VISIUM_ANN.value \
      or study_type == StudyType.VISIUM_RDS.value:
      for i, o in enumerate(batch_info):
        o['name'] = o['matrix'].split('/')[-1]
    else:
      for i, o in enumerate(batch_info):
        name = o['matrix'].split('/')
        if len(name) == 1:
          o['name'] = f'Batch {i + 1}'
        else:
          o['name'] = name[-2]
    data['batch_info'] = {f'Batch_{i}': o for i, o in enumerate(batch_info)}

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


  def submit_study_from_local(
    self,
    group_id: str,
    batch_info: object,
    study_id: str = None,
    name: str = 'TBD',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    study_type: int = StudyType.DSP.value,
    chunk_size: int = ChunkSize.CHUNK_100_MB.value,
  ):
    """
    Submit one or multiple data folders.

    Parameters
    ----------
    group_id : str
          ID of the group to submit the data to.
    batch_info : List[dict]
          File path and batch name information\n
          Example:
            For DSP format:
              [{
                'name': 'data_1',\n
                'matrix': 'local_path/data_1/matrix.xlsx',\n
                'image': 'local_path/data_1/image.ome.tiff',\n
              }, {...}]
            For Visium format:
              [{
                'name': 'data_1',\n
                'matrix': 'local_path/data_1/matrix.h5',\n
                'image': 'local_path/data_1/image.tiff'\n
                'position': 'local_path/data_1/tissue_positions_list.csv'\n
                'scale': 'local_path/data_1/scalefactors_json.json'\n
              }, {...}]
            For Visium RDS format:
              [{
                'matrix': 'local_path/GSE128223_1.rds'
              }, {...}]
            For Visium Anndata format:
              [{
                'matrix': 'local_path/GSE128223_1.h5ad'
              }, {...}]
    study_id : str, optional
          Will be displaying name of study (eg: VISIUM_PBMC). Default: uuidv4
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
                bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value\n
                bioturing_connector.typing.Species.OTHERS.value\n
    study_type : bioturing_connector.typing.StudyType, optional
          Format of dataset. Default: 7\n
          Support:
                bioturing_connector.typing.StudyType.DSP.value\n
                bioturing_connector.typing.StudyType.VISIUM.value\n
                bioturing_connector.typing.StudyType.VISIUM_RDS.value\n
                bioturing_connector.typing.StudyType.VISIUM_ANN.value\n
    chunk_size : bioturing_connector.typing.ChunkSize, optional
          Size of each separated chunk for uploading. Default: 104857600\n
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

    if chunk_size not in [e.value for e in ChunkSize]:
      return 'only support:\n{},\n{},\n{},\n{}'.format(
        'ChunkSize.CHUNK_5_MB.value',
        'ChunkSize.CHUNK_100_MB.value',
        'ChunkSize.CHUNK_500_MB.value',
        'ChunkSize.CHUNK_1_GB.value',
      )

    file_names = []
    files = []
    if study_type == StudyType.VISIUM_ANN.value \
      or study_type == StudyType.VISIUM_RDS.value:
      for o in batch_info:
        p = Path(o['matrix'])
        o['name'] = p.name
        file_names.append(p.name)
        files.append(p)
    elif study_type == StudyType.VISIUM.value:
      for o in batch_info:
        if 'hires' in o['image'].lower():
          tmp_name = 'hires'
        elif 'lowres' in o['image'].lower():
          tmp_name = 'lowres'
        else:
          tmp_name = 'image'
        file_names.extend([
          f'{o["name"]}matrix.h5',
          f'{o["name"]}{tmp_name}.{o["image"].split(".")[-1]}',
          f'{o["name"]}position.{o["position"].split(".")[-1]}',
          f'{o["name"]}scale.json',
        ])
        files.extend([
          Path(o['matrix']),
          Path(o['image']),
          Path(o['position']),
          Path(o['scale']),
        ])
    elif study_type == StudyType.DSP.value:
      for o in batch_info:
        file_names.extend([
          f'{o["name"]}matrix.xlsx',
          f'{o["name"]}image.tiff',
        ])
        files.extend([
          Path(o['matrix']),
          Path(o['image']),
        ])

    output_dir = common.upload_chunk(
      file_names,
      files,
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