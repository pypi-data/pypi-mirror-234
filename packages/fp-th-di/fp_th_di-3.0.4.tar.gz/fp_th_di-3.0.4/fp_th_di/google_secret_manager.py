#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""This script contains functions to handle secret values
"""

from google.cloud import secretmanager
import hashlib


def secret_hash(secretValue: str):
  """Get the sha224 hash of the secret value

    Args:
      secretValue (str): secret string to hash

    Returns:
        _Hash: sha224 of utf-8 secret value
    """
  return hashlib.sha224(bytes(secretValue, "utf-8")).hexdigest()

def get_secret_value_from_google(projectId: str, secretId: str, versionId='latest') -> str:
  """Get secret from Google Secret Manager

  Args:
      projectId (str): project id or name
      secretId (str): secret id or name
      versionId (str, optional): secret version. Defaults to 'latest'.

  Returns:
      str: secret stored in Google Secret Manager
  """
  client = secretmanager.SecretManagerServiceClient()

  # resource name of the targeted version
  name = f'projects/{projectId}/secrets/{secretId}/versions/{versionId}'

  # access the version
  response = client.access_secret_version(name=name)

  # decode payload
  return response.payload.data.decode('UTF-8')
