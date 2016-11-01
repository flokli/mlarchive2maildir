import mailbox
from contextlib import contextmanager

import tempfile

from io import BytesIO

import gzip

import logging
import requests

from mlarchive2maildir.message import deobfuscate


class MessageIdMaildir(mailbox.Maildir):
    """
    An extension of the mailbox.Maildir class that you can ask
    whether a message with a specific message id already exists
    """
    _message_ids = None

    def __init__(self, dirname, factory=None, create=True):
        super().__init__(dirname, factory, create)

        self._build_msgid_cache()

    def add(self, message):
        super().add(message)
        self._message_ids.add(message['message-id'])

    def _build_msgid_cache(self):
        self._message_ids = set()
        for key, message in self.items():
            self._message_ids.add(message['message-id'])

    def contains_msgid(self, message_id):
        return message_id in self._message_ids

    def import_mbox_from_url(self, url, headers=None):
        """
        request a mbox by url, and pipes all messages
        into the passed maildir object
        """

        if url.endswith('.txt'):
            suffix = '.txt'
        elif url.endswith('.txt.gz'):
            suffix = '.txt.gz'
        else:
            raise Exception('Invalid file suffix')

        # get archive url stream
        stream = BytesIO(requests.get(url).content)

        if suffix == '.txt.gz':
            stream = gzip.open(stream)

        # open mbox
        with mbox_from_stream(stream) as tmbox:
            for key, message in tmbox.items():
                if message['message-id'] is None:
                    continue

                deobfuscate(message)

                if not self.contains_msgid(message['message-id']):
                    logging.debug('imported {}'.format(message['message-id']))

                    if headers:
                        for (header, value) in headers.items():
                            del message[header]
                            message[header] = value

                    self.add(message)
                else:
                    logging.warning('maildir already contains msgid {} ({}), skipping…'.format(message['message-id'],
                                                                                               message['subject']))


@contextmanager
def mbox_from_stream(f):
    """
    consumes a file-like object containing a mailbox.
    will yield a mailbox.Mailbox object out of a temporary directory,
    and clean up afterwards
    :param f: the file-like object
    """
    with tempfile.NamedTemporaryFile(mode='w+b') as tmbox_f:
        tmbox_f.write(f.read())
        tmbox_f.flush()

        tmbox = mailbox.mbox(tmbox_f.name)
        yield tmbox


@contextmanager
def locked_messageid_maildir(maildir_path):
    """
    will yield a MessageIdMaildir, which is locked
    :param maildir_path: the path to a mailbox
    """
    maildir = MessageIdMaildir(maildir_path)

    maildir.lock()

    # override the regular add method
    maildir.normal_add = maildir.add

    yield maildir
    maildir.unlock()
