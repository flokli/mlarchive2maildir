import logging

from cleo import Application, Command

from mlarchive2maildir.mailbox import locked_messageid_maildir
from mlarchive2maildir.pipermail import get_mbox_urls


class ImportCommand(Command):
    """
    Imports mails from pipermail. Pass either the url to the archive listing, or an URL to a specific mbox

    import
        {url : The URL of one pipermail archive listing or a specific mbox file}
        {maildir : The path to the maildir folder. Will be created if it doesn't exist already}
        {--list-id= : The List-Id header to set}
        {--reply-to= : The Reply-To header to set}
    """

    def handle(self):
        url = self.argument('url')
        maildir_path = self.argument('maildir')

        headers = dict()
        for header in ['List-Id', 'Reply-To']:
            if self.option(header.lower()):
                headers[header] = self.option(header.lower())

        with locked_messageid_maildir(maildir_path) as maildir:
            if url.endswith('.txt') or url.endswith('.txt.gz'):
                maildir.import_mbox_from_url(url, headers)
            if '/pipermail/' in url:
                logging.info('Querying {} for mbox urls'.format(url))
                mbox_urls = list(get_mbox_urls(url))
                progress = self.progress_bar(len(mbox_urls))
                for mbox_url in mbox_urls:
                    maildir.import_mbox_from_url(mbox_url, headers)
                    progress.advance()
            else:
                self.error('unknown url, exiting')
                return -1

    @staticmethod
    def _import_mbox_url(maildir, url):
        logging.debug('importing mbox from {}'.format(url))
        maildir.import_mbox_from_url(url)


def main():
    application = Application()
    application.add(ImportCommand())
    application.run()

if __name__ == '__main__':
    main()
