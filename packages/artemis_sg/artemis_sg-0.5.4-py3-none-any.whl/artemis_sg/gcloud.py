#!/usr/bin/env python

import datetime
import logging
import os
import time

import puremagic
from google.cloud import storage

from artemis_sg.config import CFG

MODULE = os.path.splitext(os.path.basename(__file__))[0]


class GCloud:
    def __init__(self, cloud_key_file, bucket_name="default"):
        self.cloud_api_call_count = 0
        # This environ setting needs to stay.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cloud_key_file
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def upload_cloud_blob(self, source_file_path, destination_blob_name):
        blob = self.bucket.blob(destination_blob_name)
        ret_val = blob.upload_from_filename(source_file_path)
        self.cloud_api_call_count += 1
        return ret_val

    def generate_cloud_signed_url(self, blob_name):
        """Generates a v4 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """

        blob = self.bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=30),
            method="GET",
        )
        self.cloud_api_call_count += 1

        return url

    def list_blobs(self, prefix):
        # FIXME: use page_token
        # page_token = None
        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix)
        self.cloud_api_call_count += 1
        return blobs

    def list_image_blobs(self, prefix):
        blobs = self.list_blobs(prefix)
        names = []
        for blob in blobs:
            if "image" in blob.content_type:
                names.append(blob.name)
        return names


def upload(file_source_dir, bucket_prefix, cloud_object):
    namespace = f"{MODULE}.{upload.__name__}"
    hour = 1 * 60 * 60
    blobs = cloud_object.list_image_blobs(bucket_prefix)
    for filename in os.listdir(file_source_dir):
        filepath = os.path.join(file_source_dir, filename)
        if os.path.isfile(filepath):
            file_blob_name = f"{bucket_prefix}/{filename}"
            # verify the file is an image, otherwise delete it
            try:
                kind = puremagic.from_file(filepath)
            except puremagic.main.PureError:
                kind = None
            if kind not in [".jpg", ".png"]:
                logging.error(
                    f"{namespace}: Err reading '{filename}', deleting '{filepath}'"
                )
                os.remove(filepath)
                continue
            # don't upload existing blobs unless the file is new
            file_age = time.time() - os.path.getmtime(filepath)
            if file_blob_name in blobs and file_age > hour:
                logging.info(
                    f"{namespace}: File '{filename}' found in Google Cloud "
                    f"bucket, not uploading."
                )
                continue
            else:
                logging.info(
                    f"{namespace}: Uploading '{file_blob_name}' to Google Cloud bucket."
                )
                cloud_object.upload_cloud_blob(filepath, file_blob_name)


def main():
    file_source_dir = CFG["asg"]["data"]["dir"]["upload_source"]
    bucket_name = CFG["google"]["cloud"]["bucket"]
    bucket_prefix = CFG["google"]["cloud"]["bucket_prefix"]
    cloud_key_file = CFG["google"]["cloud"]["key_file"]

    cloud_object = GCloud(cloud_key_file=cloud_key_file, bucket_name=bucket_name)
    upload(file_source_dir, bucket_prefix, cloud_object)


if __name__ == "__main__":
    main()
