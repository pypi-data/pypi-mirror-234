# Google utils: https://cloud.google.com/storage/docs/reference/libraries

import os
import platform
import subprocess
import time
from pathlib import Path

import requests
import torch
import wget


def gsutil_getsize(url=''):
    # gs://bucket/file size https://cloud.google.com/storage/docs/gsutil/commands/du
    s = subprocess.check_output(f'gsutil du {url}', shell=True).decode('utf-8')
    return eval(s.split(' ')[0]) if len(s) else 0  # bytes


def attempt_download(file):

    # Attempt file download if does not exist
    file = Path(str(file).strip().replace("'", ''))

    if not file.exists():
        os.makedirs(str(file.parent), exist_ok=True)
        wget.download(f'https://github.com/WongKinYiu/yolov7/releases/download/v0.1/{file.name}', out=f'{file.parent}/')


def gdrive_download(id='', file='tmp.zip'):
    # Downloads a file from Google Drive. from yolov7.utils.google_utils import *; gdrive_download()
    t = time.time()
    file = Path(file)
    cookie = Path('cookie')  # gdrive cookie
    print(f'Downloading https://drive.google.com/uc?export=download&id={id} as {file}... ', end='')
    file.unlink(missing_ok=True)  # remove existing file
    cookie.unlink(missing_ok=True)  # remove existing cookie

    # Attempt file download
    out = "NUL" if platform.system() == "Windows" else "/dev/null"
    os.system(f'curl -c ./cookie -s -L "drive.google.com/uc?export=download&id={id}" > {out}')
    if os.path.exists('cookie'):  # large file
        s = f'curl -Lb ./cookie "drive.google.com/uc?export=download&confirm={get_token()}&id={id}" -o {file}'
    else:  # small file
        s = f'curl -s -L -o {file} "drive.google.com/uc?export=download&id={id}"'
    r = os.system(s)  # execute, capture return
    cookie.unlink(missing_ok=True)  # remove existing cookie

    # Error check
    if r != 0:
        file.unlink(missing_ok=True)  # remove partial
        print('Download error ')  # raise Exception('Download error')
        return r

    # Unzip if archive
    if file.suffix == '.zip':
        print('unzipping... ', end='')
        os.system(f'unzip -q {file}')  # unzip
        file.unlink()  # remove zip to free space

    print(f'Done ({time.time() - t:.1f}s)')
    return r


def get_token(cookie="./cookie"):
    with open(cookie) as f:
        for line in f:
            if "download" in line:
                return line.split()[-1]
    return ""

# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     # Uploads a file to a bucket
#     # https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
#
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)
#
#     blob.upload_from_filename(source_file_name)
#
#     print('File {} uploaded to {}.'.format(
#         source_file_name,
#         destination_blob_name))
#
#
# def download_blob(bucket_name, source_blob_name, destination_file_name):
#     # Uploads a blob from a bucket
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)
#
#     blob.download_to_filename(destination_file_name)
#
#     print('Blob {} downloaded to {}.'.format(
#         source_blob_name,
#         destination_file_name))
