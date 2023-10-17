import boto3
import requests
from boto3.s3.transfer import TransferConfig
from s3transfer import S3Transfer
import os, sys
import threading
import uuid
from slugify import slugify
from datetime import datetime, timedelta
accountId='0bccb32eafa137e718623dc513358a41'
aws_access_key_id='79ae53e1351c60ec16186c501e6be38a'
aws_secret_access_key='def0fda9c48e299faab3c0d9ef438f6c596808349cfa108f474de942dfc27532'
S3_BUCKET='victor'
KEY_PATH='files/'
DOWNLOAD_PATH='https://results.cacherecords.net/files/'
class ProgressUploadPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
class CloudFlareHelper(object):

    def get_config_sv(self, name):

        global accountId
        global aws_access_key_id
        global aws_secret_access_key
        global S3_BUCKET
        global KEY_PATH
        global DOWNLOAD_PATH
        obj = requests.get(f"http://driver.69hot.info/r2/manager/get/{name}").json()
        if "id" in obj:
            accountId = obj['account_id']
            aws_access_key_id = obj['access_key_id']
            aws_secret_access_key = obj['access_key_secret']
            S3_BUCKET = obj['bucket']
            KEY_PATH = obj['key_path']
            DOWNLOAD_PATH = obj['home_url']
    def __init__(self, name_sv="results_cacherecords"):
        self.get_config_sv(name_sv)
        self.s3_client = boto3.client('s3', endpoint_url=f"https://{accountId}.r2.cloudflarestorage.com",
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
        self.resource = boto3.resource('s3', endpoint_url=f"https://{accountId}.r2.cloudflarestorage.com",
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)
        self.config = TransferConfig(multipart_threshold=1024*1024*100, max_concurrency=10,
                        multipart_chunksize=1024*1024*100, use_threads=True)
        self.transfer = S3Transfer(self.s3_client, self.config)
    def upload(self, file_path):
        download_url = None
        try:
            file_name = os.path.basename(file_path)
            file_name_new = file_name.split(".")[0]
            file_name_new = slugify(file_name_new)
            file_name_new = file_name_new + "-" + str(uuid.uuid4())[:8] + "." + file_name.split(".")[1]
            key = KEY_PATH + file_name_new
            download_url = DOWNLOAD_PATH + file_name_new
            # s = self.transfer.upload_file(file_path, S3_BUCKET, key, callback=ProgressUploadPercentage(file_path))
            s = self.transfer.upload_file(file_path, S3_BUCKET, key)
        except:
            download_url = None
            pass
        return download_url
    def download(self, url, file_path):
        if DOWNLOAD_PATH in url:
            file_name = os.path.basename(url)
            key = KEY_PATH + file_name
            self.transfer.download_file(S3_BUCKET, key, file_path)
            return file_path
        return None
    def delete_file(self, url):
        if DOWNLOAD_PATH in url:
            file_name = os.path.basename(url)
            key = KEY_PATH + file_name
            self.s3_client.delete_object(Bucket=S3_BUCKET, Key=key)
            return "ok"
        return "error"
    def delete_expired_day(self, days=3):
        bucket = self.resource.Bucket(S3_BUCKET)
        for file in bucket.objects.filter(Prefix=KEY_PATH):
            # compare dates
            delete_day = datetime.today() - timedelta(days=days)
            delete_day=delete_day.replace(tzinfo=None)
            if file.last_modified.replace(tzinfo=None) < delete_day:
                # print results
                print('Delete File Name: %s ---- Date: %s' % (file.key, file.last_modified))
                file.delete()