"""
A chunker for iterables
"""
import io
import json

from django.core.serializers.json import DjangoJSONEncoder


class RecordIterator:
    """
    The record iterator
    """

    def __init__(self, record_start, record_end, records):
        """
        Iterators over the records

        :param record_start:    Iterator starting point
        :param record_end:      Iterator endpoint
        :param records:         The records
        """
        self._record_start = record_start
        self._record_end = record_end
        self._records = records

    def __iter__(self):
        """
        Gets the iterable

        :return: Iterable self
        """
        return self

    def __len__(self):
        """
        Length of the iterable

        :return: Remaining iterator size
        """
        return self._record_end - self._record_start

    def __next__(self):
        """
        Get the next value

        :return: The next record batch
        """
        if self._record_start < self._record_end:
            record = self._records[self._record_start]
            self._record_start += 1
            return record
        else:
            raise StopIteration


class ChunkedIterator:
    """
    A chunkedI Iterator
    """

    def __init__(self, records, chunk_size=100, offset=0):
        """
        Chunks records and creates an iterator.

        :param records: Records in a list
        :param chunk_size: Number of records per chunk
        :param offset: Starting offset
        """
        self._current_offset = offset
        self._records = records
        self._chunk_size = chunk_size
        if self._chunk_size == 0:
            self._chunk_size = len(records)
        if offset:
            if len(self._records) > offset:
                self._records = self._records[offset:]
            else:
                self._records = []

    def has_next(self):
        """
        Whether the iterator has a next batch

        :return:    Whether there is a next batch
        """
        return self.__len__() > 0

    def __len__(self):
        """
        Get the length

        :return: Length of records after the current offset or 0
        """
        if self._records:
            if len(self._records) > self._current_offset:
                return len(self._records) - self._current_offset
        return 0

    def __iter__(self):
        """
        Return self as the iterator

        :return:    Self as iterator
        """
        return self

    def __next__(self):
        """
        Get the next record batch as an iterable

        :return:    The next batch of records or None at the end
        """
        if self.__len__() > 0:
            end = self._current_offset + self._chunk_size
            end = min(len(self._records), end)
            record_it = RecordIterator(self._current_offset, end, self._records)
            self._current_offset = end
            return record_it
        raise StopIteration


def to_string_io(batch):
    """
    Converts a batch iterator to a StringIo object

    :param batch:   The batch iterator
    :param use_django:  Whether to dump with the django encoder
    :return:    The string IO object
    """
    sio = io.BytesIO()
    for record in batch:
        l = json.dumps(record, cls=DjangoJSONEncoder)
        l += "\n"
        sio.write(l.encode())
    return sio
