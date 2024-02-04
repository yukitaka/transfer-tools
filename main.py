import argparse
from dotenv import load_dotenv
from src.confluence import convert as cc
from src.growi import download as gd
from src.interactor import upload as uploader
from src.interactor.download import Confluence
from src.interactor.diff import Diff


def main():
    parser = argparse.ArgumentParser(
        description='Transfer confluence to growi and jira to redmine'
    )
    subparsers = parser.add_subparsers(help='commands')
    differ = subparsers.add_parser('diff', help='see `diff -h`')
    differ.set_defaults(handler=Diff.pages)

    confluence = subparsers.add_parser('confluence', help='see `confluence -h`')
    confluence_subparsers = confluence.add_subparsers(help='confluence commands')
    # downloader
    confluence_download = confluence_subparsers.add_parser('download', help='see `download -h`')
    confluence_download_contents_subparsers = confluence_download.add_subparsers(help='download contents')
    # pages
    add_download(confluence_download_contents_subparsers, Confluence.pages)
    # comments
    confluence_download_comments = confluence_download_contents_subparsers.add_parser('comments', help='see `comments -h`')
    confluence_download_comments.add_argument('-A', '--all', action='store_true', help='all comments')
    confluence_download_comments.add_argument('--recently', action='store', help='recently comments count', default=50)
    confluence_download_comments.set_defaults(handler=Confluence.comments)
    # attachments
    confluence_download_attachments = confluence_download_contents_subparsers.add_parser('attachments', help='see `attachments -h`')
    confluence_download_attachments.add_argument('-A', '--all', action='store_true', help='all attachments')
    confluence_download_attachments.add_argument('--recently', action='store', help='recently attachments count', default=50)
    confluence_download_attachments.set_defaults(handler=Confluence.attachments)

    # convert
    confluence_convert = confluence_subparsers.add_parser('convert', help='see `convert -h`')
    # pages
    confluence_convert_contents_subparsers = confluence_convert.add_subparsers(help='convert contents')
    confluence_convert_pages = confluence_convert_contents_subparsers.add_parser('pages', help='see `pages -h`')
    confluence_convert_pages.add_argument('-A', '--all', action='store_true', help='all pages')
    confluence_convert_pages.add_argument('--recently', action='store', help='recently pages count', default=50)
    confluence_convert_pages.set_defaults(handler=cc.pages)

    # growi
    growi = subparsers.add_parser('growi', help='see `growi -h`')
    growi_subparsers = growi.add_subparsers(help='growi commands')
    # downloader
    growi_download = growi_subparsers.add_parser('download', help='see `download -h`')
    growi_download_contents_subparsers = growi_download.add_subparsers(help='download contents')
    # pages
    add_download(growi_download_contents_subparsers, gd.pages)
    # uploader
    growi_upload = growi_subparsers.add_parser('upload', help='see `upload -h`')
    growi_upload.set_defaults(handler=uploader.upload)


    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

def add_download(parent, handler):
    download_pages = parent.add_parser('pages', help='see `pages -h`')
    download_pages.add_argument('-A', '--all', action='store_true', help='all pages')
    download_pages.add_argument('--recently', action='store', help='recently pages count', default=50)
    download_pages.set_defaults(handler=handler)

if __name__ == '__main__':
    load_dotenv()
    main()
