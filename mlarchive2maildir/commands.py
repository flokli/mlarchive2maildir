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
        if url.endswith('.txt') or url.endswith('.txt.gz'):
            maildir.import_mbox_from_url(url, headers)
        if '/pipermail/' in url:
            logger.debug('Querying {} for mbox urls'.format(url))
            mbox_urls = list(get_mbox_urls(url))

            with click.progressbar(mbox_urls) as bar:
                for mbox_url in bar:
                    maildir.import_mbox_from_url(mbox_url, headers)
        else:
            click.echo(click.style('Unknown URL, exiting!', fg='red'))
            return -1
