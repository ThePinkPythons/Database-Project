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

        :param fpath:   The file path to the db
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
