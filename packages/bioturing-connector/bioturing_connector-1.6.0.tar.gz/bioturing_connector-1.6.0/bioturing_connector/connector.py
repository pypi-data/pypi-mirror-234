import time
import pandas as pd
from typing import List
from urllib.parse import urljoin

from .common import common
from .common import decode_base64_array
from .common.https_agent import HttpsAgent
from .typing import StudyUnit


class Connector(object):
  """
  Shared functions of all platforms
  """

  def __init__(self, host: str, token: str, ssl: bool = True):
    """
    Parameters
    ----------
    host : str
      The URL of the host server, only support HTTPS connection\n
      Example:
        BBrowserX: https://talk2data.bioturing.com/t2d_index_tool/ \n
        Lens_SC: https://talk2data.bioturing.com/lens_sc/ \n
        Lens_Bulk: https://talk2data.bioturing.com/lens_bulk/ \n
    token : str
      The API token to verify authority. Generated in-app.
    """
    self.__host = host
    self.__token = token
    self.__ssl = ssl
    self.__https_agent = HttpsAgent(self.__token, self.__ssl)


  def post_request(self, api_route, data={}):
    """
    :meta private:
    """
    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, api_route),
      body=data
    )
    return submission_status


  def test_connection(self):
    """
    Test the connection with the host

    Returns
    ----------
    connection status : str
    """
    url = urljoin(self.__host, 'api/v1/test_connection')
    print(f'Connecting to host at {url}')
    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      print('Connection successful')
      return True
    else:
      print('Connection failed')
    return False


  def get_submission_log(self, group_id: str, task_id: str):
    """
    :meta private:
    """
    last_status = []
    while True:
      submission_log = self.post_request(
        api_route='api/v1/get_submission_log',
        data={'task_id': task_id}
      )
      if not submission_log or 'status' not in submission_log or \
        submission_log['status'] != 200:
        print('Internal server error. Please check server log.')
        break

      if submission_log['data']['status'] == 'ERROR':
        print('Failed to summit. Please check server log.')
        break

      current_status = submission_log['data']['log'].split('\n')[:-1]
      new_status = current_status[len(last_status):]
      if len(new_status):
        print('\n'.join(new_status))

      last_status += new_status
      if submission_log['data']['status'] != 'SUCCESS':
        time.sleep(5)
        continue
      else:
        res = self.post_request(
          api_route='api/v1/commit_submission_result',
          data={
            'group_id': group_id,
            'task_id': task_id
          }
        )
        if not res or 'status' not in res:
          print('Internal server error. Please check server log.')
          break
        elif res['status'] != 200:
          if 'message' in res:
            print(f"Connection failed. {res['message']}")
          else:
            print('Connection failed.')
          break
        else:
          print('Study submitted successfully!')
          return True
    return False


  def get_user_groups(self):
    """
    Get all the data sharing groups available for the current token

    Returns
    ----------
    List of groups' info : List[dict]
      In which:
        'group_id': uuid of the group, which will be used in further steps,\n
        'group_name': displaying name of the group
    """
    res = self.post_request(
      api_route='api/v1/get_user_groups'
    )
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def get_all_studies_info_in_group(
    self,
    species: str,
    group_id: str
  ):
    """
    Get info of all studies within group.

    Parameters
    -------------
    species : bioturing_connector.typing.Species.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id : str,
          Group hash id (uuid)

    Returns
    -------------
    List of studies' info : List[dict]
      In which:
        'uuid': the uuid of study, which will be used in further steps, \n
        'study_hash_id': the displaying id of study on platform,\n
        'created_by': email of person who submitted the study,\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_all_studies_info_in_group',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def query_genes(
    self,
    species: str,
    study_id: str,
    gene_names: List[str],
    unit: str = StudyUnit.UNIT_RAW.value
  ):
    """
    Query genes expression in study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    gene_names : List[str]
          Querying gene names. \n
          If gene_names=[], full matrix will be returned
    unit : bioturing_connector.typing.StudyUnit. Default 'raw'
          Expression unit\n
          Support:
            bioturing_connector.typing.StudyUnit.UNIT_LOGNORM.value\n
            bioturing_connector.typing.StudyUnit.UNIT_RAW.value\n

    Returns
    ----------
    expression_matrix : csc_matrix
          Expression matrix, shape=(n_cells, n_genes)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'gene_names': gene_names,
      'unit': unit
    }
    result = self.post_request(
      api_route='api/v1/study/query_genes',
      data=data
    )
    return common.parse_query_genes_result(result)


  def get_metadata(
    self,
    species: str,
    study_id: str
  ):
    """
    Get full metadata of a study.

    Parameters
    ----------
      species : bioturing_connector.typing.Species,
            Species of the study.\n
            Support:
              bioturing_connector.typing.Species.HUMAN.value\n
              bioturing_connector.typing.Species.MOUSE.value\n
              bioturing_connector.typing.Species.PRIMATE.value\n
              bioturing_connector.typing.Species.OTHERS.value\n
      study_id : str,
            uuidv4 of study

    Returns
    ----------
      Metadata: pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_metadata',
      data=data
    )
    common.check_result_status(result)
    metadata_dict = result['data']
    metadata_df = pd.DataFrame(metadata_dict)
    return metadata_df


  def get_barcodes(
    self,
    species: str,
    study_id: str
  ):
    """
    Get barcodes of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,\n
          uuidv4 of study

    Returns
    ----------
    barcodes : List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_barcodes',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def get_features(
    self,
    species: str,
    study_id: str
  ):
    """
    Get features of a study.

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    Features: List[]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/study/get_features',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def list_all_custom_embeddings(
    self,
    species: str,
    study_id: str
  ):
    """
    List out all custom embeddings in a study

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study

    Returns
    ----------
    List of embeddings' info : List[dict]
      In which:
        'embedding_id': the uuid used in further steps\n
        'embedding_name': displaying name on platform\n
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.post_request(
      api_route='api/v1/list_all_custom_embeddings',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def retrieve_custom_embedding(
    self,
    species: str,
    study_id: str,
    embedding_id: str
  ):
    """
    Retrieve custom embedding array in the study

    Parameters
    -------------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    embedding_id : str,
          Embedding id (uuid)

    Returns
    -------------
    embedding_arr : np.ndarray with shape (n_cells x n_dims)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'embedding_id': embedding_id
    }
    result = self.post_request(
      api_route='api/v1/retrieve_custom_embedding',
      data=data
    )
    common.check_result_status(result)
    coord_arr = result['data']['coord_arr']
    coord_shape = result['data']['coord_shape']
    return decode_base64_array(coord_arr, 'float32', coord_shape)


  def submit_metadata_from_dataframe(
    self,
    species: str,
    study_id: str,
    group_id: str,
    df: pd.DataFrame
  ):
    """
    Submit metadata dataframe directly to platform

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    df : pandas DataFrame,
          Barcodes must be in df.index!!!!

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    metadata_dct = common.dataframe2dictionary(df)
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'metadata_dct': metadata_dct
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_dataframe',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def submit_metadata_from_local(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str
  ):
    """
    Submit metadata to platform with local path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : local path leading to metadata file,
          Barcodes must be in the first column\n
          File suffix must be in .tsv/.csv

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    df = common.read_csv(file_path, index_col=0)
    return self.submit_metadata_from_dataframe(
      species,
      study_id,
      group_id,
      df
    )


  def submit_metadata_from_s3(
    self,
    species: str,
    study_id: str,
    group_id: str,
    file_path: str
  ):
    """
    Submit metadata to platform with s3 path

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    study_id : str,
          uuidv4 of study
    group_id : str,
          ID of the group containing study id
    file_path : str,
          Path in s3 bucket leading to metadata file,\n
          Notes:
            Barcodes must be in the fist column\n
            File suffix must be in .tsv/.csv\n
            File_path DOES NOT contain s3_bucket path configured on the platform
              E.g:
                realpath: 's3://bucket/folder/metadata.tsv'\n
                inputpath: 'folder/metadata.tsv'

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    data = {
      'species': species,
      'study_id': study_id,
      'group_id': group_id,
      'file_path': file_path
    }
    result = self.post_request(
      api_route='api/v1/submit_metadata_s3',
      data=data
    )
    common.check_result_status(result)
    print('Successful')
    return True


  def get_ontologies_tree(
    self,
    species,
    group_id,
  ):
    """
    Get standardized ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species,
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value
    group_id : str
          ID of the group.

    Returns
    ----------
    Ontologies tree : Dict[Dict]
      In which:
        'name': name of the node, which will be used in further steps\n
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.post_request(
      api_route='api/v1/get_ontologies',
      data=data
    )
    common.check_result_status(result)
    return result['data']


  def assign_standardized_meta(
    self,
    species,
    group_id,
    study_id,
    metadata_field,
    metadata_value,
    root_name,
    leaf_name,
  ):
    """
    Assign metadata value to standardized term on ontologies tree

    Parameters
    ----------
    species : bioturing_connector.typing.Species
          Species of the study.\n
          Support:
            bioturing_connector.typing.Species.HUMAN.value\n
            bioturing_connector.typing.Species.MOUSE.value\n
            bioturing_connector.typing.Species.PRIMATE.value\n
            bioturing_connector.typing.Species.OTHERS.value\n
    group_id  : str
          ID of the group to submit the data to.
    study_id  : str
          ID of the study (uuid)
    metadata_field  : str
          ~ column name of meta dataframe in platform (eg: author's tissue)
    metadata_value  : str
          ~ metadata value within the metadata field (eg: normal lung)
    root_name : str
          name of root in btr ontologies tree (eg: tissue)
    leaf_name : str
          name of leaf in btr ontologies tree (eg: lung)

    Returns
    ----------
    Submission status : bool | str
      True or Error log
    """
    ontologies_tree = self.get_ontologies_tree(species, group_id)
    root_id, leaf_id = common.parse_root_leaf_name(
      ontologies_tree,
      root_name,
      leaf_name
    )
    data = {
      'species': species,
      'group_id': group_id,
      'study_id': study_id,
      'group': metadata_field,
      'name': metadata_value,
      'root_id': root_id,
      'leaf_id': leaf_id,
    }
    result = self.post_request(
      api_route='api/v1/study/assign_standardized_term',
      data=data
    )
    common.check_result_status(result)
    return 'Successul'