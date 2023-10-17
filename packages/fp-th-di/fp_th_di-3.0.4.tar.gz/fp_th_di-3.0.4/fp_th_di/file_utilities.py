import os, shutil, gzip
from os import listdir
from os.path import isfile, join
from typing import List
from fp_th_di.logger import logger
import re
  
def current_dir() -> str:
  """Get current directory

  Returns:
      str: path to current directory
  """  
  return os.getcwd()

def dir_exists(pathToDir:str) -> bool:
  """Check if directory exists

  Args:
      pathToDir (str): targeted path to directory to check

  Returns:
      bool: True if exists; otherwise, False
  """  
  return os.path.exists(pathToDir)

def clear_dir(pathToDir:str, options: dict=dict()) -> None:
  """Clear all files in targeted directory

  Args:
      pathToDir (str): targeted path to directory
      options (dict, optional): file format to deleted. Defaults to empty dict.
  """  
  for filename in os.listdir(pathToDir):
    filePath = os.path.join(pathToDir, filename)
    try:
      if os.path.isfile(filePath) or os.path.islink(filePath):
        if 'file_format' in options and \
          not options['file_format'].lower() in filePath.lower():
          continue
        os.unlink(filePath)
      elif os.path.isdir(filePath):
        shutil.rmtree(filePath)
    except Exception as e:
        logger.info('Failed to delete %s. Reason: %s' % (filePath, e))

def create_dir(pathToDir:str) -> None:
  """Create directory

  Args:
      pathToDir (str): path to directory to create
  """  
  try:
    os.makedirs(pathToDir)
  except OSError:
    logger.info("Creation of the directory %s failed" % pathToDir)
  else:
    logger.info("Successfully created the directory %s " % pathToDir)

def delete_dir(pathToDir:str) -> None:
  """Delete directory

  Args:
      pathToDir (str): targeted path to directory to delete
  """  
  try:
    os.rmdir(pathToDir)
  except OSError:
    logger.info("Deletion of the directory %s failed" % pathToDir)
  else:
    logger.info("Successfully deleted the directory %s" % pathToDir)

def list_files_in_dir(pathToDir:str, filterOptions: dict=dict()) -> List[str]:
  """Lists all files in targeted directory

  Args:
      pathToDir (str): path to targeted directory 
      filterOptions (dict, optional): Filter options for targeted files to search in targeted directory. Defaults to empty dict.

  Returns:
      List[str]: List of files found in the targeted directory
  """  
  files = []
  for each in [f for f in listdir(pathToDir) if isfile(join(pathToDir, f))]:
    if ('name_reg' in filterOptions) and \
      not bool(re.match(filterOptions['name_reg'], each)):
      continue
    if ('file_format' in filterOptions) and \
      (not filterOptions['file_format'].lower() in each.lower()):
      continue
    if ('name_like' in filterOptions) and \
      (not filterOptions['name_like'].lower() in each.lower()):
      continue
    files.append(each)
  return files

def unzip(inputFilenames:List[str], inputPath:str, outputPath:str) -> List[str]:
  """Unzip a zipfile

  Args:
      inputFilenames (List[str]): name of the zipped file
      inputPath (str): path to zipped file
      outputPath (str): path to place the unzipped files to

  Returns:
      List[str]: list of unzipped filenames
  """  
  outputFilenames = []
  for each in inputFilenames:
    zipfile = each if inputPath in each else f'{inputPath}/{each}' 
    with gzip.open(zipfile, 'rb') as fIn:
      filename, file_extension = os.path.splitext(each)
      filepath, filename = os.path.split(filename)
      unzipfile = filename if outputPath in filename else f'{outputPath}/{filename}'
      with open(unzipfile, 'wb') as fOut:
        shutil.copyfileobj(fIn, fOut)
        outputFilenames.append(filename)
  return outputFilenames
  