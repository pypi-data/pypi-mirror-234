from googleapiclient.discovery import Resource, build
from apiclient.http import MediaFileUpload
from fp_th_di.logger import logger
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import pandas as pd

def get_google_drive_credential(
    serviceAccountSecretCredentialsLocation:str,
    scopes:list
  ):
  """Get google drive credential or create new one if not found
  """
  credentials = service_account.Credentials.from_service_account_file(
        serviceAccountSecretCredentialsLocation, scopes=scopes)
  return credentials

def create_google_drive_service(
    serviceName:str,
    serviceAccountSecretCredentialsLocation:str,
    apiVersion:str,
    scopes:list
  ):
  return build(
    serviceName,
    apiVersion,
    credentials=get_google_drive_credential(
      serviceAccountSecretCredentialsLocation=serviceAccountSecretCredentialsLocation,
      scopes=scopes
    )
  )

def generate_google_drive_folder_metadata(folderName:str, parentFolderId:str) -> dict:
  """Generates metadata dict for folder type

  Args:
    folderName (str): folder name to create
    parentFolderId (str): google id of parent folder to create new folder in

  Returns:
    dict: the folder metadata
  """
  return {
    'name': folderName,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [parentFolderId]
  }

def create_new_google_drive_folder(driveService:Resource, folderName:str, parentFolderId:str) -> str:
  """Creates new google drive folder

  Args:
    driveService (Resource): google drive service
    folderName (str): folder name
    parentFolderId (str): google id of parent folder to create new folder in

  Returns:
    str: new folder id
  """
  folder = driveService.files().create(fields='id',
    body=generate_google_drive_folder_metadata(
      folderName=folderName,
      parentFolderId=parentFolderId
    )).execute()
  logger.info('Successfully created new Google Drive folder:', folder.get('id'))
  return folder.get('id')

def search_for_google_drive_folder(driveService:Resource, folderName:str) -> str:
  """Search for targeted folder by name

  Args:
    driveService (Resource): google drive service
    folderName (str): name of folder to search for

  Returns:
    str: [description]
  """
  logger.info('Searching for Google Drive Folder:', folderName)
  pageToken = None
  while True:
    response = driveService.files().list(
      q="mimeType = 'application/vnd.google-apps.folder'",
      spaces='drive',
      fields='nextPageToken, files(id, name)',
      pageToken=pageToken
      ).execute()
    for file in response.get('files', []):
      if file.get('name') == folderName:
        logger.info('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
        return file.get('id')
    pageToken = response.get('nextPageToken', None)
    if pageToken is None:
      break
  logger.info('Could not found targeted folder in your Drive')

def list_folders_in_drive_folder(driveService, parentFolderId: str) -> list:
  """_summary_
  List out GoogleDrive folders exist in the parent folder with id given as input parameter

  Args:
      driveService: Google Drive Service object
      parentFolderId (str): Parent Google Drive Folder Id

  Returns:
      list: list of dictionary with information of folders found in the Shared Drive
  """
  logger.info("Getting folders from:", parentFolderId)
  results = driveService.files().list(
      q=f"mimeType = 'application/vnd.google-apps.folder' and trashed = false and parents in '"+ parentFolderId +"'",
      spaces="drive",
      fields="nextPageToken, files(id, name, createdTime)",
      orderBy="createdTime"
  ).execute()
  items = results.get('files', [])

  if not items:
      return ""
  else:
      return items

def generate_file_metadata(filename:str, parentFolderId:str, mimeType:str) -> dict:
  """Generates metadata dict for file type

  Args:
    filename (str): file to create
    parentFolderId (str): google id of parent folder to create the file in
    mimeType (str): file mime type. For example:
        image/png or image/jpeg for images
        application/vnd.openxmlformats-officedocument.spreadsheetml.sheet for xlsx file
        application/vnd.ms-excel for xls file
        text/csv for csv file

  Returns:
    dict: the folder metadata
  """
  return {
    'name': filename,
    'mimeType': mimeType,
    'parents': [parentFolderId]
  }

def search_files_from_google_drive_folder_by_filename(driveService:Resource, folderId:str, fileMimeType:str=None, targetedFilename:str=None) -> list:
  """Searching for files by mimetype and filename in specific GoogleDrive folder

  Args:
      driveService (Resource): google drive service
      folderId (str): Google drive folder Id
      fileMimeType (str, optional): file mime type. For example:
        image/png or image/jpeg for images
        application/vnd.openxmlformats-officedocument.spreadsheetml.sheet for xlsx file
        application/vnd.ms-excel for xls file
        text/csv for csv file
        Defaults to None.
      targetedFilename (str, optional): Filename to search. Defaults to None. If filename's none, get all files in the folder

  Returns:
      list: list of files dictionary. An item in the list consist of id of the file and filename
  """
  logger.info("Listing files in folder:", folderId)

  mimeType = f"mimeType = '{fileMimeType}' and " if fileMimeType is not None else ""
  filename = f"name = '{targetedFilename}' and " if targetedFilename is not None else ""

  pageToken = None
  results = driveService.files().list(
    q=f"{mimeType} {filename} trashed = false and parents in '{folderId}'",
    spaces='drive',
    fields='nextPageToken, files(id, name)',
    pageToken=pageToken,
    orderBy="createdTime desc",
  ).execute()

  return results.get('files', [])

def upload_file_to_google(driveService:Resource, localFileLocation:str, filename:str, parentFolderId:str, mimeType:str) -> str:
  """Upload a file from local to google drive folder

  Args:
    driveService (Resource): google drive service
    localFileLocation (str): path to file location
    filename (str): filename
    parentFolderId (str):  google id of parent folder to create the file in
    mimeType (str): file mime type. For example:
      image/png or image/jpeg for images
      application/vnd.openxmlformats-officedocument.spreadsheetml.sheet for xlsx file
      application/vnd.ms-excel for xls file
      text/csv for csv file

  Returns:
    str: google id of the file uploaded to Google Drive
  """
  media = MediaFileUpload(f'{localFileLocation}/{filename}', mimetype=mimeType)

  # Upload the file, use supportsAllDrives=True to enable uploading if targeted parent folder is shared drives.
  file = driveService.files().create(
    body=generate_file_metadata(
      filename=filename,
      parentFolderId=parentFolderId,
      mimeType=mimeType
    ),
    media_body=media,
    supportsAllDrives=True
  ).execute()
  logger.info("Successfully created file '%s' id '%s'." % (file.get('name'), file.get('id')))
  return file.get('id')

def get_folder_in_shared_drive(driveService, sharedDriveId: str) -> list:
    """_summary_

    Args:
        driveService: Google Drive Service object
        sharedDriveId (str): driveService: Google Drive Service object

    Returns:
        list: list of dictionary with information of folders found in the Shared Drive
    """
    results = driveService.files().list(
        q=f"mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        driveId=sharedDriveId,
        includeItemsFromAllDrives=True,
        corpora='drive',
        fields="nextPageToken, files(id, name, createdTime)",
        orderBy="createdTime",
        supportsAllDrives=True
    ).execute()
    items = results.get('files', [])

    if not items:
        return ""
    else:
        return items


def get_folder_id_from_shared_drive_by_folder_name(driveService,
    folderName:str, sharedDriveId: str) -> str:
    """Get Google Drive folder if from Shared Drive by searching from folder name

    Args:
        driveService: Google Drive Service object
        folderName (str): Targeted folder name
        sharedDriveId (str): driveService: Google Drive Service object

    Returns:
        str: id of the Google Drive folder if found in the Shared Drive; otherwise, None.
    """
    folders = get_folder_in_shared_drive(driveService, sharedDriveId)
    if not folders:
      return None
    for each in folders:
      if each['name'] == folderName:
        return each['id']
    else:
      return None

def get_files_from_shared_drive_by_folder_id(driveService,
    folderId: str, sharedDriveId: str, fileMimeType: str = None,
    targetedFilename: str = None) -> list:
    """Get files from Shared Drive by Google Drive folder id

    Args:
        driveService: Google Drive Service object
        folderId (str): id of gogole drive folder
        sharedDriveId (str): id of shared drive folder
        fileMimeType (str, optional): targeted files' type. Defaults to None.
        targetedFilename (str, optional): targeted files' names. Defaults to None.

    Returns:
        list: list of dictionary with information of targeted files found in the Google Drive folder.
    """
    mimeType = f"mimeType = '{fileMimeType}' and" if fileMimeType is not None else ""
    filename = f"name = '{targetedFilename}' and " if targetedFilename is not None else ""

    results = driveService.files().list(
        q=f"{mimeType} {filename} parents in '{folderId}' and trashed = false",
        driveId=sharedDriveId,
        includeItemsFromAllDrives=True,
        corpora='drive',
        fields="nextPageToken, files(id, name, createdTime)",
        orderBy="createdTime desc",
        supportsAllDrives=True
    ).execute()
    return results.get('files', [])

def delete_file_in_drive_by_file_id(driveService, fileId:str, folderId:str):
  """Remove file with Id from google drive folder Id

  Args:
      driveService (Resource): google drive service
      fileId (str): file id
      folderId (str): google drive folder id
  """
  driveService.files().update(fileId=fileId, removeParents=folderId).execute()

def download_file_from_drive_by_file_id(driveService, fileId:str, localFilePath:str):
    """Download targeted file from Google Drive by file id

    Args:
        driveService: Google Drive Service
        fileId (str): targeted file id
        localFilePath (str): path to save file locally
    """
    request = driveService.files().get_media(fileId=fileId)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    # Write the stuff
    with open(localFilePath, "wb") as f:
        f.write(fh.getbuffer())

def read_dataframe_from_google_sheet(sheetService, fileId:str, range:str) -> pd.DataFrame:
    """Return dataframe from specified range in targeted Google Sheet

    Args:
        sheetService (object): Google service with credential
        fileId (str): GoogleSheet File ID
        range (str): Range of information to extract into dataframe

    Returns:
        pd.DataFrame: dataframe with the information from the range specified in the input
    """
    # Get dataframe from file
    sheetObject = sheetService.spreadsheets().values().get(
      spreadsheetId=fileId,
      range=range
    ).execute()
    valuesFromRanges = sheetObject.get("values", [])
    return pd.DataFrame(valuesFromRanges[1:], columns=valuesFromRanges[0])

def write_dataframe_in_google_sheet(
    sheetService, fileId:str,
    range:str, dataframe:pd.DataFrame
  ):
  """Update gsheet range with values from dataframe

  Args:
      sheetService (_type_): Google Drive Service
      fileId (str): gsheet file id
      range (str): range to update
      dataframe (pd.DataFrame): dataframe to update in the range
  """
  try:
    # clearing out current values
    logger.info("Clearing out previous data")
    sheetService.spreadsheets( ).values( ).clear(
      spreadsheetId=fileId,
      range=range,
      body={}).execute( )

    logger.info("Writing new data")
    values = [list(dataframe.columns)]
    if len(dataframe) > 0:
      values.extend(dataframe.values.tolist())

    body = {
        'values': values
    }
    result = sheetService.spreadsheets().values().update(
        spreadsheetId=fileId,
        range=range,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    logger.info(f"{result.get('updatedCells')} cells updated.")
    return result

  except Exception as error:
    logger.error(f"An error occurred: {error}")
    return error

def create_google_sheet_service(serviceAccountSecretCredentialsLocation:str):
  return create_google_drive_service(
    serviceName='sheets',
    serviceAccountSecretCredentialsLocation=serviceAccountSecretCredentialsLocation,
    apiVersion='v4',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
  )

def create_google_drive_service_sh(serviceAccountSecretCredentialsLocation:str):
  return create_google_drive_service(
    serviceName="drive",
    serviceAccountSecretCredentialsLocation=serviceAccountSecretCredentialsLocation,
    apiVersion="v3",
    scopes=['https://www.googleapis.com/auth/drive']
  )
