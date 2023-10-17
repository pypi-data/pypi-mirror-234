#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""This script contains helper functions related to date and datetime
"""

import datetime as dt
import os

HOUR_OFFSET_ENV_NAME='HOUR_OFFSET'

def set_hour_offset(offset:float):
  """Set offset hour to add to datetime.now timestamp

  Args:
      offset (float): 
  """  
  os.environ[HOUR_OFFSET_ENV_NAME] = offset

def get_hour_offset(offset:float):
  """Get offset hour set for your environment
  """
  return os.getenv(HOUR_OFFSET_ENV_NAME, None)

def now() -> dt.datetime:
  """Gets current datetime.
    To add hour offset, set HOUR_OFFSET environment using os.setenv function

  Returns:
      dt.datetime: datetime object
  """    
  return (dt.datetime.now() + dt.timedelta(hours=os.getenv(HOUR_OFFSET_ENV_NAME, 0)))

def today() -> dt.date:
  """Get today date

  Returns:
      dt.date: date object from datetime class
  """  
  return dt.datetime.now().date()

def days_before(days:int, date:dt.datetime = None) -> dt.date:
  """Get date of N days before the given date

  Args:
      days (int): N numbers of days
      date (dt.datetime, optional): initial date to subtract N days from. If not specified, it's using current date by default

  Returns:
      dt.date: N days before date
  """  
  if date is None:
    return (now() - dt.timedelta(days=days)).date() 
  return (date - dt.timedelta(days=days)).date()

def days_after(days:int, date:dt.datetime = None) -> dt.date:
  """Get date of N days after the given date

  Args:
      days (int): N numbers of days
      date (dt.datetime, optional): initial date to add N days to. If not specified, it's using current date by default

  Returns:
      dt.date: N days after date
  """  
  if date is None:
    return (now() + dt.timedelta(days=days)).date() 
  return (date + dt.timedelta(days=days)).date()

def yesterday() -> dt.date:
  """Yesterday date

  Returns:
      dt.date: yesterday date object
  """  
  return days_before(1)  

def tomorrow() -> dt.datetime:
  """Tomorrow date

  Returns:
      dt.datetime: tomorrow date object
  """  
  return days_after(1)

def currentHour() -> str:
  """Gets current hour in HH format. 
  For example: 00, 01, 02, ..., 12, 13, ... ,23

  Returns:
      str: 2 digits hour in 24 hour format
  """  
  return now().strftime('%H')

def currentMinute() -> str:
  """Gets current minute of the current hour

  Returns:
      str: minute
  """  
  return now().strftime('%M')

def str_to_date(text:str, dateFormat:str = '%Y-%m-%d') -> dt.date:
  """Convert string to date 

  Args:
      text (str): date string
      dateFormat (str, optional): Format of the given date string. Defaults to '%Y-%m-%d'.

  Returns:
      dt.datetime._date: date object
  """  
  return dt.datetime.strptime(text, dateFormat).date()

def str_to_datetime(text:str, dateTimeFormat:str = '%Y-%m-%d %H:%M:%S') -> dt.datetime:
  """Convert string to datetime

  Args:
      text (str): datetime string
      dateTimeFormat (str, optional): Format of the given datetime string. Defaults to '%Y-%m-%d %H:%M:%S'.

  Returns:
      dt.datetime: datetime object
  """  
  try:
    return dt.datetime.strptime(text, dateTimeFormat).replace(microsecond=0)
  except Exception as e:
    return None

def date_to_str(date:dt.date, date_format:str = '%Y-%m-%d') -> str:
  """Convert date object to string

  Args:
      date (dt.date): date object to convert to string
      date_format (str, optional): Format of output string date. Defaults to '%Y-%m-%d'.

  Returns:
      str: string of date
  """  
  return dt.datetime(date.year, date.month, date.day).strftime(date_format) 

def datetime_to_str(date:dt.datetime, date_format:str = '%Y-%m-%d %H:%M:%S') -> str:
  """Convert datetime object to string

  Args:
      date (dt.datetime): datetime object to convert to string
      date_format (str, optional): Format of output string date. Defaults to '%Y-%m-%d %H:%M:%S'.

  Returns:
      str: string of datetime
  """  
  return date.strftime(date_format) 
