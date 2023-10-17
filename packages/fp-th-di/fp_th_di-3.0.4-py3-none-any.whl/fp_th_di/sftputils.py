from typing import List
import pysftp
import re
import os
from fp_th_di.logger import logger

class SFTPManager:
  def __init__(self, host: str, username: str, password: str=None, privateKey: str=None,
      privateKeyPass:str=None, port:int=22):
    self.host = host
    self.username = username
    self.password = password
    self.privateKey = privateKey
    self.privateKeyPass = privateKeyPass
    self.port = port

    self.cnopts = pysftp.CnOpts()
    self.cnopts.hostkeys = None

  def create_connection(self):
    try:
      if self.privateKey is not None:
        self.sftp = pysftp.Connection(host=self.host, username=self.username,
            private_key=self.privateKey, private_key_pass=self.privateKeyPass,
            port=self.port, cnopts=self.cnopts)
      elif self.password is not None:
        self.sftp = pysftp.Connection(host=self.host, username=self.username,
            password=self.password, cnopts=self.cnopts, port=self.port)
      else:
        raise Exception('Please provide sftp password or private key')
    except Exception as e:
      logger.error(e)
      raise e

  def close_connection(self):
    try:
      self.sftp.close()
    except Exception as e:
      logger.error(e)
      raise e

  def list_files_in_path(self, remotePath:str = '.') -> list:
    """Get list of filenames in the given remote directory

    Args:
        remotePath (str): remote directory

    Raises:
        Exception: if failed to connect to SFTP server

    Returns:
        list: List of filenames found in remotePath
    """
    try:
      return list(self.sftp.listdir(remotePath))
    except Exception as e:
      logger.error(e)
      raise e

  def download_file(self, remoteFilename:str, localFilename:str):
    """Download file from remote directory to local directory

    Args:
        remoteFilename (str): path_to_remote_file_to_download_from
        localFilename (str): path_to_local_file_to_download_to

    Raises:
        Exception: if failed to connect to SFTP server
    """
    try:
      self.sftp.get(remoteFilename, localFilename)
    except Exception as e:
      logger.error(e)
      raise e

  def __downloadDir__(self, sftp:pysftp.Connection, filesInDir:List[str], localPath:str, filterOptions: dict = dict()) -> List[str]:
    """A helper private function to download all files given in the list of filesInDir

    Args:
        sftp (pysftp.Connection): SFTP connection
        filesInDir (List[str]): list of filenames to download
        localPath (str): local path to download to
        filterOptions (dict, optional): optional filtering condition to detemine whether a file should be downloaded or not. Defaults to dict().

    Returns:
        List[str]: list of path_to_downloaded_files
    """
    files = []
    for eachFile in filesInDir:
      filename, fileExtension = os.path.splitext(eachFile)
      # not download if does not pass filtering conditions
      if ('name_reg' in filterOptions) and \
        not bool(re.match(filterOptions['name_reg'], eachFile)):
        continue
      if ('file_format' in filterOptions) and \
        (not filterOptions['file_format'] in fileExtension):
        continue
      if ('name_like' in filterOptions) and \
        (not filterOptions['name_like'] in filename):
        continue
      # download file
      sftp.get(eachFile, localPath + eachFile)
      files.append(localPath + eachFile)
    return files

  def download_dir(self, remotePath:str, localPath:str, filterOptions: dict = dict()) -> List[str]:
    """Download all files in remote directory to a specific local directory

    Args:
        remotePath (str): remote directory to download from
        localPath (str): local directory to download to
        filterOptions (dict, optional): filtering option to determine whether a file should be downloaded or not. Defaults to dict().

    Raises:
        Exception: if failed to connec to SFTP server

    Returns:
        list: list of path_to_downloaded_files
    """
    try:
      self.__downloadDir__(self.sftp, self.list_files_in_path(remotePath), localPath, filterOptions)
    except Exception as e:
      logger.error(e)
      raise e

  def upload_file(self, localFilename:str, remoteFilename:str):
    """Upload local file to SFTP server

    Args:
        localFilename (str): path_to_local_file_to_upload
        remoteFilename (str): path_to_remote_file

    Raises:
        Exception: if failed to connect to SFTP server
    """
    try:
      self.sftp.put(localFilename, remoteFilename)
    except Exception as e:
      logger.error(e)
      raise e

  def delete_file(self, remoteFilename:str):
    """delete a specific file in SFTP server

    Args:
        remoteFilename (str): path_to_remote_file

    Raises:
        Exception: if fail to connect to SFTP server
    """
    try:
      self.sftp.remove(remoteFilename)
    except Exception as e:
      logger.error(e)
      raise e
