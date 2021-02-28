"""
CSV source io
"""
import codecs
import os

import boto3
import csv


class CSVSource:
    """
    Intended to offer download and read support from a file
    """

    def __init__(self, fpath, headers=None, batch_size=100):
        """
        Constructor

        :param fpath:   The file path to the csv
        :param headers: Headers to read in the order they appear in the fle
        :param batch_size:  The overall batch size
        """
        assert fpath
        self._fpath = fpath
        self._batch_size = batch_size
        self._fp = None
        self._headers = headers
        self._do_read = True
        self._reader = None

    def close(self):
        """
        Closes file pointer
        """
        self._fp.close()

    def download(self):
        """
        Download the S3 target file or files. Used when stream is False
        """
        self._fp = open(self._fpath, newline='\x0a')
        print(self._fp)
        self._reader = csv.DictReader(self._fp, fieldnames=self._headers)

    def __iter__(self):
        """
        Returns self as an iteration. Sets up the stream from S3.

        :return:    Self as an iterator
        """
        self.download()
        return self

    def __next__(self):
        """
        Iterates through a CSV from s3.
        """
        batch = []
        if self._reader is None:
            self.download()
        if self._do_read:
            try:
                while len(batch) < self._batch_size:
                    d = self._reader.__next__()
                    if d:
                        batch.append(d)
                    else:
                        break
                return batch
            except StopIteration as e:
                self._do_read = False
                if len(batch) > 0:
                    return batch
                else:
                    raise StopIteration
        else:
            raise StopIteration


class S3CSVSource:
    """
    Intended to offer download and read support from S3
    """

    def __init__(self, bucket, key=None, temp_folder=None, stream=False, profile=None, batch_size=10000, region=None, s3_filter=None):
        """
        Constructor

        :param bucket:  The s3 bucket
        :param key:     Key to the s3 if specific or None for all
        :param temp_folder: Where to place the temporary folder
        :param s3_filter:  Filter to use when searching for resources
        :param stream:  Whether to stream the file
        :param profile: The profile name to use if not in the AWS_PROFILE environment var
        :param region: Region to use if file is not listed
        """
        profile_name = profile
        if profile_name is None:
            profile_name = os.environ["AWS_PROFILE"]
        self._boto = boto3.session.Session(profile_name=profile_name)
        self._s3 = self._boto.client("s3")
        self._key = key
        self._keys = []
        self._temp_folder = temp_folder
        self._stream = stream
        self._filter = s3_filter
        self._bucket = bucket
        self._reader = None
        self._batch_size = batch_size
        self._do_read = True
        self._region = region

    def get_keys(self):
        """
        Get the keys
        """
        if self._key is None and self._bucket and self._filter:
            if self._region:
                kl = self._boto.resource("s3", region_name=self._region)
            else:
                kl = self._boto.resource("s3")
            kl = kl.Bucket(self._bucket)
            objects = [x.key for x in kl.objects.all() if self._filter in x.key and ".csv" in x.key]
            return objects
        else:
            return None

    def download(self):
        """
        Download the S3 target file or files. Used when stream is False
        """
        if self._bucket and self._stream is False:
            if self._key is None:
                self._keys = self.get_keys()
                if self._keys is None:
                    raise ValueError
                else:
                    if len(self._keys) > 0:
                      self._key = self._keys.pop()
            if self._key:
                data = self._s3.get_object(Bucket=self._bucket, Key=self._key)
                self._reader = csv.DictReader(codecs.getreader("utf-8")(data["Body"]))

    def get_next_reader(self):
        """
        Get the next io from the keys

        :return: The io or None
        """
        if self._keys and len(self._keys) > 0:
            self._key = self._keys.pop()
            data = self._s3.get_object(Bucket=self._bucket, Key=self._key)
            self._reader = csv.DictReader(codecs.getreader("utf-8")(data["Body"]))
            return self._reader
        else:
            return None

    def __iter__(self):
        """
        Returns self as an iteration. Sets up the stream from S3.

        :return:    Self as an iterator
        """
        self.download()
        return self

    def __next__(self):
        """
        Iterates through a CSV from s3.
        """
        if self._reader is None:
            self.download()
        if self._reader:
            batch = []
            if self._do_read:
                while len(batch) < self._batch_size:
                    try:
                        d = self._reader.__next__()
                        if d:
                            batch.append(d)
                    except StopIteration as e:
                        if self._keys and len(self._keys) > 0:
                            self._reader = self.get_next_reader()
                            if self._reader is None:
                                raise ValueError("Failed to Get Next Reader")
                        else:
                            self._do_read = False
                            if len(batch) > 0:
                                return batch
                            else:
                                raise StopIteration
            else:
                raise StopIteration
        else:
            raise StopIteration

