# BigQueryUtils.py
from google.cloud import bigquery
import google.auth
from enum import Enum
import pandas as pd
from fp_th_di.logger import logger
import datetime

class BigQuery:
  def create_connection(self, projectId:str): 
    """Create Google bigquery client 

    Args:
        projectId (str): GCP project id to run BigQuery job on

    Raises:
        e: Exception
    """    
    credentials,project = google.auth.default(scopes=[
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/bigquery',
    ])
    self.client = None
    try:
      self.client = bigquery.Client(project=projectId, credentials=credentials)
    except Exception as e:
      logger.error(e)
      raise e

  def fetch(self, statement:str) -> bigquery.QueryJob:
    """Fetch data from BigQuery

    Args:
        statement (str): bigquery sql statement to execute

    Raises:
        Exception: if failed to query data from bigquery

    Returns:
        bigquery.QueryJob: querying result
    """    
    if self.client is None:
      raise Exception('Client not found. Please call create_connection().')

    try: 
      return self.client.query(statement) 
    except Exception as e:
      logger.error(e)
      raise e
  
  def fetch_dataframe(self, statement:str) -> pd.DataFrame:
    """Fetch data from BigQuery as pandas.DataFrame

    Args:
        statement (str): bigquery sql statement to execute

    Raises:
        Exception: if failed to query data from bigquery

    Returns:
        pd.DataFrame: pandas.DataFrame with querying result
    """    
    if self.client is None:
      raise Exception('Client not found. Please call create_connection().')

    try:
      return self.fetch(statement).to_dataframe() 
    except Exception as e:
      logger.error(e)
      raise e

  def execute(self, statement:str) -> None:
    """Execute statement in BigQuery

    Args:
        statement (str): bigquery sql statement to execute

    Raises:
        Exception: if failed to query data from bigquery
    """    
    if self.client is None:
      raise Exception('Client not found. Please call create_connection().')

    try:
      queryJob = self.client.query(statement)  
      queryJob.result()  # Waits for statement to finish
      logger.info("Query completed successfully")
    except Exception as e:
      logger.error(e)
      raise e
  
  def create_table_in_bq(self, project:str, datset:str, table_name:str, schema:list, partition_by_column:str=None) -> None:
    """Create new table in BigQuery

    Args:
        project (str): project name
        datset (str): dataset name
        table_name (str): table name
        schema (list): table schema
        partition_by_column (str): partition column 
    """    
    dataset_ref = bigquery.DatasetReference(project, datset)

    table_ref = dataset_ref.table(table_name)
    table = bigquery.Table(table_ref, schema=schema)
    if partition_by_column is not None:
      table.time_partitioning = bigquery.TimePartitioning(
          type_=bigquery.TimePartitioningType.DAY,
          field=partition_by_column, 
      ) 

    table = self.client.create_table(table)

    logger.info(
        "Created table {}, partitioned on column {}".format(
            table.table_id, table.time_partitioning.field if partition_by_column is not None else 'None'
        )
    )

  def upload_dataframe_to_bq(self, targetedTable:str, dataframe:pd.DataFrame, schema:list, writeDisposition:str='WRITE_APPEND') -> None:
    """
      Args:
        targetedTable (str) : targeted table id (full table name)
        schema (list) : table schema
        dataframe (pd.DataFrame) : pandas dataframe to import to targeted table
        writeDisposition (str) : Optionally, specifies the action that occurs if the destination table already exists.
            The following values are supported:
              WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data and uses the schema from the load.
              WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
              WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.
            The default value is WRITE_APPEND.
    """
    try:
      jobConfig = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=writeDisposition
      )
      
      # Make an API request.
      job = self.client.load_table_from_dataframe(
          dataframe, targetedTable, job_config=jobConfig
      )  
      job.result()  # Wait for the job to complete.
    except Exception as e:
      logger.error(e)
      raise e
  
  def get_schema_field_by_value(self, columnName:str, columnValue:object) -> bigquery.SchemaField:
    columnDType = type(columnValue)

    if columnDType == str:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.STRING)
    if columnDType == int:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.INT64)
    if columnDType == float:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.FLOAT)
    if columnDType == bool:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.BOOLEAN)
    if columnDType == datetime.date:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.DATE)
    if columnDType == datetime.datetime:
      return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.DATETIME)
    return bigquery.SchemaField(columnName, bigquery.enums.SqlTypeNames.STRING)

  def generate_bq_schema_from_dictionary(self, df:dict) -> list:
    schema = []
    for key,value in df.items():
      schema.append(self.get_schema_field_by_value(key, value))
    return schema
