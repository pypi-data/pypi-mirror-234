#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""This script contains functions to handle cloud storage
"""

from google.cloud import storage

def upload_to_bucket(remoteFilepath, localFilepath, bucketName:str):
    """ Upload data to a bucket"""
    storage_client = storage.Client()

    # get bucket to upload
    bucket = storage_client.get_bucket(bucketName)
    blob = bucket.blob(remoteFilepath)
    blob.upload_from_filename(localFilepath)
    print(blob)
    #returns a public url
    return blob.public_url
