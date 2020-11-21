import logging

import click
import click_log

from mlarchive2maildir.mailbox import locked_messageid_maildir
from mlarchive2maildir.pipermail import get_mbox_urls

logger = logging.getLogger()
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    pass


@cli.command('import')
@click.argument('url')
@click.argument('maildir', type=click.Path())
@click.option('--list-id', required=True, help='The List-Id header to set')
@click.option('--reply-to', help='The Reply-To header to set')
def cli_import(**kwargs):
    """
    Imports mails from pipermail. Pass either the URL to the archive listing, or to a specific mbox
    """
    url = kwargs['url']
    maildir_path = kwargs['maildir']
    list_id = kwargs['list_id']
    reply_to = kwargs['reply_to']

    headers = dict()
    if list_id:
        headers['List-Id'] = list_id
    if reply_to:
        headers['Reply-To'] = reply_to

    with locked_messageid_maildir(maildir_path) as maildir:
        mbox_urls = []
        if url.endswith('.txt') or url.endswith('.gz'):
            mbox_urls.append(url)
        else:
            logger.debug('Querying {} for mbox urls'.format(url))
            mbox_urls.extend(get_mbox_urls(url))

        if len(mbox_urls) == 0:
            logger.critical("Unable to find any mboxes at {}, exiting!")
            return -1

        with click.progressbar(mbox_urls) as bar:
            for mbox_url in bar:
                try:
                    maildir.import_mbox_from_url(mbox_url, headers)
                except UnicodeDecodeError as e:
                    logger.warning("Error importing mbox at {}, skipping: {}".format(mbox_url, e))
