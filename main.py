import argparse
from dotenv import load_dotenv
from src.confluence import download
from src.confluence import convert

def main():
    parser = argparse.ArgumentParser(
        description='Transfer confluence to growi and jira to redmine'
    )
    subparsers = parser.add_subparsers(help='confluence commands')

    confluence = subparsers.add_parser('confluence', help='see `confluence -h`')
    confluence_subparsers = confluence.add_subparsers(help='confluence commands')
    # downloader
    confluence_download = confluence_subparsers.add_parser('download', help='see `download -h`')
    # pages
    confluence_download_contents_subparsers = confluence_download.add_subparsers(help='download contents')
    confluence_download_pages = confluence_download_contents_subparsers.add_parser('pages', help='see `pages -h`')
    confluence_download_pages.add_argument('-A', '--all', action='store_true', help='all pages')
    confluence_download_pages.add_argument('--recently', action='store', help='recently pages count', default=50)
    confluence_download_pages.set_defaults(handler=download.pages)
    # comments
    confluence_download_comments = confluence_download_contents_subparsers.add_parser('comments', help='see `comments -h`')
    confluence_download_comments.add_argument('-A', '--all', action='store_true', help='all comments')
    confluence_download_comments.add_argument('--recently', action='store', help='recently comments count', default=50)
    confluence_download_comments.set_defaults(handler=download.comments)
    # attachments
    confluence_download_attachments = confluence_download_contents_subparsers.add_parser('attachments', help='see `attachments -h`')
    confluence_download_attachments.add_argument('-A', '--all', action='store_true', help='all attachments')
    confluence_download_attachments.add_argument('--recently', action='store', help='recently attachments count', default=50)
    confluence_download_attachments.set_defaults(handler=download.attachments)

    # convert
    confluence_convert = confluence_subparsers.add_parser('convert', help='see `convert -h`')
    # pages
    confluence_convert_contents_subparsers = confluence_convert.add_subparsers(help='convert contents')
    confluence_convert_pages = confluence_convert_contents_subparsers.add_parser('pages', help='see `pages -h`')
    confluence_convert_pages.add_argument('-A', '--all', action='store_true', help='all pages')
    confluence_convert_pages.add_argument('--recently', action='store', help='recently pages count', default=50)
    confluence_convert_pages.set_defaults(handler=convert.pages)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    load_dotenv()
    main()
