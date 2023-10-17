#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""This script contains Logger instance to print data with timestamp on console or log to file
"""

# set timezone for data ingestion
from fp_th_di.date_utils import *

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

# Logger tool to print data with timestamp
class Logger:
  def appendLog(self, filename:str, *txt):
    with open(filename, 'a') as f:
      txt = [str(t) for t in txt]
      f.write(','.join(txt) + '\n')

  def log_info_with_timestamp(self, filename:str, *txt):
    with open(filename, 'a') as f:
      txt = [str(t) for t in txt]
      f.write('[INFO] ' + now().strftime('%Y-%m-%d %X') + ' - ' + ' '.join(txt) + '\n')

  def log_error_with_timestamp(self, filename:str, *txt):
    with open(filename, 'a') as f:
      txt = [str(t) for t in txt]
      f.write('[ERROR] ' + now().strftime('%Y-%m-%d %X') + ' - ' + ' '.join(txt) + '\n')

  def writeToFile(self, filename:str, txt:str):
    with open(filename, 'w') as f:
      f.write(txt)

  def info(self, *txt):
    txt = [str(t) for t in txt]
    print('[INFO]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt))

  def error(self, *txt):
    txt = [str(t) for t in txt]
    try:
      prepared = ' '.join(['[ERROR]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt)])
      finalText = bcolors.FAIL + prepared + bcolors.ENDC
      print(finalText)
    except Exception as e:
      print('[ERROR]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt))

  def warning(self, *txt):
    txt = [str(t) for t in txt]
    try:
      prepared = ' '.join(['[WARNING]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt)])
      finalText = bcolors.WARNING + prepared + bcolors.ENDC
      print(finalText)
    except Exception as e:
      print('[WARNING]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt))

  def exception(self, *txt):
    txt = [str(t) for t in txt]
    print('[ERROR]', now().strftime('%Y-%m-%d %X'), '-', ' '.join(txt))

  def logInfo(self, filename:str, *txt):
    txt = [str(t) for t in txt]
    logStr = '[INFO]' + now().strftime('%Y-%m-%d %X') + ' - ' + ' '.join(txt)
    self.appendLog(filename, logStr)

  def logError(self, filename:str, *txt):
    txt = [str(t) for t in txt]
    logStr = '[ERROR]' + now().strftime('%Y-%m-%d %X') + ' - ' + ' '.join(txt)
    self.appendLog(filename, logStr)

logger = Logger()
