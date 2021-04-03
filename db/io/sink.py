"""
CSV Sink
"""

import csv


class CSVSink(object):

    def __init__(self, fpath, headers):
        """
        Constructor

        :param fpath:   The file path
        :param headers: The headers to use
        """
        self._fp = open(fpath, 'w', newline='')
        self._writer = csv.DictWriter(self._fp, fieldnames=headers)
        self._writer.writeheader()

    def close(self):
        """
        Close the file object
        """
        self._fp.close()

    def write_rows(self, batch):
        """
        Write the rows to a file

        :param batch:   Batch of dictionaries
        """
        self._writer.writerows(batch)

    def write_row(self, record):
        """
        Write a row to file

        :param record:  The record
        """
        self._writer.writerow(record)
